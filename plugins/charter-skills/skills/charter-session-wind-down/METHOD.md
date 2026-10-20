# Charter · Session Wind-Down

An orderly stop lets useful work survive and leaves no consequence running
that nobody controls. The reason for stopping is a parameter: a pause the user
will lift later, a restart of the app or its host, an account switch, or a
handoff of the work to another agent. The reason changes the wording of the
request and who resumes, not the method. A stop does not require every visible
session to finish, and a completed turn does not mean nothing can start again.

This package owns stopping one session or many, whatever the runtime calls
them (sessions, tasks or threads), including requests to "coordinate" or
"orchestrate" a graceful stop of everything. It does not restart the app or
host, resume or move sessions, or vouch for unrelated processes. Use
`charter-session-portfolio-status` for a report on where sessions stand,
`charter-session-coordination` for dependencies between sessions that keep
running, and `charter-workflow-recovery` after a real interruption has left
effects uncertain. When the stop is part of a transition a harness skill
owns, such as an account switch, use that skill instead: it runs this method
for the stop and adds what the transition needs.

## A readiness question usually needs two lines

When the user asks whether it is safe to stop or restart now, look at the
affected sessions and answer directly:

- "Yes. Nothing is mid-work; the web session's disposable preview can be restarted."
- "Not yet. The migration session is writing the new schema; once that step
  finishes it is at a safe point. Want me to ask it to wind down?"

A disposable development server, file watcher or preview normally needs only
a way to start it again, not a completed product before stopping. Check what
the actual transition does to its owner: restarting a client may leave a
detached or remote process running. It matters when it holds unsaved state,
supports another session or can still produce an external effect; then keep
that dependency or effect controlled. Restarting a local service that no
session depends on needs none of this package.

A session waiting on the user's answer, with the question in its last reply,
needs no wind-down request when the stop would neither leave unmanaged effects
nor interrupt work that needs preserving. Waiting describes the foreground: a
command, delegate or external operation may still be running. The same
condition applies to a session held at an approval prompt.

The stop can still lose the question: after a logout, a restart or a handoff,
nobody may open that reply again. Carry the question, its options and what
depends on it into the report, so that it reaches the user and whoever resumes
asks it rather than deciding it. For an approval prompt, carry what it was
about to do and what depends on it.

The rest of this method is for sessions that are actually mid-work.

## Determine which work the stop affects

Identify what is stopping: one session, a project's sessions, everything in
this app, or the host. Resolve the affected sessions, projectless ones
included, with the tools this runtime offers for listing and reading them.
Sessions those tools cannot see, such as another account's, profile's or
harness's, stay outside the claim unless you can observe them another way.
Visibility in one app does not place every session on that host, and losing a
client need not stop remote execution.

For each candidate, check for a running turn, queued messages, pending input,
running commands or background work, external operations, and a result that
must stay resumable. Idle, settled and untouched sessions can be left out
unless a dependency crosses the stop. Keep separate sessions separate even
when they share a project. When you could see only part of the population,
the readiness claim covers only that part.

## Wind-down changes what may start, not what already happened

Use the user's own wording when they give it. Otherwise send this, with the
reason filled in, in the language the user writes in:

> Stop at the nearest coherent point, because {reason}. Let useful work
> already in flight finish, but start nothing new. In your last message, say
> what completed and where it is, any external effect already performed,
> what remains, the first safe action for whoever resumes, anything still
> running, and any question still waiting for my answer with what depends on
> it. Then wait until I explicitly tell you to continue.

> Fermati al primo punto coerente, perché {motivo}. Lascia finire il lavoro
> utile già in corso, ma non avviarne altro. Nel tuo ultimo messaggio indica
> cosa è stato completato e dove si trova, gli effetti esterni già prodotti,
> cosa resta, la prima azione sicura per chi riprende, cosa è ancora attivo e
> ogni domanda che aspetta ancora una mia risposta, con cosa ne dipende. Poi
> aspetta che ti dica esplicitamente di continuare.

The reason is, for example, "the app needs to restart" / "devo riavviare
l'app", "I am switching account" / "sto cambiando account", "I am pausing this
work" / "metto in pausa questo lavoro", or "another agent will take over this
work" / "un altro agente prenderà in carico questo lavoro". Send it only to
sessions with a running turn, or with a self-starting objective that will
start one, together with the request to pause it below: a message to an idle
session starts a turn there, the opposite of stopping it. Keep each
session's settings as they are. When a session has already accepted an
equivalent request, watch it rather than sending another. A delivered message
is not a wind-down that took effect: look for the effect where the runtime
shows it, and treat silence as not yet seen.

Queued messages are not in-flight work: starting them to empty the queue
defeats the stop. Besides the queue, two things start turns on their own. An
objective that restarts its session whenever it goes idle lets the session
hold still only once that objective is paused. Use the actual runtime's
lifecycle tools and permission contract to establish who can pause it; this
skill does not supply a session-control API. When you cannot pause it
yourself, add to the text "Also pause
your {objective}; this is my explicit request." / "Metti in pausa anche il tuo
{obiettivo}: te lo chiedo esplicitamente." If the session cannot act on it,
the pause is the user's to make. Never mark such an objective complete or
blocked, or clear it, to make it stop. Scheduled work that targets an affected
session, such as an automation, a scheduled task or a loop, starts turns on
its schedule: pause it only when the user's stop covers scheduled work, and
list it among the things to resume. A queued message, objective or schedule
you can see but not control is an item for the user.

Let useful contained actions finish; interrupt when the user asks or when
continuing would defeat the stop. Cancelling a local command can leave an
external operation running, so that operation still needs its owner.

## Keep the way back without doing the work

The coordinator stops work. It does not start implementation, tests, cleanup,
installation, delegation or rollover to make the report look complete, and it
does not commit, push, stash, reset, delete or regenerate another session's
work.

Work can resume when someone can find the intended result, the choices already
settled, what completed and where it is, effects already performed, what
remains, the first safe action, any consequence still live and any question
still waiting for the user. The session's last message, an existing handoff
document or a continuation ledger often holds all of it already: point to it
rather than writing a second record. For a handoff to another agent, that
account is what the receiver starts from, so it names exact paths, branches
and session IDs.

## Report readiness as what the stop would strand

When several sessions are mid-work, keep these states apart:

- **Ready:** the session is at a safe point, the way back survives, nothing
  queued or scheduled will start new work against the stop, and the stop
  strands no live consequence. A pause you asked for counts once you have
  seen it take effect.
- **Draining:** in-flight work, or a wind-down already delivered, is still
  reaching its boundary.
- **Needs you:** an action or decision only the user or the system can take
  remains, such as cancelling a queued message or pausing a self-starting
  objective.
- **Can't tell:** one named missing observation prevents the claim.

Report the mix as it is: "two ready; one needs your cancellation decision" is
more useful than "readiness incomplete". A wait that times out changes none of
these states. Stop watching when everything is ready or the remaining step
belongs to the user; if you return while sessions are still draining, name
them and what is still running. The readiness covers the sessions you
inspected, not the whole machine or whether a restart then succeeds, and the
first safe action you recorded is for after the go-ahead, not something to
start now.
[Reporting across several sessions](references/wind-down-report.md) has a
compact comparison and the states that look alike but need different actions.
