# Control and feedback

Use this when an action feels loose, heavy, unresponsive, hard to read or
uncomfortable, or when a proposed improvement would change the physical skill
the game asks of its players.

## Feel is a relationship

The player supplies input through a device; the game interprets it, changes a
simulation or discrete state, and presents the consequence through a camera,
animation, sound and other feedback. Level geometry gives that response
meaning. A turning radius that feels graceful in an open space can feel
unmanageable in a corridor designed for instant turns.

Locate the mismatch in that relationship. Delayed input delivery, gradual
acceleration, an animation before action, a camera trailing the character and
an unclear contact effect can all be described as "sluggish." They need
different changes. An instantaneous camera and an inertial vehicle can be a
good combination; removing the vehicle's inertia because the camera is late
would change the wrong thing.

Observe the relevant action and state, including the device when it matters.
A keyboard's discrete presses, an analog stick's magnitude, a pointer's
position and a touchscreen gesture offer different control. Copying numeric
sensitivity between them does not preserve the experience. In turn-based
play, clear selection, targeting and commitment can matter more than continuous
response; intentional deliberation is not input lag.

## Preserve the source of mastery

Acceleration, braking, momentum, air control and turning limits determine
which anticipation and correction the player learns. Camera framing and
look-ahead determine how much of the upcoming space is available for that
judgment. Tune them together with collision shapes, target sizes and level
spacing rather than optimizing each in isolation.

Input buffering accepts an action just before it becomes legal; a small ledge
grace permits a jump just after ground contact ends. These can make an arcade
platformer honor an apparent intention that the animation or collision timing
otherwise frustrates. They also change the valid action window. In a precise
simulation or an established competitive ruleset, hidden assistance may erase
a chosen constraint or change what counts as a successful move. Choose it for
the intended skill, not as a universal polish step.

Likewise, aim assistance, snap-to-target and forgiving collisions can support
one fantasy and undermine another. A control adaptation can be optional where
players need different access, while the game makes any consequential effect
on a shared contest intelligible. Do not make physical accuracy the test of
understanding when the game is meant to test planning instead.

## Feedback explains action

Feedback can acknowledge input, expose a state change, suggest a material,
direct attention or reinforce mood. Assign it a job. A recoil animation can
communicate force, an impact sound can identify contact, and a restrained
target response can distinguish a hit from a miss. Effects that all peak
together can mask the event that matters next.

Separate anticipation, execution, contact and recovery when diagnosing an
action. A wind-up can make commitment legible; a delayed impact sound may
disconnect cause from contact; a long recovery may create tactical exposure.
Removing every pause can make actions less readable or weightless, while
adding hit-stop to every action can make sustained movement unpleasant.

Camera shake, flashes, particles and loudness do not repair inconsistent
targeting or a command that never registered. They can also reduce visibility
or comfort. Prefer distinct, proportionate cues over maximum intensity, and
preserve important information when an optional effect is reduced.

Audio needs listening in context. Check whether a cue is audible against the
mix, whether repeated triggers become tiring, and whether its spatial or
rhythmic information is doing work. A source file or event hook establishes
neither its level nor its perceptual meaning. Screenshots similarly omit
motion, response and camera behavior.

## Access and challenge are different decisions

Identify the ability the game intends to exercise. Small text, color-only
signals, excessive simultaneous inputs or unavoidable camera motion may add a
barrier unrelated to it. Remapping, readable cues, alternatives to a held input
and motion controls can remove that barrier without replacing the central
judgment. A rhythm game, however, cannot treat timing as incidental merely
because timing is demanding.

An adaptation should preserve the information or action the player needs, not
just satisfy an interface convention. Pairing an audio warning with a visual
signal can preserve knowledge of danger; a full-screen flash might introduce
a different access problem. Select relevant accommodations for the game's
mechanics and audience rather than importing an entire generic checklist.

## A useful contrast

A drifting vehicle rounds a bend poorly because its camera shows the bend
only after braking should start. Earlier visibility can restore anticipatory
driving while preserving inertia. If the same vehicle belongs to a toy-like
arcade racer whose fantasy is immediate steering, stronger correction or a
different handling model may be right. "More responsive" is incomplete until
the desired relationship between intention and motion is clear.

## Sources and scope

[Steve Swink, *Game Feel: The Secret Ingredient*](https://www.gamedeveloper.com/design/game-feel-the-secret-ingredient)
describes how input, response, context and presentation contribute to feel;
it is a design account, not a prescription for the same response model in
every game. The examples here are conditional applications of that lens.

[Game Accessibility Guidelines, *Why and how*](https://gameaccessibilityguidelines.com/why-and-how/)
supports distinguishing unnecessary access barriers from intended challenge
and choosing applicable guidance. Consult the relevant guideline when an
actual control or presentation decision needs more detail.
