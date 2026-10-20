"""Local Apple Container/BuildKit and OrbStack adapters, never daemon starters."""

from __future__ import annotations

import json
import os
import re
import stat
from pathlib import Path

from _cleanup_common import CleanupError, canonical_digest
from _cleanup_native import (
    _candidate,
    _env,
    _executable,
    _json_read,
    _measurement,
    _path_identity,
    _read,
    _resolved,
    _version,
)

# Explicitly source-qualified buildctl contracts. Versions outside this set
# remain unsupported until their prune/filter/output behavior is reviewed.
BUILDCTL_VERSIONS = {"0.26.2"}
PRIVATE_FILTER = 'private=""'


def _name(value: str | None) -> str:
    if not value or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,126}", value):
        raise CleanupError("native_target_required", "Supply one exact container or builder name")
    return value


def _apple_snapshot(exe: dict, target: str) -> dict:
    rows = _json_read([exe["path"], "inspect", target])
    if not isinstance(rows, list) or len(rows) != 1 or rows[0].get("id") != target:
        raise CleanupError(
            "native_identity_unavailable", "Container inspection did not return the exact target"
        )
    row = rows[0]
    if not isinstance(row.get("configuration"), dict) or not isinstance(row.get("status"), dict):
        raise CleanupError("native_output_invalid", "Container 1.5.0 inspection shape is missing")
    return row


def _mounts(configuration: dict) -> tuple[list[dict], list[dict]]:
    included, skipped = [], []
    if not configuration.get("readOnly", False):
        included.append({"destination": "/", "kind": "rootfs"})
    for mount in configuration.get("mounts", []):
        kind = mount.get("type")
        if not isinstance(kind, dict) or len(kind) != 1:
            raise CleanupError("native_mount_unsupported", "Cannot identify Container mount type")
        kind_name = next(iter(kind))
        if kind_name not in {"block", "volume", "virtiofs", "tmpfs"}:
            raise CleanupError(
                "native_mount_unsupported", "Unreviewed Container mount type", type=kind_name
            )
        value = {key: mount[key] for key in ("source", "destination", "options", "type")}
        value["kind"] = kind_name
        if kind_name in {"block", "volume"} and "ro" not in mount["options"]:
            value["source_identity"] = _path_identity(mount["source"])
            included.append(value)
        else:
            skipped.append(value)
    return included, skipped


