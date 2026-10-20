
# Charter · Mac Resource Triage

## Recognition

Use this skill when the Mac is hot, slow, swapping, draining power, or showing
unexpected CPU, GPU, ANE, memory, disk, or network use and the user needs the
real owner. The visible process may be the worker, a broker, a model host, a UI
helper, or the victim of a slow client. The skill owns the machine-level
investigation from resource anomaly to an evidence-bounded mechanism and
intervention.

Use a product-specific skill after the process, runtime, or application has been
identified and its own control surface owns the next action. Use an application
profiler when source code and the hot code path are already known. Use
`charter-systemic-failure-analysis` after the macOS occurrence has been localized and the
remaining job is to redesign a distributed recurrence mechanism.

## First move

Capture the machine envelope before changing it: architecture, CPU load, GPU or
ANE activity when relevant, memory pressure, compressed memory, swap, thermal
state, and I/O. Then record the exact process identity, PID, owner, CPU, resident
or physical footprint, elapsed time, thread count, and at least one later sample,
plus the user's last relevant action and the onset window.

On Apple silicon, CPU and GPU draw from unified memory. Do not invent a separate
VRAM total or add a supposed GPU-memory number to process memory. First decide
whether the machine is under pressure; then attribute resident models and active
accelerator work separately.

When installed, use macmon as the terminal-first Apple-silicon observer: its TUI
for interactive inspection, bounded `macmon pipe -s 3 --soc-info` for agent-readable
machine samples. Read [macmon operations and metric semantics](references/macmon.md)
before interpreting its percentages, process attribution, or advanced modes.
Keep active residency separate from frequency-scaled utilization. Its JSON does
not contain the process table or memory pressure; pair it with process identity,
`memory_pressure`, `vm_stat`, and swap evidence. A zero GPU/process-power reading
can mean missing data, not no work. Sampling does not require starting its HTTP
server, installing a service, or generating a stress load.

If the load has cooled, preserve the high-water observation and distinguish
retained memory, loaded-but-idle models, delayed cleanup, swap left from earlier
pressure, and still-active work. Do not begin by blaming the most recent model
load, cleanup, backup, mount, install, or file operation. Treat it as a candidate
event until process, runtime, and timing connect it to the consequence.

## Causal model

Keep these roles separate:

```text
visible resource holder
  <- active work, resident state, or backlog
  <- client, producer, or controller
  <- onset trigger
  <- amplifier or threshold condition
  <- recurrence owner
```

- **Holder is not owner.** A daemon can drain client work; a helper can expose an
  app's GPU use; a Python host can retain MLX weights selected by another
  controller. A dropped client can itself be collateral damage.
- **Loaded is not generating.** A model may occupy unified memory with no active
  tokens, GPU work, or CPU burn. A listening server may have no model loaded.
- **Burn is not residue.** CPU-time or accelerator-time growth means active work;
  high footprint with flat compute can be a deliberately loaded model or
  allocation residue after work ended.
- **RSS is not system pressure.** Compression, swap, wired memory, shared mappings,
  purgeable pages, and memory pressure determine machine consequence. One
  process's RSS does not equal the memory the system can immediately recover.
- **GPU activity is not GPU memory.** System GPU utilization and per-process GPU
  time can establish work; they do not automatically quantify a process's
  unified-memory allocation.
- **Current rate is not historical backlog.** Low current filesystem or network
  activity does not exclude replay, recovery, per-client drain, or queued work.
- **Trigger is not amplifier.** Disk pressure, snapshots, backup maintenance,
  and cleanup tools can make an incident more likely without owning the loop.
- **A log phrase is not a mechanism.** Repeated messages can mark repeated
  client creation or instrumentation rather than corruption inside the daemon.
- **PID identity expires.** Correlate a historical PID with executable, start
  time, parent, and log timestamp before naming its owner.

## Investigation

### Establish the machine envelope

Start with a short CLI series, using macmon where available for Apple-silicon
CPU/GPU/ANE metrics. Add Activity Monitor's CPU, Memory, Energy, Disk, Network,
or GPU History views when their pressure graph, history, or process relationships
would distinguish the live explanations. Record memory pressure, compressed
memory, and swap before interpreting a large process row.

