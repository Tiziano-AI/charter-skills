# Rendered stills and films

Render time is the budget of a rendered piece: it sets how many times you can
see the whole of it before the final render.

- From the first render in the kind of process the final will use, make the
  renderer report the device each stage ran on, denoising included. Fallbacks
  can be silent and a default log may name no device, so raise its logging
  and confirm that the device lines actually appear; a filter that matches
  nothing proves nothing. Device preferences need not travel with the scene
  file into another process, a stage such as denoising can stay on the CPU
  unless enabled, and one stage on the CPU can multiply the budget.
  In Blender's Cycles on Metal (checked on 5.2), a headless process that
  renders must itself call `refresh_devices()` on the add-on's preferences,
  which startup does not do, keep the Metal entry's `use` on and set
  `scene.cycles.device = 'GPU'`; final-render denoising stays on the CPU until
  `scene.cycles.denoising_use_gpu` is on. `-- --cycles-device METAL` moves path
  tracing only. Confirm with `--debug-cycles`, at the report's "Path tracing
  on" and "Denoising on" lines.
- Measure seconds per frame on the hardest shot, at the samples and
  resolution you intend for the final, as soon as it has its final materials
  and light: time several consecutive frames in that same kind of process,
  apart from one-off start-up. Do this before
  committing samples and resolution and before promising frame rate and
  length; when the person's own numbers do not fit, show them the
  measurement.
- Before the long render, push a short span through the whole chain (render,
  master, grade, encode) and check the decoded file as
  `charter-visual-asset-production` describes for derivation. Choose a span
  with the darkest gradient, a fade and the fastest motion. A setting whose
  output is identical with it switched off is doing nothing.
- A background Blender script that raises still exits 0 unless the run passes
  `--python-exit-code 1`, so without it shell success says nothing about the
  script. A first Cycles render on Metal can go quiet while it compiles its
  kernels, so low renderer CPU and a silent log do not show a hang. Sample the
  renderer's threads and the system's `MTLCompilerService` before killing the
  run.
- Render into durable storage in units a restart can skip once complete. A
  unit counts as complete only when it reads back whole, or was written under
  a temporary name and renamed when finished; the presence of a file does not
  prove it, and a renderer's own skip-existing option may not check.
- When exposure or grade may still change after rendering, keep a scene-linear
  master in a floating-point format, so values above display white survive,
  and finish it through the same view transform you judged the look in.
  Written linear, an integer file clips those values; written through the
  display transform, it bakes the tone curve, and at 8 bits its steps too.
  An integer file carries them only through an encoding that maps the range
  above white into its code values, such as a log curve, PQ or a stated
  linear scale, at a bit depth whose steps stay invisible after the grade,
  and the grade must decode that same mapping.
- Sampling noise moves differently from the scene. With a fixed seed it stays
  put on the screen while the scene slides under it; with an animated seed it
  boils; a per-frame denoiser turns either into shifting blotches. Where the
  camera is locked, a fixed seed keeps still areas that see no moving part
  identical before denoising, though a denoiser or adaptive sampler that looks
  at neighbouring pixels can still carry change in from a nearby moving part.
  Render one frame with two seeds, denoised as the final will be: the
  difference shows how much the noise will change wherever the image under it
  changes, which with an animated seed or a moving camera is everywhere.
  Where it shows at playback size, the remedy is
  more samples or a lower noise threshold, the same every frame, which a time
  cap does not keep.
- A repeated feature such as gear teeth, spokes or a hex socket that moves more
  than half its spacing per frame appears to stand still, run slow or reverse,
  and it judders well before that. Motion blur hides this only once the
  shutter smears each feature across a full repeat; between those rates it
  strobes even when blurred; a high-contrast feature keeps a faint drift
  beyond a full repeat, fading only slowly as the smear lengthens; and an
  eased spin-up or stop passes through that band.
  Check peak rates, not averages.
- When you cannot watch the motion, measure the scene as the renderer
  evaluates it, frame by frame, rather than the curves you authored: the
  on-screen speed in pixels per frame of each moving part, and of the subject
  and background as the camera move sweeps them across the frame (too fast
  reads as debris, too slow as nothing); each repeated feature's peak step
  against its spacing; and evaluated positions against their intended values,
  which exposes jitter a still hides. The motion section of
  `charter-visual-asset-production` covers the decoded file and when motion
  counts as watched.
