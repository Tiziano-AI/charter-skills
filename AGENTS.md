# Working on Charter Skills

This public repository distributes the skills-only `charter-skills` plugin for
Codex and Claude Code. The installable unit is `plugins/charter-skills/`.
Canonical skill content and the deterministic release builder belong to
Charter; this repository is not a second authored skill library.

## Source and qualification

Prepare releases through Charter's `docs/SKILLS_RELEASE.md`. Do not hand-edit
generated skills, native metadata, manifests, catalogues, guides or assets.
Repair their canonical owner, then export and qualify a new artifact. Preserve
licenses, third-party notices, declared resources and executable modes.

This root `AGENTS.md` is repository-owned maintenance guidance, not generated
release content. Preserve it beside an export; it does not enter the installed
plugin subtree. Keep private source, workstation paths, credentials and native
runtime captures out of this public repository.

Artifact parity, native installation, session loading and useful real work are
separate claims. Qualify the exact commit and report only what was observed;
a version string or release tag supplies no missing acceptance evidence.

## Release convention

Follow the shared [marketplace release
convention](https://github.com/Tiziano-AI/plugins/blob/main/AGENTS.md#release-convention).
Charter owns product qualification and this guide; the marketplace owner owns
catalog pins and plugin-home updates. Do not promote a later HEAD merely
because its manifest still names the published version.

Commit coherent changes locally. Each public push, tags included, needs
Tiziano's approval for the exact outgoing commits and tags. An earlier release
approval does not authorize another push. Keep English for source,
documentation and commit messages, and preserve other contributors' work.
