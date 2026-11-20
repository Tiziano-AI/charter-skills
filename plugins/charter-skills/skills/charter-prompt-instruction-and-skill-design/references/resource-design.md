# Resource design and assembly

## Knowledge determines the container

A recurring job may depend on causal relationships, craft judgments, exact
constraints or repetitive operations. These imply different resources.

Judgment-heavy work benefits from a domain model and contrasting cases because
the right action varies with conditions. A template helps when an artifact has
stable semantic structure but should leave meaningful choices open. A script
helps when manual execution is brittle or repetitive and its inputs, outputs,
effects and failure behavior can be explicit.

A reference is useful when it answers a recognizable subproblem. An asset is
useful when it serves an output or interface. Unused scaffolding is not spare
capability: an empty `scripts/` or a placeholder template creates a plausible
route to irrelevant work. Many resources are coherent when different tasks
need different depths; file count and length do not define the boundary.

## Redesigning a package that already exists

Read the complete existing resource set before redesigning. A rich reference or
a correct script can survive a wholesale rewrite of the entrypoint, and a
script need not change because the teaching around it changes. Reading only
the entrypoint tends to preserve the easiest visible prose while losing expert
substance hidden in a reference. Conversely, keeping historical file
boundaries can leave three partial explanations where one coherent resource is
needed.

Retaining, enriching, merging, moving and retiring are all legitimate resource
decisions. Comparing the user's job, the likely first action and the payoff
with those of neighboring packages exposes the real boundary. A model upgrade
can make a prescribed sequence unnecessary while leaving specialist depth
valuable; that does not by itself mean a smaller package.

## Packaging mechanics that break delivery

Some packaging defects stop expertise from arriving at all: malformed YAML can
make a loader skip the skill, a broken relative link hides a reference, a file
missing from the package's inventory or install list is never shipped, and a
script that loses its executable bit or depends on an undeclared tool fails
when it is needed. After editing, parse the changed frontmatter and metadata,
resolve the changed links, and run a changed script on small cases, because
its behavior changed and not only its wording.

Generated caches, build outputs and operating-system metadata files are not
package resources. When redesigning, replace only the files the package owns
so adjacent work survives.

## Visual resources have a consumer

An icon can aid recognition, a reference image can teach craft, and a template
can accelerate an artifact. Their value depends on the actual use, not on
decorative presence.

For production knowledge, connect an inspectable source to a visible result
and show a consequential adaptation: changing proportion rather than merely
recoloring a model, or recomposing a layout rather than shrinking it. Explain
which relationship survives the change and which must be rebuilt. A finished
asset can teach form or material treatment without carrying its construction
history; label that limit instead of inventing one. Authoring the example
does not make it a positive standard: inspect the result at its intended use,
and revise or omit it if it does not teach the claimed distinction.

Keep only the files needed to use that resource, with dependencies, source
rights and modifications visible. Distinguish originals from adaptations,
and link each resource to the subproblem it serves rather than asking every
task to ingest the collection.

Canonical relative paths make them reachable, and provenance keeps their
origin intelligible. Type, dimensions and rendering at the intended size matter
where a consumer imposes them: an image that is legible full-screen can fail as
a small recognition icon. A package with no visual need is complete without
visual resources.
