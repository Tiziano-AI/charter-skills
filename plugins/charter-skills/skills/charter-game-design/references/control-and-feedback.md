# Control and feedback

Use this when building a first movement or threat, when an action feels loose,
heavy, unresponsive, hard to read or uncomfortable, or when a proposed
improvement would change the physical skill the game asks of its players.

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
grace (coyote time) permits a jump just after ground contact ends. These can
make an arcade platformer honor an apparent intention that the animation or
collision timing otherwise frustrates. They also change the valid action
window. In a precise simulation or an established competitive ruleset, hidden
assistance may erase a chosen constraint or change what counts as a successful
move. Choose it for the intended skill, not as a universal polish step.

Likewise, aim assistance, snap-to-target and forgiving collisions can support
one fantasy and undermine another. A control adaptation can be optional where
players need different access, while the game makes any consequential effect
on a shared contest intelligible. Do not make physical accuracy the test of
understanding when the game is meant to test planning instead.

## Construct movement from the space it must cross

For a jump, choose an apex height `h` in world units and a time to apex `t` in
seconds. For constant downward acceleration of magnitude `g` and upward launch
speed `v`, derive `g = 2h / t²` and `v = 2h / t`. With positive-up coordinates,
the ascent is `y(s) = v*s - g*s²/2`; positive-down engines reverse the signs,
not the magnitudes. This construction assumes no drag, changing gravity or
intervening collision. The time can also come from horizontal distance to the
apex at running speed, `t = distance / run_speed`, which ties the jump to the
gaps a level contains.

For example, a one-unit-tall character rising
three units in 0.4 seconds needs `g = 37.5 units/s²` and `v = 15 units/s`.
At a constant horizontal speed of five units/s it reaches the apex two units
from takeoff. That gives a concrete relation to a ledge and to camera
look-ahead; collision shapes still decide actual clearance. A longer ascent
at the same height creates more time for correction and more horizontal
travel, not just a slower-looking animation.

Keep the symmetric arc when its predictable flight is the desired
constraint. For snappy arcade landings, increasing gravity after the apex
shortens the descent. A tap can produce a lower jump by increasing gravity
once the button is released while rising, or by holding launch speed only
while the button stays down. Halving gravity near the apex while the button
is held lengthens hang time for placing a landing without raising the jump,
and a cap on fall speed keeps long drops readable. These change the
trajectory, so tune short and held jumps against the same route and measure
the resulting apex in the actual simulation; the simple formula no longer
describes a piecewise arc or guarantees its sampled height under a discrete
integrator.

For scale, *Celeste*'s released player code, at 320×180 pixels with
8-pixel tiles, launches at 105 px/s and holds that speed for up to 0.2 s
while jump is held, applies 900 px/s² of gravity, halves it while vertical
speed is under 40 px/s with jump held, caps ordinary falling at 160 px/s,
allows 0.1 s of ledge grace and reaches its 90 px/s run speed in under a
tenth of a second. Those values serve short screens of exact, forgiving
platforming; a floaty explorer, a heavy character or a wider view changes
most of them.

Choose time to reach running speed and time to stop from the approach and
braking space the move needs. With linear acceleration from rest,
`acceleration = top_speed / time_to_top_speed`; easing or immediate reversal
creates a different response and can be right for a different fantasy. Keep
the camera far enough ahead to see the space in which this decision matters.

Tune coyote time and the pre-landing input buffer separately. One preserves a
late takeoff; the other turns an early press into a jump on landing. Use
simulation time or fixed-step ticks rather than render-frame counts so
rendering rate does not silently change the rule. A queued press expires at
the end of its window and is consumed by the jump it produces, so one press
cannot jump twice; jumping again while the button stays held is a separate
control choice. Choose the windows against actual near-misses and
the intended valid action window, not a universal number of forgiving frames.

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

## Construct warnings and feedback with different weights

For a threat the player should dodge on sight, put the telegraph before the
danger becomes active. Its visible lead time must leave room to notice,
choose, deliver an input and complete the necessary movement, including any
startup before the dodge takes effect. Show the threatened direction or area
while it can change the response. If the skill is anticipating a learned
pattern or reading a bluff, the useful warning can occur earlier in the
sequence instead; a long explicit warning on every strike may remove that
play. Tune in the crowd and camera view of an actual encounter, not only
against an isolated enemy.

Build feedback tiers from what needs to stand apart. In an impact-led game,
an ordinary input can get a small pose change or dry click; a consequential
contact can get local recoil and a material-specific sound; a decisive impact
can get a brief hit-stop and stronger displacement if interruption supports
its weight. A player's own attack can keep its responsiveness with a single
frame of anticipation and a single frame overshooting its final pose; an
enemy's needs enough wind-up to be answered. The *Skullgirls* team kept
framecount starting points for weak, medium and hard moves, the same tiering
applied to timing. A quiet cut can carry more emphasis than another explosion.

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

## Keep tuning reachable

Name the values a play judgment can change: jump height and apex time,
acceleration and stopping time, grace and buffer windows, camera look-ahead,
attack startup/active/recovery durations, and feedback strength. Keep units
beside them in the engine's existing inspector or a coherent configuration
block. When height and time derive gravity and launch speed, edit the targets
rather than maintaining two competing sets of tunable values. In an existing
game, keep the parameters it already uses and report the height and timing
they produce; convert them only when its owner wants to tune that way. Live
controls help repeated tuning; a single local repair does not need a new
debug UI.

Connect a value to a revealing move, such as taking a ledge from standing or
recognizing a wind-up among several enemies. If perceptual observation is
unavailable, deliver that move and the place to tune it while leaving the feel
question open.

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

[Kyle Pittman, *Building a Better Jump*](https://www.gdcvault.com/play/1023148/Math-for-Game-Programmers-Building)
describes constructing trajectories from designer-facing targets and varying
them with input or after the apex. The equations here are the
constant-acceleration derivation for the stated sign convention, not numeric
settings for every platformer. The public session summary supplies the scope;
it does not establish the example's feel.

[Maddy Thorson, *Celeste & Forgiveness*](https://maddymakesgames.com/articles/celeste_and_forgiveness/index.html)
shows coyote time, pre-landing jump buffering and altered gravity near the apex
in *Celeste*. Its particular assistance serves that game's demanding but
forgiving movement; it supplies techniques, not universal window lengths.
The figures quoted above are constants in the game's released player code
([`Player.cs`](https://github.com/NoelFB/Celeste/blob/master/Source/Player/Player.cs)),
read in November 2026.

[Mariel Cartwright, *Powerful and Effective Animation for 2D/3D Games*](https://media.gdcvault.com/gdcchina14/presentations/833784_MarielCartwright_PowerfulAndEffective_EN.pdf)
contrasts player responsiveness with enemy anticipation and describes
hit-stop as an optional impact tool. The warning budget and feedback tiers
above apply that relationship; they are not measured reaction-time thresholds
or a requirement that every game use hit-stop.

[Godot manual, *Idle and Physics Processing*](https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html)
distinguishes variable-rate rendering from fixed physics steps and explains
elapsed-time updates. This supports frame-rate-independent timing windows;
use the chosen engine's timing primitive rather than importing Godot's API.
