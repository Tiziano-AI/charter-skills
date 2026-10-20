# Macmon operations and metric semantics

Use macmon for terminal inspection and bounded Apple-silicon machine samples.
It complements process identity, pressure, stacks, and runtime state; it does
not replace them. The commands and metric contracts below describe **macmon
0.10.0** and its [official source](https://github.com/vladkens/macmon/tree/v0.10.0).
Recheck installed `--version` and subcommand `--help` after an upgrade;
do not assume current `main` describes the installed release.

## Interactive investigation

Run `macmon`; `?` shows the installed key map. Useful operations:

| Key | Use and consequence |
| --- | --- |
| `/`, Enter, Esc | Filter by case-insensitive name/PID substring, keep filter, clear filter/selection |
| `s`, `S`, header click | Next sort column, reverse order, select column |
| arrows, `i` | Select process; inspect executable, cwd, open files and sockets |
| `/` inside `i` | Filter descriptor type/path, e.g. `tcp`, `cwd`, or a file path |
| `r` | Switch CPU/GPU panels between frequency-scaled and raw active residency |
| `v` | Switch graph/gauge presentation |
| `p` | Hide/show processes; hiding also stops the process sampler |
| `+`, `-` | Change sampling interval |
| `q` | Leave the info overlay; on the main screen, exit |

Filters support positive terms separated by commas (OR) and `!term` exclusions:
`python, !helper`. A PID filter is not exact identity: `123` also finds `1234`.
Per-term totals can overlap; do not sum them. Confirm the actual PID and executable
before attributing work. `TIME` is cumulative user+system CPU time, not process age.

`i` shows readable descriptors, not guaranteed complete files/ports or I/O rates.
Closed/unreadable descriptors can be absent; device/pipe/kqueue counts need not
have corresponding rows. Access to other users can be denied.

`e` reveals a process/file in Finder; `c` copies its path to the clipboard.
Neither is needed for passive sampling. `k` opens a kill dialog whose default
Enter action is SIGTERM; force kill sends SIGKILL. Do not use it without authority
for that exact intervention. **`c` is not a per-core-view toggle.**

### Preserve the user's presentation

The TUI reads `~/.config/macmon.json` (from `HOME`, not `XDG_CONFIG_HOME`). Opening,
help, filtering, selection, info, and exiting do not save it. View, ratio mode,
process visibility, interval, and sort changes save immediately. Unknown fields
are discarded on a later save. An `-i` TUI launch override is run-only; `+/-`
replaces it and saves the new interval. Avoid changing these during an agent's
inspection unless requested; a separate terminal does not isolate this config.

Sources: [keys](https://github.com/vladkens/macmon/blob/v0.10.0/src/app/tui/help.rs),
[process view](https://github.com/vladkens/macmon/blob/v0.10.0/src/app/tui/proc_view.rs),
[config](https://github.com/vladkens/macmon/blob/v0.10.0/src/app/config.rs),
[descriptor reader](https://github.com/vladkens/macmon/blob/v0.10.0/src/app/fds.rs).

## Bounded machine samples for agents

```zsh
macmon --version
macmon pipe --help
macmon pipe -s 3 -i 1000 --soc-info | jq -c '{
  timestamp,
  cpu_active_pct: (.cpu_active_ratio * 100),
  cpu_scaled_pct: (.cpu_scaled_ratio * 100),
  gpu_active_pct: (.gpu_active_ratio * 100),
  gpu_scaled_pct: (.gpu_scaled_ratio * 100),
  cpu_w: .cpu_power, gpu_w: .gpu_power, ane_w: .ane_power,
  components_w: .all_power, system_w: .sys_power,
  memory, temp, fans
}'
```

`pipe` emits one JSON object per line; `-s 0` (the default) never stops on its own.
Keep a finite sample count and inspect stderr/exit status. Use `cpu_tiers` for
cluster/core detail; `--soc-info` adds hardware identity. Exported JSON contains
system/SoC metrics, **not the TUI process table or descriptor overlay**. Use
`ps`, `top`, `lsof`, and the owning runtime for those questions, not an invented
`processes` JSON field.

### Interpret the numbers before naming a culprit

- `*_active_ratio`: active residency over the sample. `*_scaled_ratio`: activity
  weighted by frequency relative to maximum. Both are fractions 0–1, not
  percentages; CPU totals are weighted by core count. A low scaled GPU ratio can
  coexist with higher residency at a low clock. The deprecated `cpu_usage_pct`
  is also a 0–1 scaled ratio despite its name; prefer explicit ratio fields.
- Process CPU 100% represents one fully occupied core and can exceed 100%; it
  is not on the same scale as the combined machine percentage. Process MEM is
  physical footprint for the current user but RSS via `ps` for other users.
- Process POWER comes from energy-counter deltas. `-` is unavailable, not zero;
  `≥` on a filter total means some energy values are missing. It is not a complete
  allocation of whole-machine watts.
- Process GPU% is Apple GPU-client accumulated-time delta divided by elapsed
  time, capped at 100%. Missing/backward counters and a new baseline produce zero.
  It does not redistribute system GPU utilization among processes. Do not equate
  those rows with the frequency-scaled GPU panel, require them to sum to it, or
  treat zero as proof of inactivity. Correlate disputed MLX/helper attribution
  with the actual worker and the same active interval; use Instruments Metal
  System Trace if exact ownership remains consequential. Macmon is not a proven
  cure for incorrect Apple process counters.
- Memory fields are bytes for RAM and swap usage/totals, not memory pressure,
  compression, pageout rate, or separate VRAM. Pair with `memory_pressure`,
  `vm_stat`, and `sysctl vm.swapusage` before diagnosing contention.
- Power is watts; `all_power` sums CPU+GPU+ANE, **not the whole machine**.
  `sys_power` is a separate system-power reading. Temperature is Celsius and may
  be null when no valid sensor exists; a VM can expose zero/unavailable hardware
  metrics. On macOS 27, CPU/ANE zero can mean unsupported private CLPC mappings.
  Running as root does not grant Apple's private energy-reporting entitlement.

Sources: [metrics model](https://github.com/vladkens/macmon/blob/v0.10.0/src/metrics.rs),
[process collection](https://github.com/vladkens/macmon/blob/v0.10.0/src/app/procs.rs),
[pipe implementation](https://github.com/vladkens/macmon/blob/v0.10.0/src/app/main.rs),
[CLPC limitations](https://github.com/vladkens/macmon/blob/v0.10.0/docs/clpc-discovery.md).

## Advanced capabilities are separate effects

- `serve` exposes `/json` and `/metrics` (Prometheus); default **0.0.0.0:9090**,
  plain HTTP with no authentication. A deliberately local server must use
  `macmon serve --host 127.0.0.1`. Do not start it for ordinary observation or
  expose it through a tunnel. There is no built-in historical store.
- HTTP `/json` timestamps serialization at request time; sampling errors can
  retain the last good metrics. A recent timestamp alone does not prove fresh
  sampling. Prefer bounded `pipe` for incident evidence.
- `serve --install` installs and starts
  `~/Library/LaunchAgents/com.macmon.plist`, with login startup and KeepAlive;
  `serve --uninstall` stops/removes that service. Both require authority for the
  persistent service change. The generated plist preserves host/port, not `-i`.
- `stress` generates CPU pulse, CPU, GPU, ANE, or all three loads. The installed
  `stress --help` is more accurate than the tag README's older CPU/GPU-only
  description of `all`. Without `--duration` it continues until interrupted.
  `find-clpc` also generates CPU/GPU/ANE loads; it is not passive discovery.
  Its `--powermetrics` adds a credentialed reference probe. Neither command is a
  prerequisite for using macmon or diagnosing an existing workload.

Source: [HTTP/service implementation](https://github.com/vladkens/macmon/blob/v0.10.0/src/app/serve.rs),
[sampling cache](https://github.com/vladkens/macmon/blob/v0.10.0/src/app/main.rs),
[CLPC discovery](https://github.com/vladkens/macmon/blob/v0.10.0/src/app/find_clpc.rs).
