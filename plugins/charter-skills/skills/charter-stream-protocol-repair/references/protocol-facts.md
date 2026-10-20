# Protocol Facts That Decide Outcomes

Each section states the transport's own rules for framing, ending, errors and
resumption, with the source they come from. These are the rules that decide
what a close, an end of input or an error event means; a design that
contradicts one of them is wrong however consistent it looks.

## Server-sent events

Source: WHATWG HTML Living Standard, section 9.2 "Server-sent events"
(<https://html.spec.whatwg.org/multipage/server-sent-events.html>).

- **Framing.** The stream is always UTF-8. Lines end with CRLF, LF or CR. A
  blank line dispatches the pending event. A line starting with `:` is a
  comment, commonly sent as a keepalive. Successive `data:` lines are joined
  with LF, and one space after the colon is stripped.
- **End of input.** At end of file, a pending event not yet terminated by a
  blank line is discarded. A server that writes its final event and closes
  without the trailing blank line loses that event.
- **Events without data.** EventSource does not dispatch an event whose data
  buffer is empty: `event: done` with no `data:` line never fires, while
  `data:` with an empty value does. Parsers outside the browser decide this
  themselves, so a terminal event should carry a `data:` line.
- **Automatic reconnect.** EventSource reconnects both after a network error
  and after the response body ends normally, firing `error` with `readyState`
  CONNECTING each time. It stops when the page calls `close()`, when the fetch
  is aborted, or when a response is not status 200 with content type
  `text/event-stream`; a 204 No Content therefore stops reconnection. A server
  that finishes an operation and closes the body receives a new request for the
  same URL after the reconnection delay, and if that endpoint starts work, the
  operation runs again. The client should close on the terminal event, and the
  server can answer a reconnect for finished work with 204.
- **Resume.** An `id:` field sets the last event ID, which persists across later
  events that carry no `id`; an empty `id:` clears it. On reconnect a nonempty
  last event ID is sent as the `Last-Event-ID` request header. The server has to
  map that value to a resume point; the header by itself replays nothing.
- **Retry.** A `retry:` field consisting only of ASCII digits sets the
  reconnection delay in milliseconds; any other value is ignored. The initial
  delay is implementation-defined.
- **EventSource is GET-only.** Its constructor takes a URL and a credentials
  flag, with no method or body. Streams opened by POST, as most LLM APIs are,
  are read with `fetch` and a stream parser: there is no automatic reconnect,
  and the parser may or may not follow the rules above.

## WebSocket

Sources: RFC 6455 "The WebSocket Protocol"
(<https://www.rfc-editor.org/rfc/rfc6455>), sections 5.5, 7.1.5, 7.4 and 8.1;
WHATWG WebSockets Standard (<https://websockets.spec.whatwg.org/>).

- **Close frame.** It carries an optional 2-byte status code followed by a
  UTF-8 reason. Control frames carry at most 125 bytes of payload, so the reason
  is at most 123 bytes. The browser's `close(code, reason)` throws
  `InvalidAccessError` unless the code is 1000 or in 3000–4999, and
  `SyntaxError` if the encoded reason exceeds 123 bytes.
- **Codes that are never on the wire.** 1005 (no status code was present),
  1006 (closed abnormally, without a Close frame sent or received) and 1015
  (TLS handshake failure) must not be sent in a Close frame. They exist for a
  local API to report what happened. A 1006 means no closing handshake was
  observed, from a dropped connection, a killed process or a proxy cutting the
  link; it is never a code the peer chose. In a browser, 1006 also covers every
  failure to connect (DNS, refused connection, TLS, a server that is not a
  WebSocket server) and 1015 is never reported; whether `open` fired tells a
  failed connection from a dropped one.
- **Code ranges.** 1000–2999 belong to the protocol and its extensions;
  3000–3999 are registered with IANA for libraries, frameworks and
  applications; 4000–4999 are private, by agreement between the applications.
  An application outcome carried in a close code belongs in 4000–4999 or a
  registered 3000-range code, with its meaning defined by the application.
- **Closing handshake.** After sending Close, an endpoint sends no more data
  frames; on receiving Close without having sent one, it replies with Close.
  Messages can still arrive after you send Close, until the peer's Close
  arrives. When both sides close at once, each sees the other's code, so the
  two endpoints can record different close codes.
- **Text messages.** A text message must be valid UTF-8 as a whole, but a
  single frame may end in the middle of a code point; validate after
  reassembly. Invalid UTF-8 fails the connection, and 1007 is the code for data
  inconsistent with the message type.
- **Heartbeat.** A Pong must echo the Ping's payload; an unsolicited Pong is a
  one-way heartbeat. The browser API exposes neither Ping nor Pong, so a
  browser client that needs liveness uses application-level messages.
- **Backpressure.** The browser's `send()` never blocks. Queued bytes show in
  `bufferedAmount`, and when the user agent cannot buffer more it closes the
  connection. A producer that ignores `bufferedAmount` grows memory and can
  lose the connection.

## LLM provider streams

Sources: Anthropic, "Streaming messages"
(<https://platform.claude.com/docs/en/build-with-claude/streaming>); OpenAI,
"Streaming API responses"
(<https://developers.openai.com/api/docs/guides/streaming-responses>),
"Background mode" (<https://developers.openai.com/api/docs/guides/background>)
and "Function calling", streaming section
(<https://developers.openai.com/api/docs/guides/function-calling>); the
`openai` Python SDK, `openai/_streaming.py`.

Provider event names illustrate distinct outcomes; they are not a support
matrix for every model, transport or SDK. Resolve the applicable API contract
and the adopted SDK's event dispatch before relying on a particular mapping.

- **HTTP 200 is not success.** Once the status line is sent, later failures can
  only arrive in the stream. Anthropic may send `event: error` mid-stream, for
  example with an `overloaded_error`; OpenAI Responses emits `error` and
  `response.failed` events. An SDK may turn some failures into exceptions while
  yielding others as ordinary events. A decoder that raises only for a
  top-level `error` object will not catch an event with top-level `code` and
  `message`, or an error nested inside `response`. Inspect both event and
  exception paths; the consumer must recognize failures left as events. A
  consumer that has already rendered partial text still ends that attempt as
  failed.
- **Terminal events.** An Anthropic Messages stream runs `message_start`,
  content blocks (`content_block_start`, deltas, `content_block_stop`), one or
  more `message_delta` events carrying `stop_reason`, then `message_stop`.
  OpenAI Responses ends with `response.completed`, `response.failed` or
  `response.incomplete`. A stream that reaches end of input without its
  terminal event is truncated, whatever the HTTP status said.
- **Unknown event types.** Anthropic's versioning policy allows new event types
  and asks clients to handle unknown ones gracefully, and `ping` events can
  appear anywhere. Where that provider's extension contract permits ignoring
  new types, skip them and derive termination only from known terminal events,
  so an unfamiliar type can never be taken for success. This permission does
  not transfer to another protocol whose unknown events may be required.
- **Partial tool arguments.** Tool inputs stream as fragments of a JSON string:
  Anthropic sends `input_json_delta` with `partial_json` for a content-block
  `index`, to be parsed after that block's `content_block_stop`; OpenAI sends
  `response.function_call_arguments.delta` for an `output_index` and `item_id`,
  with the complete string in `response.function_call_arguments.done`. The
  fragments are not valid JSON on their own. Accumulate per index, since
  one response can carry several calls, and parse at the block's end; a partial-JSON
  parser is for display, not for acting on the arguments.
- **Cumulative fields.** Anthropic's `usage` counts in `message_delta` are
  cumulative: replace the running value rather than adding to it.
- **Resumption belongs to an operation mode.** For synchronous OpenAI Responses
  requests, closing the connection cancels the response. Background responses
  instead continue after a dropped stream; cursor-based reattachment requires
  creation with both `background=true` and `stream=true`. With the stream's `sequence_number`,
  `GET /v1/responses/{id}?stream=true&starting_after=<n>` is a cursor-based
  reattachment to the same response, not a new generation. Check the selected
  operation's retention, gap and connection-close behavior rather than
  transferring that guarantee to another mode or provider. Anthropic Messages
  documents recovery by submitting a new continuation request, not by replaying
  the interrupted stream. This starts another generation with its own cost.
  Follow the selected model's continuation rules rather than assuming assistant
  prefilling is supported; incomplete tool-use and thinking blocks cannot be
  partially recovered.

## Pseudo-terminals

Sources: POSIX `close()`
(<https://pubs.opengroup.org/onlinepubs/9799919799/functions/close.html>);
Linux man pages `pty(7)`, `termios(3)` and `TIOCSWINSZ(2const)`
(<https://man7.org/linux/man-pages/>); the `ptyprocess` library
(<https://github.com/pexpect/ptyprocess>) and CPython's `pty` module for the
platform difference in end of output; behavior on macOS as observed with
Python's `pty.fork`.

- **End of output.** Once the child's side is closed, reading the master fails
  with `EIO` on Linux and returns 0 bytes on macOS and the BSDs. Both mean end
  of stream, not an error.
- **Drain before reaping.** A child that writes more than the PTY buffer holds
  blocks until the parent reads, so waiting for its exit before reading can
  deadlock. On macOS, output left unread when the child exits can be gone.
  Read concurrently until end of stream, then collect the exit status; the exit
  status and the end of output are separate signals.
- **Line discipline.** By default, bytes written to the master are echoed back
  into the output, output newlines arrive as CRLF, and control characters act
  as signals: writing Ctrl-C to the master sends SIGINT to the foreground
  process group. A machine-readable protocol over a PTY needs raw mode
  (`cfmakeraw`: character-at-a-time input, no echo, no special input or output
  processing) or a separate channel, or its parser will see its own input and
  `\r\n` line ends.
- **Buffering.** C stdio, and runtimes that follow it such as Python,
  line-buffer standard output on a terminal and block-buffer it on a pipe. The
  same program therefore streams progress under a PTY and delivers it all at
  exit under a pipe. Using a PTY only to obtain line buffering buys the line
  discipline above with it.
- **Window size.** Changing the size with `TIOCSWINSZ` on the master sends
  SIGWINCH to the foreground process group, and full-screen programs redraw;
  setting the same size again sends nothing.
- **Hangup.** The last close of the master sends SIGHUP to the controlling
  process of the child's session. A child that ignores SIGHUP, or processes it
  moved to another process group or session, keep running; closing the PTY is
  not a reliable cancellation: signal each process group involved and reap it.
