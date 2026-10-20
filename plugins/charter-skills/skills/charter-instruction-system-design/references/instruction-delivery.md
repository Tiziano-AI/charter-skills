# How instructions reach the model

Use this when a rule exists in source but the behavior suggests the model
never had it, or had a different version of it. The target is the first edge
where the intended text and what the model read diverge, not a complete map of
the stack.

## Walk back from what the model read

Start from the occurrence: the session, process or request that behaved, and
what its input actually contained. Walk back only as far as the divergence.

- **Rendering.** A source file becomes a generated prompt, a projected skill or
  a merged configuration. A renderer, a manifest that does not list the file or
  a template that no longer includes the section can drop a rule.
- **Projection and installation.** The generated text has to land where the
  runtime reads it. A correct fragment in the wrong destination, a stale
  install or another copy earlier on a search path delivers something else.
- **Selection.** Runtimes decide which files a session sees. The project root,
  working directory, file being read and workspace trust can each affect
  selection. A guide loaded only while reading a subdirectory does not reach a
  task that never enters it. Inspect that runtime's actual selection rule and
  budget rather than borrowing another harness's behavior. A listed skill's
  body still has to be selected and loaded.
- **Capture.** Some inputs are read once when a session starts, others on every
  turn. A process-start snapshot and a per-turn read can disagree while both
  source files are current, and a resumed session can keep what it captured
  when it was created.
- **Truncation.** Listings and results are cut to budgets. A crowded skill
  catalog shortens descriptions to a prefix, so a clause past the cut never
  reaches the selector; oversized tool output and compacted history lose their
  tail or their detail.
- **Reading.** Linked depth reaches the model only when the model opens the
  link. Some models rarely follow references from an entrypoint, which leaves a
  rule kept only in a reference undelivered for them.

The operators along the way are replacement, append or prepend, ordered
concatenation, conditional inclusion, shallow or deep merge, projection,
normalization, truncation and deletion. Record message placement, selection
conditions and capture time only when they can change the disputed result.

## Read the assembled input, not the source

Source shows what should assemble under its conditions; only the assembled
input shows what an occurrence received. Depending on the runtime, instruction
load events, prompt snapshots or native session records may expose different
parts of it. Read the record's contract: a file-load event need not show the
complete assembled prompt, and a session's initial base need not include later
messages. A version marker shows that one layer is present, not that nothing
else was added.

For a complex stack, source → operator → receiver → capture point is a useful
compact map. Keep the complete selected sources reachable rather than copying
them into the account.

| Observation | Next owner to inspect |
| --- | --- |
| Relevant guidance cannot be found | Discovery, file placement or naming |
| Correct source, generated output lacks the rule | Renderer or manifest |
| Correct generated output, different destination | Installation or projection |
| Correct destination, session shows old text | Selection or capture point |
| Expected base plus unexpected instructions | Runtime-injected messages or a transition |
| Rule listed but cut from what the model saw | Truncation budget or card order |
| Rule kept in a reference the model never opened | Entrypoint content and link cues |
| Intended input, wrong behavior | The distinction itself, an interaction, or its application |
| Good compliance, poor result | The chosen behavior or the product premise |

## Repair at the layer that diverged

Which value a process actually read, and why it won, is an effective
configuration question that belongs to its actual reader and winning source;
configuration diagnosis is the specialist for that. A conflict between
delivered instructions is a question of meaning and belongs to the main
method. Rearranging messages so a locally preferred rule wins does not change
the runtime's authority.

The same meaning can need different delivery mechanics in different runtimes:
keep the meaning at one owner and the delivery seam local. Several generated
carriers are fine when their receivers require them; several editable copies
drift. A delivery repair is done when the rule arrives at the layer you
observed, which a fresh session's loaded input confirms.
