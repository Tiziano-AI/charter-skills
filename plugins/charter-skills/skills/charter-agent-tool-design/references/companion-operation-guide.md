# Companion Operation Guide

A CLI or MCP server needs a companion skill when safe, effective operation depends on domain
sequence or judgment that `--help` or a tool description should not carry. The guide teaches how to
use the product; it is not a duplicate API reference or a release history. Its value is in
explaining why one command is eligible now and another is not. If syntax and local help already
answer the job, a separate mandatory guide adds another versioned surface without adding operating
knowledge.

## What belongs in the guide

- the jobs for which the tool is the nearest operating surface;
- the first diagnostic or status command when setup state matters;
- how user-facing names, URLs, or current-directory context become stable IDs;
- the shortest read-only path to useful state;
- the normal mutation sequence, including preview when the product supports it;
- lifecycle interpretation: pending, complete, failed, retryable, canceled, partial, or stale;
- the command that reads an operation or changed object after mutation;
- common recovery branches that remain within the public commands or tools;
- when the raw escape hatch is appropriate and what it cannot safely infer;
- a few realistic, copyable sequences for frequent jobs.

Explain the dependencies in a sequence. Resolving a target before mutation
avoids ambiguity; reading an accepted operation before retry avoids duplicate
effects. An unconditional preflight tour does neither when the target and
effect state are already known. Include a contrasting branch where the normal
sequence should stop, resume or use an existing output instead of restarting.

Keep authentication guidance at the level callers need: supported source, profile selection, login
command, and diagnostic state. Leave machine-specific credential values and private workstation
recovery outside a portable package unless the product deliberately owns those paths.

## Relationship to the tool's own docs

`--help` and tool descriptions own syntax and immediate meaning. Product documentation owns the
complete command and configuration reference. The companion guide owns sequencing and judgment:
which command to run first, how to resolve identities, which state distinction matters, and how to
recover.

Link to deeper references instead of copying every flag, endpoint, enum, and JSON field. Examples
should use stable product vocabulary and should not depend on an author's personal directory,
account, or hidden setup. The package form of the guide (card, references, metadata) is
`charter-skill-package-design`'s subject.

## Keep it current

Exercise the documented sequences against the same command grammar shipped by the product. Remove
superseded routes rather than leaving two “recommended” workflows. If the tool changes its identity,
configuration, mutation, or recovery model, update the guide at the same semantic owner boundary.

The guide has earned its place when an unfamiliar agent can move from user intent to the correct
public commands or tools without improvising provider requests or reading source code.