Activity Monitor supplies the user's high-water state and process relationships;
CLI samples show which counters are still moving. Activity Monitor, `sysmond`,
`top`, sampling, and custom probes add some measurement load.

Read [macOS observation surfaces](references/macos-observation-surfaces.md) when
you need command patterns for CPU, GPU, memory pressure, swap, thermal state,
Activity Monitor fields, privilege boundaries, or process and log correlation.

### Identify the holder and lifecycle owner

Inspect only surfaces that can separate live explanations:

- thread samples or stack summaries for the active code path;
- memory pressure, physical footprint, mappings, and loaded model files for
  resident state;
- system GPU/ANE activity and per-process accelerator time for active compute;
- open files, sockets, volumes, snapshots, and controller state for the work
  domain;
- process parents, children, clients, and executable paths for ownership;
- unified logs constrained to the onset and recovery windows;
- client-add, drop, timeout, replay, retry, or teardown events that explain
  multiplicity and persistence.

For MLX, Ollama, LM Studio, llama.cpp, or another local inference runtime, read
[the local-model branch](references/local-model-runtimes.md) before using vendor
status commands or unloading anything. A UI process, service, runner, loaded
model, and active inference are separate states. Some apparently observational
commands can wake a sleeping service.

For system services, start with the daemon's own logs, then add a suspected
client or controller only when their event order could change the diagnosis.
Avoid broad all-day log dumps: they make temporal correlation weaker and can
themselves be expensive.

### Use one discriminating observation at a time

Choose the next observation from the explanations still alive. Examples:

- sample CPU time, GPU time, footprint, pressure, and swap over time to separate
  active compute, a resident idle model, retained residue, and system harm;
- compare a runtime's process tree, listening service, loaded-model registry, and
  request activity to separate service presence from inference;
- compare current input rate with daemon work to separate live production from
  historical drain;
- correlate repeated work blocks with client registrations to test per-client
  replication;
- observe whether a fresh client inherits a degraded marker to distinguish a
  global daemon state from one slow consumer;
- temporarily quiet a suspected producer only with the user's authorization,
  and only when the before/after result would change the repair.

For `fseventsd`, `deleted`, `backupd`, watcher churn, or FSEvents drop/rescan
signals, read [the FSEvents branch](references/fsevents-branch.md) before creating
a custom stream or interpreting the dropped client as the producer.

### Stop at the actionable recurrence owner

Climb from symptom to mechanism to trigger and recurrence condition only while
the next layer changes the intervention. Separate:

1. **Containment** — reduce current compute, requests, I/O, or thermal load.
2. **Recovery** — unload a model, release retained state, or return the service
   to a clean run.
3. **Structural repair** — change model lifecycle, client, watcher, controller,
   limits, or contract that recreates the overload.

A restart can prove that state was retained and can recover the machine, but it
does not prove the recurrence was fixed.

## Intervention boundary

Remain read-only with respect to live processes, model state, services, and
storage until the diagnosis supports an intervention and the user authorizes it.
Do not unload a model, stop inference, kill or restart a process or daemon, wake
or stop a model service, close an application, unmount a volume, delete or
rebuild a journal, purge snapshots, disable backup, or run a credentialed `sudo`
probe without that authority. Preserve the onset evidence before any action that
would erase it.

When a read-only probe is denied, report what that missing layer would establish
instead of treating denial as proof. Prefer a narrower live observation over a
privileged diagnostic when both would make the same decision.

## Return

Lead with the verdict and keep proof layers explicit:

- **Machine envelope:** CPU, GPU or ANE, memory pressure, compression, swap,
  thermal state, and I/O at the relevant time.
- **Observed owners:** process, service, helper, runtime, loaded model, client,
  controller, and event order established directly.
- **Strongly supported:** the mechanism that best explains the observations and
  predicts the recovery pattern.
- **Not established:** unknowns that would change the structural repair.
- **Recurrence condition:** what combination makes the incident return.
- **Intervention:** containment, model or state recovery, and structural fix,
  kept distinct.
- **Effects:** every model, process, service, volume, or journal mutation
  actually made; say explicitly when none were made.

Return control when the user can decide whether to contain, recover, escalate,
or repair the real owner, and the remaining unknowns no longer change that next
move.
