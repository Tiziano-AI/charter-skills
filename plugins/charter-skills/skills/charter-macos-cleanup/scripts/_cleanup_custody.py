"""Host-user resource claims; a dead writer is never proof of a finished effect."""

from __future__ import annotations

import contextlib
import fcntl
import json
import os
import pwd
import stat
import uuid
from pathlib import Path

from _cleanup_common import CleanupError


def account_home() -> Path:
    """Use the login account, never HOME or a projected harness directory."""
    return Path(pwd.getpwuid(os.getuid()).pw_dir)


def custody_path() -> Path:
    return account_home() / "Library/Application Support/Charter Mac Cleanup"


def normalize_scopes(scopes: list[dict]) -> list[dict]:
    if not isinstance(scopes, list) or not scopes:
        raise CleanupError("invalid_scopes", "Every action needs canonical resource scopes.")
    result, seen = [], set()
    for scope in scopes:
        if not isinstance(scope, dict):
            raise CleanupError("invalid_scopes", "Resource scope must be an object.")
        kind = scope.get("kind")
        if kind == "path" and set(scope) == {"kind", "path"}:
            value = scope["path"]
            if (
                not isinstance(value, str)
                or not value.startswith("/")
                or "\0" in value
                or os.path.normpath(value) != value
            ):
                raise CleanupError("invalid_scopes", "Path scope must be absolute and canonical.")
        elif kind == "engine" and set(scope) == {"kind", "id"}:
            value = scope["id"]
            if not isinstance(value, str) or not value.strip() or "\0" in value:
                raise CleanupError("invalid_scopes", "Engine scope needs an actual owner identity.")
        else:
            raise CleanupError("invalid_scopes", "Unknown resource scope.")
        key = (kind, value)
        if key not in seen:
            seen.add(key)
            result.append(dict(scope))
    return result


def path_overlaps(left: str, right: str) -> bool:
    return (
        left == right
        or left.startswith(right.rstrip("/") + "/")
        or right.startswith(left.rstrip("/") + "/")
    )


def scopes_overlap(left: list[dict], right: list[dict]) -> bool:
    for one in left:
        for two in right:
            if one["kind"] != two["kind"]:
                continue
            if one["kind"] == "engine" and one["id"] == two["id"]:
                return True
            if one["kind"] == "path" and path_overlaps(one["path"], two["path"]):
                return True
    return False


def candidate_scopes(candidate: dict) -> list[dict]:
    # A retained Python skeleton still has one consumer boundary. Claiming it
    # also avoids quadratic overlap checks between thousands of exact files.
    if candidate.get("kind") == "filesystem" and candidate.get("category") == "venv_payload":
        return normalize_scopes([{"kind": "path", "path": candidate.get("path")}])
    return normalize_scopes(candidate.get("scopes"))


def _path_identities(scopes: list[dict]) -> list[dict]:
    """Retain inode ancestry so a renamed claimed subtree is still claimed."""
    identities = []
    for scope in scopes:
        if scope["kind"] != "path":
            continue
        target = Path(scope["path"])
        ancestry = []
        identity = None
        for path in (target, *target.parents):
            try:
                info = path.stat(follow_symlinks=False)
            except FileNotFoundError:
                continue
            pair = [info.st_dev, info.st_ino]
            ancestry.append(pair)
            if path == target:
                identity = pair
        identities.append({"identity": identity, "ancestry": ancestry})
    return identities


def _identity_overlap(left: list[dict], right: list[dict]) -> bool:
    return any(
        (one["identity"] is not None and one["identity"] in two["ancestry"])
        or (two["identity"] is not None and two["identity"] in one["ancestry"])
        for one in left
        for two in right
    )


def _private_file(fd: int) -> None:
    info = os.fstat(fd)
    if (
        not stat.S_ISREG(info.st_mode)
        or info.st_uid != os.getuid()
        or stat.S_IMODE(info.st_mode) & 0o077
        or info.st_nlink != 1
    ):
        raise CleanupError(
            "unsafe_custody",
            "Custody files must be private, singly linked regular files.",
        )


def _directory(path: Path, create: bool) -> int:
    """Hold every descent with no-follow; never repair an unsafe existing directory."""
    if not path.is_absolute() or str(path) != os.path.normpath(path):
        raise CleanupError("unsafe_custody", "Custody directory must be absolute and normalized.")
    fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in path.parts[1:]:
            try:
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            except FileNotFoundError:
                if not create:
                    raise
                try:
                    os.mkdir(part, 0o700, dir_fd=fd)
                    os.fsync(fd)
                except FileExistsError:
                    pass
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = child
        info = os.fstat(fd)
        if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) & 0o077:
            raise CleanupError(
                "unsafe_custody",
                "Custody directory must be owned by this user and mode 0700.",
            )
        return fd
    except BaseException:
        os.close(fd)
        raise


class Lease:
    def __init__(self, custody: "Custody", claim: dict, fd: int):
        self.custody = custody
        self.claim = claim
        self.fd = fd

    def close(self) -> None:
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None

    def update(self, **fields) -> None:
        with self.custody.admission():
            current = self.custody._read(self.claim["claim_id"] + ".json")
            current.update(fields)
            self.custody._write(current["claim_id"] + ".json", current)
            self.claim = current

    def release(self) -> None:
        """Caller must first durably record a trusted definite execution end."""
        with self.custody.admission():
            os.unlink(self.claim["claim_id"] + ".json", dir_fd=self.custody.fd)
            os.fsync(self.custody.fd)
            os.unlink(self.claim["claim_id"] + ".lease", dir_fd=self.custody.fd)
            os.fsync(self.custody.fd)
        self.close()


