# macOS Observation Surfaces

Load this reference when the investigation needs concrete Activity Monitor,
CPU, GPU, memory, stack, log, volume, thermal, or privilege-aware probes. These
are patterns, not a fixed battery. Run only the probes that can separate the live
explanations.

## Machine and memory model

Establish the hardware branch before interpreting GPU memory:

```zsh
uname -m
sysctl -n hw.model
system_profiler SPHardwareDataType SPDisplaysDataType
```

Apple-silicon CPUs and GPUs share unified physical memory. Treat process
footprint, loaded-model state, system GPU activity, memory pressure, compression,
and swap as separate observations. Do not manufacture a per-process VRAM figure
from system GPU utilization or add it to RSS.

## Activity Monitor

Select **View > All Processes**, then capture relevant views rather than only the
hottest CPU row:

- process name and PID;
- `% CPU` (values above 100% can represent more than one logical core);
- Memory plus whether the row and Memory Pressure graph continue to grow;
- compressed memory, swap used, cached files, and the pressure color;
- GPU History when accelerator work is part of the question;
- Energy, Disk, and Network deltas when they can own the consequence;
- user, thread count, elapsed CPU time, and process state;
- related processes visible at the same time.

Open **Inspect** for process identity and open files or ports. Use **Sample
Process** only when the sample can identify the active subsystem. Keep the
timestamp of screenshots or notes: a later quiet state does not invalidate the
earlier high-water observation.

Activity Monitor and `sysmond` consume resources while observing. Do not mistake
their measurement cost for the original incident.

## System memory pressure

Read system consequence before blaming one large process:

```zsh
memory_pressure
vm_stat
sysctl vm.swapusage
top -l 1 -stats pid,command,cpu,mem,threads,time,state
```

Interpret the series, not one number:

- green/free pressure with a large idle process can be intentional residency;
- increasing compressed pages, swap use, pageouts, or yellow/red pressure shows
  machine-level contention;
- swap can remain allocated after the original pressure ends, so current free
  percentage and swap used describe different time horizons;
- wired and kernel memory are not normally recoverable by unloading a user
  model; file-backed or purgeable mappings behave differently from anonymous
  allocations.

Use `footprint` or `vmmap -summary` for a process only when their extra detail
changes the decision. They may be denied for root-owned or protected processes.

## GPU and ANE activity

On Apple silicon with macmon installed, prefer its bounded, unprivileged sampler
before a credentialed probe:

```zsh
macmon pipe -s 3 -i 1000 --soc-info
```

Read [macmon operations](macmon.md) for JSONL selection, active versus scaled
ratios, process-counter limitations, and commands that create load or persistent
services. Pair RAM/swap totals with the memory-pressure probes above. Macmon's
process table is TUI-only, not part of this JSON stream.

Activity Monitor GPU History is a useful system-level occurrence record, not
automatic per-process attribution. Check the installed `powermetrics --help`
for available samplers and process flags; hardware and macOS releases differ.
A bounded example, where supported, is:

```zsh
sudo powermetrics \
  --samplers tasks,gpu_power,ane_power,thermal \
  --show-process-gpu \
  --sample-rate 1000 \
  --sample-count 3
```

`sudo` is a credentialed boundary: obtain authorization before running it.
GPU/ANE power and utilization establish active accelerator work. Per-process GPU
time helps attribution but does not establish a process's unified-memory
allocation. `ioreg` accelerator statistics are a fallback discovery surface;
property names and meaning vary by hardware and macOS, so do not build the
verdict on an unlabeled counter.

## Process identity and short series

Use a variable name such as `proc_name`; in zsh, do not assign to the special
array `path`, because doing so changes executable lookup and can invalidate the
probe.

```zsh
proc_name=fseventsd
pgrep -x "$proc_name"
pid=533  # replace with the observed literal PID
ps -ww -p "$pid" -o pid=,ppid=,user=,%cpu=,%mem=,rss=,etime=,state=,command=
top -l 3 -s 2 -pid "$pid" -stats pid,command,cpu,mem,threads,time,state
```