def _apple(owner: str, target: str | None) -> dict:
    target = _name(target or ("buildkit" if owner == "apple-buildkit" else None))
    exe = _executable("container")
    version = _version(exe, "container")
    row = _apple_snapshot(exe, target)
    if row["status"].get("state") != "running":
        raise CleanupError(
            "native_target_not_running",
            "Container must already be running; this helper never starts it",
            target=target,
            observed=row["status"].get("state"),
        )
    config = row["configuration"]
    if not row["status"].get("startedDate") or not config.get("creationDate"):
        raise CleanupError(
            "native_identity_unavailable", "Container creation/start identity is absent"
        )
    mounts, skipped = _mounts(config)
    endpoint = f"apple-container:xpc:uid:{os.getuid()}"
    root = _env().get("CONTAINER_ROOT")
    if root:
        # The normal XPC route cannot prove that an arbitrary root override
        # belongs to this service. Do not invent a second endpoint.
        raise CleanupError(
            "native_configuration_unsupported",
            "CONTAINER_ROOT override requires separate qualification",
        )
    engine = f"{endpoint}:container:{target}"
    identity = {
        "executable": exe,
        "version": version,
        "endpoint": endpoint,
        "container": target,
        "created": config["creationDate"],
        "started": row["status"]["startedDate"],
        "config_digest": canonical_digest(config),
        "mounts": mounts,
        "skipped_mounts": skipped,
        "mount_fingerprint": canonical_digest([mounts, skipped]),
    }
    paths = [m["source_identity"]["path"] for m in mounts if "source_identity" in m]
    scopes = [{"kind": "engine", "id": engine}] + [{"kind": "path", "path": p} for p in paths]
    if owner == "apple-container":
        action = {
            "type": "apple_container_clean",
            "container": target,
            "effect": "Trim writable rootfs and every writable block/volume mount; skip read-only and VirtioFS mounts",
        }
        result = _candidate(
            owner, target, action, identity, scopes, operation="reclaim", paths=paths
        )
        result["measurements"]["coverage"] += (
            "; rootfs host backing allocation unavailable from inspect"
        )
        return result
    # Pin an explicit Unix endpoint inside the reviewed container. Neither
    # buildctl environment defaults nor a TCP endpoint may redirect the prune.
    addr = "unix:///run/buildkit/buildkitd.sock"
    prefix = [exe["path"], "exec", target, "buildctl"]
    version_text = _read([*prefix, "--version"])
    found = re.search(r"\bv(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?)(?![\d.])", version_text)
    buildctl_version = found.group(1) if found else None
    if buildctl_version not in BUILDCTL_VERSIONS:
        raise CleanupError(
            "native_version_unsupported",
            "Guest buildctl version is not qualified",
            observed=buildctl_version,
            supported=sorted(BUILDCTL_VERSIONS),
        )
    identity.update(buildctl_version=buildctl_version, buildkit_endpoint=addr)
    rows = _json_read(
        [*prefix, "--addr", addr, "du", "--filter", "private", "--format", "{{json .}}"]
    )
    if rows is None:
        rows = []
    if not isinstance(rows, list):
        raise CleanupError("native_output_invalid", "Buildctl usage must be a JSON array")
    action = {
        "type": "apple_buildkit_private_prune",
        "container": target,
        "endpoint": addr,
        "effect": "Prune unused private BuildKit cache in the exact running container; preserve shared records/images/volumes",
    }
    result = _candidate(owner, target, action, identity, scopes, paths=paths)
    result["measurements"].update(
        engine_bytes=sum(r["Size"] for r in rows if not r.get("InUse", True)),
        engine_records=len(rows),
        engine_unit="bytes",
    )
    return result


def _socket(endpoint: str) -> dict:
    if not endpoint.startswith("unix:///"):
        raise CleanupError(
            "native_remote_denied",
            "Only an exact local Unix-socket endpoint is admitted",
            endpoint=endpoint,
        )
    identity = _path_identity(endpoint[len("unix://") :])
    if identity["type"] != stat.S_IFSOCK:
        raise CleanupError("native_endpoint_invalid", "Engine endpoint is not a Unix socket")
    return identity


def _docker_endpoint(exe: dict, endpoint: str) -> tuple[str, dict]:
    if "://" not in endpoint:
        rows = _json_read([exe["path"], "context", "inspect", _name(endpoint)])
        if not isinstance(rows, list) or len(rows) != 1:
            raise CleanupError(
                "native_identity_unavailable", "Docker context did not resolve uniquely"
            )
        endpoint = rows[0].get("Endpoints", {}).get("docker", {}).get("Host", "")
    identity = _socket(endpoint)
    return "unix://" + identity["path"], identity


def _inspect_builder(text: str, name: str) -> dict:
    before, separator, after = text.partition("Nodes:")
    header = dict(re.findall(r"^([^:\n]+):\s*(.*?)\s*$", before, re.M))
    if not separator or header.get("Name") != name:
        raise CleanupError("native_output_invalid", "Buildx did not inspect the selected builder")
    nodes = []
    for match in re.finditer(r"^Name:\s*(.+)$", after, re.M):
        start = match.start()
        end = after.find("\nName:", match.end())
        block = after[start : end if end >= 0 else len(after)]
        values = dict(re.findall(r"^([^:\n]+):\s*(.*?)\s*$", block, re.M))
        if values.get("Status") != "running" or "Error" in values:
            raise CleanupError(
                "native_target_not_running", "Every selected builder node must already be running"
            )
        nodes.append(
            {
                k: values[k]
                for k in ("Name", "Endpoint", "Status", "BuildKit version")
                if k in values
            }
        )
    if not nodes:
        raise CleanupError("native_identity_unavailable", "Builder nodes are absent")
    return {"driver": header.get("Driver"), "nodes": nodes}


