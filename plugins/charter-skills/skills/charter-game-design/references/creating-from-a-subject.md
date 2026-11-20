# Creating from a subject

Use this when the brief names a subject but leaves the play open.

## Turn the premise into something playable

Find actions and tensions in the subject before borrowing a loop. Look at the
objects people handle, the signals they attend to, what they can change and
what they must wait for, risk or leave behind. A source might be a performance,
a tool's behavior, a place's routes, a character's conflicting obligations or
the transformations of an abstract puzzle. Turn that material into something
the player does with a consequence. Fidelity means preserving the relationship
that makes it interesting, not simulating every detail of the activity.

When the direction is open, commit to the relationship a player will feel,
concretely enough to be wrong. It can be a rule, the arrangement of a place
or an authored situation: "triggering a firework fixes the beat on which it
bursts, and it cannot be recalled"; "a tower crane's hook keeps swinging
after the jib stops, so you brake early and let the swing carry the load
home"; "at a wake, each story told about the dead changes which stories the
others can still bring themselves to tell". Let it determine a moment worth
playing, what must be visible there and what counts as a satisfying result.
Then set the idea beside a sibling brief: stage lights that change the
moment you press, a forklift that stops dead, a dinner party where nothing is
at stake. If only the nouns change, the subject does not yet affect play. Ask
again of the first playable, where attractive art can conceal unchanged
decisions. Shared mechanics can be intentional; the test is whether they
deliver this brief, not whether nobody has used them before.

Let that one relationship carry the unfamiliarity inside controls, feedback
and a frame the player already knows. Develop the relationship's consequences
through different situations before adding systems alongside it. An
experimental game about learning an alien system may need several unfamiliar
rules working together; focus is not a mechanic quota. In a faithful genre
exercise, the familiar pleasure is the source, and the contribution can be a
layout or tuning. A local repair inside an established game needs the repair,
not a new premise.

Adding to an established game takes its source from that game: a new level,
enemy or item earns its place by asking a new question of a rule players
already know, in the controls and feedback they already read. The sibling
question there is whether the addition would fit any game of the genre
equally well.

Common first answers to an open game brief in late 2026, likely including
yours; they shift with the model and the year, and each is right for some
game:

- **The reskinned arcade loop** supplies collecting and dodging before finding
  the subject's own verbs. It fits a requested arcade variation; it displaces
  the premise when the promised activity never reaches the rules.
- **Score, hearts and power-ups** make optimization, attrition and escalation
  the structure, potentially replacing interpretation or expression. They fit
  when performance, survivable mistakes and changing capabilities are the
  intended play, with each display or reward explaining that play.
- **Experience points and rarity tiers** can substitute accumulation for
  changed possibilities. They fit when collecting, building a loadout or
  feeling advancement is itself wanted; distinctions in a tier should serve
  that pleasure rather than promise decisions the objects do not offer.
- **Screen shake on every hit** gives frequent contact the same emphasis as a
  decisive event and may hide the next cue. Repeated recoil can suit a
  sustained barrage when readability and comfort hold; otherwise tiers of
  feedback let different events carry different weight.
- **Kind, neutral and selfish replies** feeding a relationship meter label an
  attitude where the player could enact one. They fit when choosing a stance
  is the play; when expression is, write what this character could say, evade
  or admit at this moment.

## Worked creation: a fireworks encore

**Brief:** a small, exuberant game about composing the fireworks encore for a
fictional street festival. The crowd calls, "¡Otra!" ("Again!").

A familiar first answer is to move a launcher, catch sparks, dodge falling
debris and increase a score. That could suit a requested fireworks arcade
game, but it gives this brief the same collecting-and-avoiding decisions as
many unrelated subjects. The source here offers a different relationship:
an ignition and its visible burst happen at different times. Choreographing
what people see means acting before it happens. Finale 3D's distinction
between ignition time, prefire and effect time is useful source material for
this relationship, not a game structure to copy wholesale.

**Committed rule:** triggering a cue schedules its burst after its printed
delay, and the burst cannot be recalled. The player composes the future sky
while the present sky may still be empty.

Keep the frame familiar: a cue sheet, a beat strip and buttons to trigger or
wait. The unfamiliarity lives in committing before the visible payoff, not in
inventing a control scheme as well. Distinguish the pending cue from its
arrival: a marked countdown acknowledges a trigger immediately; the burst
arrives only when due. Otherwise deliberate delay can look like a dropped
input.

