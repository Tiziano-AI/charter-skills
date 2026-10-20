# Local Model Runtimes

Load this reference when MLX, Ollama, LM Studio, llama.cpp, a Python model host,
or another local inference runtime may own CPU, GPU, ANE, or unified memory.

## State model

Keep these states separate:

```text
UI installed or open
  != background service listening
  != runner process present
  != model weights resident
  != inference request active
  != GPU or ANE work active
```

A service can listen with no loaded model. A model can remain resident and idle.
A UI GPU helper can exist without inference. A Python process can run MLX under
a generic executable name. Closing a window may leave its server and model alive.

On Apple silicon, model weights, KV cache, runtime allocations, CPU work, and GPU
work contend for unified memory. Diagnose system pressure and active compute
separately; do not search for a separate VRAM pool.

## No-wake discovery first

Start from operating-system state so observation does not launch a runtime:

```zsh
ps -axo pid=,ppid=,user=,%cpu=,rss=,etime=,state=,command= \
  | rg -i 'ollama|lm studio|llmster|mlx|llama|gguf|safetensors|metal'
lsof -nP -iTCP -sTCP:LISTEN \
  | rg -i 'ollama|lm studio|llmster|python|llama'
```

For a candidate PID, inspect its full command, children, listening ports, and
open model files:

```zsh
pid=1234  # replace with the observed literal PID
ps -ww -p "$pid" -o pid=,ppid=,user=,%cpu=,%mem=,rss=,etime=,state=,command=
pgrep -P "$pid" -fl .
lsof -nP -p "$pid" | rg -i 'models|\.gguf|\.safetensors|\.mlx|tokenizer|config\.json'
```

Open weights support model identity but do not prove all mapped bytes are
resident or that inference is active. Use footprint, pressure, GPU time, request
logs, or the runtime's already-running status surface for those claims.

## Ollama

An Ollama app/service or listener on port `11434` is not evidence of an active
model. When the service is already reachable, use independent surfaces:

```zsh
ollama ps
curl --silent --show-error http://127.0.0.1:11434/api/ps
ollama_serve_pid=2011  # replace with the observed literal service PID
pgrep -P "$ollama_serve_pid" -fl .
```

`ollama ps` and `/api/ps` identify models retained by the current runtime;
process CPU/GPU series and request activity distinguish residency from
inference. Do not kill `ollama serve` merely because the port is listening. If
the user wants memory released, unload or stop the exact model through Ollama's
current public surface and verify the model registry, runner tree, pressure, and
swap afterward.

## LM Studio

Check the process tree before calling `lms`:

- `/Applications/LM Studio.app/... --run-as-service` means the service app is
  present, not that a model is loaded;
- Electron `Helper (GPU)` is UI infrastructure and does not prove inference;
- a model runner, runtime log, loaded-model registry, or open weight files are
  stronger model-residency evidence.

On the locally observed LM Studio CLI, `lms ps` **wakes LM Studio when its service
is asleep**. It is therefore not a no-effect status command. Run it only when
the service is already present or the user authorizes waking it. If already
running, `lms ps` can distinguish loaded models from an empty service.

`lms unload` changes model state, `lms daemon down` changes the daemon lifecycle,
and quitting LM Studio changes the application lifecycle. Choose the narrowest
effect that matches the user's goal and verify it; do not treat them as
interchangeable cleanup commands.

## MLX and Python-hosted inference

MLX may appear as `python`, `uv`, a product CLI, `python -m mlx_lm.server`, or an
application-owned worker rather than a process named `mlx`. Use the full command
line, parent process, current directory when available, open model files,
listening ports, and product logs to identify the owner.

Distinguish:

- model load or compilation;
- active prompt or generation;
- resident weights and KV cache after generation;
- a serialized worker waiting for the next request;
- a wedged or abandoned process whose controller is gone.

GPU History or `powermetrics --show-process-gpu` can establish active GPU time;
process footprint and system pressure establish memory consequence. Neither
surface alone establishes the model name, so join them through PID, command,
open weights, runtime logs, or product-owned state.

## Intervention and verification

Before unloading or terminating anything, preserve:

- exact PID and parent/controller;
- model identity and runtime;
- whether inference is active;
- memory pressure, compression, and swap;
- CPU/GPU/ANE activity;
- listening endpoints and dependent clients.

Prefer unloading one idle model over stopping its service, and stopping one
orphaned runner over quitting an unrelated UI. After the authorized action,
verify the owning surface: loaded-model registry, process tree, open weights,
memory pressure, footprint, GPU time, and any client error. A falling RSS or
free-memory increase does not by itself prove swap has been reclaimed or the
runtime will not reload the model on the next request.
