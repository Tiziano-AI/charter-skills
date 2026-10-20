# Callbacks, audio and UI publication

A framework object's role in a UI does not determine the execution context of
its callbacks. Separate the documented callback delivery contract, Swift's
actor isolation and the lifetime of the operation.

## Establish the actual contract

Read the selected SDK declaration or current framework documentation for the
specific callback. Queue, thread, executor and actor are related but not
interchangeable. A main-queue default is not permission to ignore the type's
concurrency annotations or a queue the application changed.

A closure created in actor-isolated code can inherit isolation depending on
its type and compiler rules. Make a nonisolated boundary explicit where an
external callback must run elsewhere; publish into UI isolation only where
state actually changes. Do not scatter detached tasks or unchecked isolation
assertions over a boundary you have not understood.

## Speech callbacks are not one family

The `SFSpeechRecognizer` contract distinguishes:

- `requestAuthorization(_:)`: delivery is not guaranteed on the main queue.
- Recognition task handlers and delegate methods: delivery uses the
  recognizer's `queue`, whose default is the application's main queue.
- The authorization handler does not use that recognition queue.

Permission handling and recognition results therefore need their own correct
boundaries. Resolve the declarations in the selected SDK's
`Speech.framework/Headers/SFSpeechRecognizer.h` rather than relying on a
versioned absolute path from another machine.

## Audio ingress and realtime constraints

`AVAudioNodeTapBlock` may run on a thread other than the main thread, as stated
in `AVAudioNode.h`. That establishes no UI-mutation guarantee; it does not by
itself specify every realtime scheduling or buffer-lifetime property.

For an audio callback, establish whether the particular path is realtime and
what processing or buffer retention the framework permits. Keep ingress
bounded. Avoid UI work, blocking waits, file or network I/O and unbounded
queues on a realtime path. If processing is transferred elsewhere, use an
appropriate bounded mechanism and preserve the buffer's valid lifetime.
Starting an unbounded task per audio buffer is not a concurrency design.

A speech tap can append or hand off audio to its processing request as allowed
by that API. UI transcription, errors and recording state are downstream
products, not work for the raw audio callback.

## Lifecycle and stale publication

Treat capture, processing and UI publication as different owners of state.
When recording stops or a session changes, a late callback may still arrive.
Associate results with the session or generation they belong to so an old
recognition result cannot overwrite the new draft.

Choose cancellation and teardown order from the framework: stop admitting
input, finish or cancel the processor as intended, remove callbacks or taps,
and release retained resources when their use has ended. Do not infer that a
closed window ended an audio operation.

Copy or isolate only what must cross the boundary. Keep actor-isolated view
state out of raw callbacks; keep callback-owned buffers out of UI models unless
their lifetime and transfer are valid. Test the actual start, stop, interruption
and late-result path when changing this seam.

## Official sources

- <https://developer.apple.com/documentation/speech/recognizing-speech-in-live-audio>
- <https://developer.apple.com/documentation/speech/sfspeechrecognizer/recognitiontask(with:resulthandler:)>
- <https://developer.apple.com/documentation/speech/sfspeechrecognizer/queue>
- <https://developer.apple.com/documentation/avfaudio/avaudionode>

The selected SDK headers supplement the web documentation for callback delivery
and imported types; compiler success alone does not establish realtime safety.