## A complete small situation

This slice is a turn-based sequence puzzle. Beats advance only after a player
action, so the first problem tests ordering rather than reaction speed.

- The player has three single-use cues: Red with delay 1, Gold with delay 3,
  and Blue with delay 2. Names accompany colors so the rule does not depend
  on color vision.
- On each beat, the firer's one hand triggers one unused cue or waits. At the
  end of that beat, decrease every pending counter by one, including a newly
  triggered cue. A counter reaching zero produces its burst and leaves play.
- The audience request is Red alone on beat 1, no bursts on beats 2 and 3,
  then Gold and Blue together on beat 4. Completion means matching that
  phrase, not collecting the largest number of bursts.
- The cue sheet shows every delay and the requested phrase. Pending bursts
  appear on the future beat strip. A restart restores the unused cues and
  beat 1 with the same request still visible.

One legal trace:

| Beat | Player action | Pending after the beat | Visible burst |
| --- | --- | --- | --- |
| 1 | Trigger Red | None | Red |
| 2 | Trigger Gold | Gold: 2 | None |
| 3 | Trigger Blue | Gold: 1; Blue: 1 | None |
| 4 | Wait | None | Gold and Blue |

Triggering Gold, then Blue, then Red instead makes all three burst on beat 3.
It is a legal sequence with a different composition, not a random punishment.
Show it against the requested phrase so the missed relationship is legible.
An execution mistake can be retried with one action; a free-composition mode
could keep that alternate phrase as a valid performance rather than a loss.

## Develop the rule instead of adding a reward system

Introduce a cue alone so its delay and acknowledgment are visible, then let
unequal delays produce a shared arrival, as the first request does. That
request is solved cue by cue: each trigger beat is the burst beat minus the
delay plus one, the same subtraction show software performs for a designer.
Decisions begin when the one-hand limit binds. Keep the inventory and change
the request: silence on beats 1 and 2, any two colors together on beat 3,
then the third alone on beat 4. Pairing Red with Gold or with Blue pushes the
remaining cue's trigger onto a beat the pair already uses, so the only
composition is Gold, Blue, wait, Red. The player withholds the cue that
opened the first phrase and plans around the hand, not only each fuse. This
changes the thought without adding a power-up, a faster clock or a larger
score.

Silence is part of the composition, so filling every empty beat with a
particle reward would erase its contrast. Separate the dry trigger cue, the
audible/visible individual burst and the fuller paired finale. Its timing and
mix need to be heard in a playable implementation; a countdown trace proves
only the schedule. For this puzzle, keep delay values and requests reachable
as data so a new phrase can be tried without editing the resolution rule.

The brief's exuberance has a place in the rules too. Once players read the
beat strip, the crowd's "¡O-tra! ¡O-tra!" can become the clock, advancing
beats on the chant instead of on the player's action: the same commitment,
now performed under pressure. That changes the skill the game asks for, so it
belongs after the schedule is understood, as its own stage, not as polish on
the puzzle.

## Test the sibling brief and the playable result

For a show of directly switched stage lights, changing a button can change the
current light immediately. Planning non-recallable bursts several beats ahead
would no longer come from that activity. If the fireworks prototype plays as
"press the matching button when the flash appears," it has lost the chosen
relationship even if the art is recognizably fireworks. The revealing moment
is choosing the next trigger during an empty beat while an earlier burst is
still pending. Does that pending future change what the player chooses now?

This test locates the identity; it does not establish enjoyment. If waiting
is tedious even when the schedule is understood, change the interaction or
the premise rather than attaching experience points to the wait. A deliberately
familiar rhythm game can be the right request too; then reactive timing,
not advance commitment, should shape its encounters.

## Sources and scope

[Finale 3D, *CSV and DMX CSV*](https://finale3d.com/documentation/csv-export-format/)
defines prefire as the delay from ignition to perceived effect and
distinguishes those event times. The game's counters, single-trigger limit,
non-recallable commitment and festival are authored simplifications, not a
model of professional show operation.

[Matthew Davis, *Into the Breach Design Postmortem*](https://media.gdcvault.com/gdc2019/presentations/Into%20the%20Breach%20Postmortem%20Final.pdf)
shows how a commitment to telegraphed attacks shaped threats, defensive goals,
weapons and interface constraints. It supports following a rule's
consequences through a design, not copying that game's deterministic combat
or treating a persuasive premise as evidence of good play.