If `pgrep` returns several PIDs, inspect each rather than choosing the first.
Repeat the `ps` or `top` observation after a short interval. Flat CPU with stable
high RSS and sleeping threads supports retained residue; increasing CPU time
supports active work.

For historical PIDs, current `ps` output is insufficient because a PID can be
reused. Correlate the log timestamp with process start time, executable path,
parent, launchd label, or another persisted identity surface.

## Process relationships and owned objects

```zsh
ps -axo pid=,ppid=,user=,lstart=,etime=,command=
lsof -nP -p "$pid"
launchctl print system/com.apple.fseventsd
```

Use the exact launchd domain and label for the target; do not guess a label from
the executable name. `lsof` may be partial for root-owned processes. Open files
show what the process has open, not necessarily what is consuming CPU.

Inspect child and client processes only when the daemon's protocol makes them a
plausible work owner. Record executable paths before short-lived processes exit.

## Stack and memory surfaces

A short sample is useful when the daemon is actively burning CPU:

```zsh
out_dir=$(mktemp -d /tmp/mac-resource-triage.XXXXXX)
sample "$pid" 5 1 -file "$out_dir/sample.txt"
```

This writes a temporary diagnostic file but does not modify the target process.
State where the output was written. Read the dominant stacks and thread names;
do not equate one symbol with the complete root cause.

`vmmap`, `footprint`, and targeted `spindump` can attribute retained memory or a
hot root-owned process, but macOS may deny them without privileges. A memory map
shows address-space and mapping categories; it does not mean every mapped model
byte is resident. `sudo` is a credentialed boundary even for read-only sampling:
obtain user authorization before using it. A denied sample leaves stack or heap
ownership unknown; it does not weaken measurements established elsewhere.

## Unified logs

Prefer the narrowest window that contains onset, sustained work, and recovery.
Use literal process names in predicates rather than interpolating untrusted text.

```zsh
/usr/bin/log show \
  --start '2026-08-19 12:18:00' \
  --end   '2026-08-19 12:24:00' \
  --style compact \
  --predicate 'process == "fseventsd"'
```

Use `--last 10m` only for a genuinely current incident whose onset is inside that
window. Add one suspected client or controller at a time. Look for event order
and multiplicity:

- client registration and teardown;
- dropped, replayed, retried, or timed-out work;
- volume mount, unmount, backup, snapshot, or cleanup transitions;
- the point CPU returned to idle.

Count repeated events by timestamp, thread, client, PID, root, or request ID when
that distinguishes one loop from replicated per-client work. Do not infer that a
repeated message is the expensive function until a stack or event sequence
connects it to the burn.

## Storage, backup, and filesystem context

Load these surfaces only for storage-related daemons or evidence pointing to a
volume, snapshot, backup, cache, or journal:

```zsh
df -h
mount
diskutil info '/Volumes/Example'
tmutil status
tmutil destinationinfo
```

Near-full volumes, mounted snapshots, a running backup, or purgeable-space scans
are conditions, not causal conclusions. Connect them to the onset through logs,
stacks, client timeouts, or a controlled before/after observation.

Tools such as `fs_usage`, `opensnoop`, `spindump`, and some volume or APFS
inspection commands may require privileges and can produce substantial output.
Use them only when their result changes the diagnosis or intervention.

## Thermal and energy context

Thermal pressure can cap performance and make low throughput coexist with high
resource use. Use Activity Monitor Energy and a bounded `powermetrics` thermal
sample when throttling changes the conclusion. Separate:

- high compute causing heat;
- thermal limiting reducing achieved CPU/GPU frequency;
- battery or power impact;
- a fanless or already heat-soaked machine amplifying an otherwise valid load.

Thermal state is an amplifier or consequence until timing connects it to the
incident; it is not a process owner.

## Measurement hygiene

- Keep every probe's timestamp and duration.
- Preserve failed-probe diagnostics; do not silently substitute missing output.
- Do not reuse invalid data after a shell error, broken pipe, permission denial,
  or observer that terminated early.
- Account for probes that create clients, watchers, or filesystem events of
  their own.
- Remove or stop a temporary watcher when its bounded observation ends; report
  its output path if retained.