def _buildx(target: str | None) -> dict:
    target = _name(target or "orbstack")
    exe = _executable("docker")
    version = _version(exe, "buildx", ["buildx", "version"])
    env = _env()
    docker_config = _resolved(env.get("DOCKER_CONFIG") or str(Path.home() / ".docker"))
    buildx_config = _resolved(env.get("BUILDX_CONFIG") or str(Path(docker_config) / "buildx"))
    instance = Path(buildx_config) / "instances" / target
    if instance.is_file():
        try:
            config = json.loads(instance.read_text())
        except (OSError, ValueError) as error:
            raise CleanupError(
                "native_configuration_unavailable", "Cannot read selected builder metadata"
            ) from error
        if config.get("Name") != target or config.get("Dynamic"):
            raise CleanupError(
                "native_builder_unsupported", "Dynamic or mismatched builders are unsupported"
            )
    else:
        # Buildx's context-backed docker driver has no instance file.
        config = {
            "Name": target,
            "Driver": "docker",
            "Nodes": [{"Name": target, "Endpoint": target}],
        }
    if config.get("Driver") not in {"docker", "docker-container"}:
        raise CleanupError(
            "native_builder_unsupported",
            "Only local docker and docker-container drivers are qualified",
        )
    expected = config.get("Nodes", [])
    if not expected:
        raise CleanupError("native_identity_unavailable", "Builder contains no nodes")
    # Resolve EVERY node before any daemon-facing read. ls would probe unrelated
    # remote builders; inspect target cannot be used before this locality check.
    resolved = []
    for node in expected:
        endpoint, socket = _docker_endpoint(exe, node["Endpoint"])
        resolved.append(
            {
                "name": node["Name"],
                "configured_endpoint": node["Endpoint"],
                "endpoint": endpoint,
                "socket": socket,
            }
        )
    live = _inspect_builder(_read([exe["path"], "buildx", "inspect", target]), target)
    if live["driver"] != config["Driver"] or [
        (n["Name"], n["Endpoint"]) for n in live["nodes"]
    ] != [(n["Name"], n["Endpoint"]) for n in expected]:
        raise CleanupError("native_conflict", "Live builder nodes differ from the local metadata")
    # Enforce OrbStack ownership by querying the already-resolved local daemon.
    engines = []
    plugin_identity = None
    for node in resolved:
        info = _json_read(
            [exe["path"], "--host", node["endpoint"], "info", "--format", "{{json .}}"]
        )
        if "orbstack" not in str(info.get("OperatingSystem", "")).lower() or not info.get("ID"):
            raise CleanupError(
                "native_engine_mismatch", "Resolved engine is not an identified OrbStack daemon"
            )
        plugins = info.get("ClientInfo", {}).get("Plugins", [])
        plugin = next((p for p in plugins if p.get("Name") == "buildx"), None)
        if not plugin or not plugin.get("Path"):
            raise CleanupError(
                "native_identity_unavailable",
                "Docker did not identify the active Buildx plugin executable",
            )
        plugin_identity = _path_identity(plugin["Path"])
        ps = Path(plugin_identity["path"]).stat()
        plugin_identity.update(size=ps.st_size, mtime_ns=ps.st_mtime_ns)
        engines.append(
            {
                "id": info["ID"],
                "endpoint": node["endpoint"],
                "server_version": info.get("ServerVersion"),
                "os": info["OperatingSystem"],
            }
        )
    identity = {
        "executable": exe,
        "version": version,
        "builder": target,
        "driver": live["driver"],
        "nodes": resolved,
        "live_nodes": live["nodes"],
        "engines": engines,
        "config_digest": canonical_digest(config),
        "docker_config": docker_config,
        "buildx_config": buildx_config,
        "buildx_executable": plugin_identity,
    }
    action = {
        "type": "orbstack_buildx_private_prune",
        "builder": target,
        "effect": "Prune unused private cache on every selected builder node; preserve shared cache, images, containers and volumes",
    }
    scopes = [{"kind": "engine", "id": "docker:" + node["endpoint"]} for node in resolved]
    rows = _read(
        [
            exe["path"],
            "buildx",
            "du",
            "--builder",
            target,
            "--filter",
            PRIVATE_FILTER,
            "--format",
            "{{json .}}",
        ]
    )
    try:
        usage = [json.loads(line) for line in rows.splitlines() if line.strip()]
    except ValueError as error:
        raise CleanupError("native_output_invalid", "Buildx usage JSON is malformed") from error
    result = _candidate("orbstack-buildx", target, action, identity, scopes)
    result["measurements"].update(
        engine_records=len(usage),
        engine_reported_sizes=[r.get("Size") for r in usage],
        engine_bytes=None,
        engine_unit="owner-formatted quantities, not exact bytes",
    )
    return result


