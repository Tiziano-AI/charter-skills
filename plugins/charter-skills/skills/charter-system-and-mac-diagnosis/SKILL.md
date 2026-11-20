---
name: charter-system-and-mac-diagnosis
description: Diagnose an unexplained slowdown, recurring system failure, or hot, swapping
  or power-hungry Mac, even on the first occurrence. Trace the failing request, queue,
  process or loaded model before a restart erases the evidence. Not disk cleanup or
  profiling an already localized code path.
metadata:
  content_version: charter-system-and-mac-diagnosis@2026.11.20.0
---
# Charter · System Failures & Mac Resource Diagnosis

What was supposed to finish, release memory or drain a queue, and what
happened instead? Follow one occurrence while the state that distinguishes
the explanations is still there. A restart can make both a stopped consumer
and a retry storm disappear; it cannot tell you which happened. Capture the
distinguishing evidence before suggesting an intervention that would erase
it. If service restoration takes priority, retain what you can without
delaying it and say what the loss prevents you from concluding. Diagnosis
alone does not authorize a restart, model unload, privileged probe or cleanup.

## A Mac is under strain now

Read [Mac resource triage](mac-resource-triage.md) when the first evidence is
heat, fan noise, sluggishness, swap, power draw, unexpected accelerator use
or a large process in Activity Monitor. Do not wait for a second incident.
While it is happening, pair the machine's pressure, compression, swap and
relevant CPU, accelerator or I/O activity with the process identity and a
short series of samples. Distinguish counters still increasing from earlier
high-water marks. A large footprint alone cannot tell whether the Mac is
under pressure, and swap left over after pressure subsides does not prove
it is still thrashing.

The process doing the work may not have requested it. Join the PID and
start time, active stacks, client or controller activity, and onset before
attributing the cost. On Apple silicon the CPU and GPU use unified memory:
do not add a separate VRAM estimate to the process footprint. A resident
model, a listening service and a model generating tokens are three different
things. For MLX, Ollama, LM Studio or llama.cpp, read [local model runtimes](references/local-model-runtimes.md)
before querying a service that might wake on contact. For filesystem
notification churn, read [the FSEvents branch](references/fsevents-branch.md)
before treating a dropped client as the producer. Use the [macOS observations](references/macos-observation-surfaces.md)
and, where installed, [macmon's metric definitions](references/macmon.md)
to choose a bounded read; a missing counter is not measured zero.

## A failure recurs, crosses owners or remains unexplained

Read [Systemic failure analysis](systemic-failure-analysis.md) before
choosing where to intervene. Compare one failed request with one successful
request by operation identity and order of events. Find the first transition
that matters to the outcome, not the loudest error downstream. For latency,
follow the chain that holds up completion and separate queue time from
service time. More workers do little if every worker waits on the same lock;
more retries can make an overloaded service slower.

When recovery will erase which client held the lease, how far a consumer
had drained its backlog, or which model was loaded, choose an
[observation that separates the explanations](references/investigation-workflow.md)
while it is still possible. Use [causal modeling](references/causal-modeling.md)
when transition order, ownership or a feedback loop determines the repair.
Choose the nearest owner that can both observe the relevant distinction and
control the consequential action. Draining a backlog may restore service;
it does not keep arrivals below the rate the consumer can sustain.

Return the supported cause, what could still change it, and distinguish
containment, recovery and prevention. A localized code defect needs its
local fix. A wrong binary or effective setting goes to
`charter-release-and-configuration-diagnosis` with the observed reader.
When a stream corrupts outcomes through framing, replay or terminal events,
take the event sequence to `charter-stream-protocol-repair`. If reclaiming
Mac disk space is requested, give `charter-macos-cleanup` the identified
candidate and its consumers; a full disk is evidence, not permission to
remove its contents.