class Custody:
    """Only tests inject state_dir. Public callers always share custody_path()."""

    def __init__(self, state_dir: str | Path | None = None, *, create: bool = True):
        self.path = Path(state_dir) if state_dir is not None else custody_path()
        try:
            self.fd = _directory(self.path, create)
        except FileNotFoundError:
            if create:
                raise
            self.fd = None
        except OSError as exc:
            raise CleanupError(
                "unsafe_custody",
                "Cannot securely open custody directory.",
                path=str(self.path),
                reason=str(exc),
            ) from exc

    def close(self) -> None:
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None

    @contextlib.contextmanager
    def admission(self):
        check = _directory(self.path, False)
        try:
            current, held = os.fstat(check), os.fstat(self.fd)
            if (current.st_dev, current.st_ino) != (held.st_dev, held.st_ino):
                raise CleanupError("unsafe_custody", "Custody directory changed while running.")
        finally:
            os.close(check)
        fd = os.open(
            "admission.lock",
            os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW,
            0o600,
            dir_fd=self.fd,
        )
        try:
            _private_file(fd)
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise CleanupError(
                    "custody_busy",
                    "Another caller is admitting or recording an action.",
                ) from exc
            yield
        finally:
            os.close(fd)

    def _read(self, name: str) -> dict:
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=self.fd)
        try:
            _private_file(fd)
            with os.fdopen(fd, "r", encoding="utf-8", closefd=False) as stream:
                value = json.load(stream)
            if not isinstance(value, dict):
                raise ValueError("Claim is not an object")
            return value
        except (ValueError, OSError) as exc:
            raise CleanupError(
                "custody_corrupt", "Cannot read durable resource claim.", claim=name
            ) from exc
        finally:
            os.close(fd)

    def _write(self, name: str, value: dict) -> None:
        temporary = ".write-" + uuid.uuid4().hex
        fd = os.open(
            temporary,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
            0o600,
            dir_fd=self.fd,
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8", closefd=False) as stream:
                json.dump(value, stream, sort_keys=True, ensure_ascii=False)
                stream.write("\n")
                stream.flush()
                os.fsync(fd)
            os.rename(temporary, name, src_dir_fd=self.fd, dst_dir_fd=self.fd)
            os.fsync(self.fd)
        finally:
            os.close(fd)
            try:
                os.unlink(temporary, dir_fd=self.fd)
            except FileNotFoundError:
                pass

    def _claims(self) -> list[dict]:
        result = []
        for name in sorted(os.listdir(self.fd)):
            if not name.endswith(".json"):
                continue
            claim = self._read(name)
            if (
                claim.get("schema_version") != 1
                or not isinstance(claim.get("claim_id"), str)
                or claim["claim_id"] + ".json" != name
                or not isinstance(claim.get("operation_path"), str)
            ):
                raise CleanupError("custody_corrupt", "Invalid durable resource claim.", claim=name)
            normalize_scopes(claim.get("scopes"))
            result.append(claim)
        return result

    def claim(self, candidate: dict, operation_path: str, operation_id: str) -> Lease:
        scopes = candidate_scopes(candidate)
        with self.admission():
            identities = _path_identities(scopes)
            conflicts = [
                c
                for c in self._claims()
                if scopes_overlap(scopes, c["scopes"])
                or _identity_overlap(identities, c.get("path_identities", []))
            ]
            if conflicts:
                raise CleanupError(
                    "resource_claimed",
                    "Resource has an active or unresolved action.",
                    claims=[
                        {
                            "claim_id": c["claim_id"],
                            "operation_path": c["operation_path"],
                        }
                        for c in conflicts
                    ],
                )
            claim_id = uuid.uuid4().hex
            fd = os.open(
                claim_id + ".lease",
                os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                0o600,
                dir_fd=self.fd,
            )
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                retained = (
                    candidate
                    if candidate["kind"] == "native"
                    else {
                        key: value
                        for key, value in candidate.items()
                        if key
                        not in {
                            "snapshot",
                            "payload_files",
                            "distributions",
                            "preserve",
                        }
                    }
                )
                if candidate["kind"] == "filesystem":
                    retained["scopes"] = scopes
                claim = {
                    "schema_version": 1,
                    "claim_id": claim_id,
                    "operation_id": operation_id,
                    "operation_path": operation_path,
                    "candidate": retained,
                    "scopes": scopes,
                    "path_identities": identities,
                    "state": "admitted",
                    "writer_pid": os.getpid(),
                }
                self._write(claim_id + ".json", claim)
                return Lease(self, claim, fd)
            except BaseException:
                os.close(fd)
                raise

    def acquire_orphan(self, claim_id: str) -> Lease | None:
        if (
            not isinstance(claim_id, str)
            or len(claim_id) != 32
            or any(char not in "0123456789abcdef" for char in claim_id)
        ):
            raise CleanupError("custody_corrupt", "Invalid claim identity.")
        with self.admission():
            try:
                claim = self._read(claim_id + ".json")
            except FileNotFoundError:
                return None
            try:
                fd = os.open(claim_id + ".lease", os.O_RDWR | os.O_NOFOLLOW, dir_fd=self.fd)
            except OSError as exc:
                raise CleanupError(
                    "custody_corrupt", "Resource claim has no secure execution lease."
                ) from exc
            try:
                _private_file(fd)
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                os.close(fd)
                return None
            except BaseException:
                os.close(fd)
                raise
            return Lease(self, claim, fd)

    def claims(self) -> list[dict]:
        if self.fd is None:
            return []
        with self.admission():
            return self._claims()