def _orbstack(target: str | None) -> dict:
    exe = _executable("orb")
    version = _version(exe, "orb", ["version"])
    # OrbStack 2.2.3's installed data/README.txt names data.img.raw. Its
    # sandbox app-group directory is the vendor-owned default storage root.
    storage = Path.home() / "Library/Group Containers/HUAQ24HBR6.dev.orbstack/data/data.img.raw"
    path = _resolved(target or str(storage))
    # Do not turn an arbitrary file into an OrbStack reclaim target.
    expected = _resolved(str(storage))
    if path != expected:
        raise CleanupError(
            "native_storage_unsupported",
            "Only OrbStack's resolved app-group data.img.raw is qualified",
        )
    identity = {"executable": exe, "version": version, "storage": _path_identity(path)}
    if identity["storage"]["type"] != stat.S_IFREG:
        raise CleanupError(
            "native_storage_unsupported", "OrbStack backing store is not a regular sparse file"
        )
    return _candidate(
        "orbstack",
        target,
        {
            "type": "orbstack_observe_reclaim",
            "effect": "Observe automatic sparse-file shrink; submit no compaction or trim command",
        },
        identity,
        [{"kind": "path", "path": path}],
        operation="reclaim",
        paths=[path],
    )


def discover_engine(owner: str, target: str | None) -> dict:
    if owner.startswith("apple-"):
        return _apple(owner, target)
    return _buildx(target) if owner == "orbstack-buildx" else _orbstack(target)


def engine_argv(candidate: dict) -> list[str] | None:
    exe = candidate["identity"]["executable"]["path"]
    action = candidate["action"]
    match action["type"]:
        case "apple_container_clean":
            return [exe, "clean", action["container"]]
        case "apple_buildkit_private_prune":
            return [
                exe,
                "exec",
                action["container"],
                "buildctl",
                "--addr",
                action["endpoint"],
                "prune",
                "--filter",
                "private",
                "--format",
                "{{json .}}",
            ]
        case "orbstack_buildx_private_prune":
            return [
                exe,
                "buildx",
                "prune",
                "--builder",
                action["builder"],
                "--filter",
                PRIVATE_FILTER,
                "--force",
            ]
        case "orbstack_observe_reclaim":
            return None
    raise CleanupError("native_action_unsupported", "Unsupported typed native action")


def read_engine(candidate: dict, record: dict) -> dict | None:
    if candidate["owner"].startswith("apple-"):
        try:
            row = _apple_snapshot(
                candidate["identity"]["executable"], candidate["identity"]["container"]
            )
        except CleanupError:
            return None
        old = record.get("owner_identity", candidate["identity"])
        # An observed different VM incarnation, or the old VM now stopped,
        # establishes that its filesystem/BuildKit operations cannot continue.
        # Missing containers, unavailable services, and CLI exit alone do not.
        if row["status"].get("state") == "stopped" or row["status"].get("startedDate") not in (
            None,
            old["started"],
        ):
            return {
                "state": "partial",
                "execution_ended": True,
                "attribution": "unknown",
                "note": "The original container instance ended; no cleanup was replayed",
                "measurements": _measurement(candidate.get("measurement_paths", [])),
            }
    # Buildx supplies no per-prune handle. A changed socket/daemon ID is not
    # proof that the original daemon ended, so preserve unresolved custody.
    return None
