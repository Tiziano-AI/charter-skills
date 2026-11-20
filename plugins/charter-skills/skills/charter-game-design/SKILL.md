---
name: charter-game-design
description: 'Design or improve how a game plays: rules, player choices, information,
  controls, pacing and progression. Use it for a paper game or an interactive scene,
  not for engine setup, visual polish or technical QA alone.'
metadata:
  content_version: charter-game-design@2026.11.20.0
---
# Charter · Game Design

Start with a playable moment: what the player notices, can do, expects and
experiences next. Rules, controls, space and presentation can make the same
action precise or precarious, an unexplained room intriguing or simply hard
to navigate. In an existing game, follow a moment that works or disappoints.
In a new game, commit to a playable idea rather than a design document,
feature inventory or loop diagram. The fantasy and form of play decide which
genre conventions to keep, in solo or shared, continuous or discrete play.

Locate the source of interest before choosing a remedy:

- Tactical or strategic play depends on alternatives whose value changes with
  circumstances, information and opportunity cost. More buttons do not add
  depth when one action makes the others pointless.
- Movement and action depend on the relationship between input, response,
  space and perceptible consequence. Assistance can support an arcade
  fantasy while removing the inertial judgment a simulation is about.
- Exploration and interpretation depend on questions worth pursuing, clues
  worth connecting and room to form an understanding. Adding a score or a
  fight can redirect attention away from the place the player came to explore.
- Authored choices can change events, reveal a viewpoint or let the player
  express one. Rejoining branches is not inherently a false choice; promising
  lasting consequences and then erasing them is a different defect.
- Social play depends on what participants can contribute and how their
  actions affect one another. Rules may support a fair contest, shared
  discovery or creative agreement during conflict between fictional
  characters. These need different interventions.

These sources of interest can coexist. A repeatable loop helps explain a
resource cycle; a sequence of discoveries or changing relationships may
explain another game better. Winning, failure, numeric progression and sustained
intensity are design choices, not prerequisites for play.

## When the game does not exist yet

Find a relationship in the subject that makes a player act differently:
a crane hook keeps swinging after the jib stops, so the player brakes early.
Would the same choice work unchanged in a forklift that stops dead? In an
existing game, a new level can ask a new question of a familiar rule; a local
repair needs no new premise. A requested arcade variation can earn its score,
hearts and rewards, but adding them to a game about interpreting a place may
replace the pleasure the player came for.

Before committing an open premise to rules and situations, read
[Creating from a subject](references/creating-from-a-subject.md) for the
contrasting design choices and a worked fireworks encore.

## Make the mechanism fit the experience

Trace how a proposed change alters what the player can perceive, attempt,
learn or express. A choice that looks different but has the same strategic
payoff may be cosmetic in a tactics game and meaningful self-expression in a
story. Keep the criterion attached to its purpose.

For decisions under uncertainty, distinguish what the player knows from what
the game resolves. Telegraph enough to support the kind of anticipation the
game asks for; hidden information can still create suspense, bluffing or
discovery. A surprising outcome is not automatically unfair, and exposing
every probability can destroy the uncertainty the design intends.

For control feel, treat input, simulation, camera, level geometry and feedback
as one relationship. Change the part that causes the mismatch: a camera that
conceals landing space needs a different repair from inconsistent acceleration.
Sound, animation and effects can communicate weight and contact; adding them
cannot make an unregistered input take effect. Preserve deliberate physical
constraints while removing unrelated motor, sensory or comprehension barriers.

For discovery, distinguish an invitation to interpret from information needed
to act. A room can support several readings without confirming an official
one; a hazard must support whatever recognition or surprise the encounter
depends on. In shared play, distinguish a character's loss from a player's
exclusion: fictional conflict can be enjoyable when participants retain agency
and a worthwhile contribution.

If the player needs a cue to act, settle *what must be noticed* before the cue
is built. For a silhouette, give `charter-3d-and-visual-production` the viewing
distance, time to react and what may stay ambiguous. Its scene method handles
form, materials, light and motion; its image method makes new source imagery
such as a texture, and its media method delivers standalone images or video.
Check the cue in motion at playing distance; camera behavior, timing and
routes that change play stay here. For a control or readout, hand the actual
player decision to `charter-web-apple-and-status-interfaces` for accessible
platform interaction. A menu focus bug goes there directly. If entering,
resuming or keeping a result fails outside the play itself, follow that
journey with `charter-product-strategy-and-design`.

Depth for the relevant problem:

- [Rules and balance](references/rules-and-balance.md) when choices collapse,
  resources fail to create trade-offs, information or randomness feels wrong,
  or an advantage appears to remove counterplay.
- [Control and feedback](references/control-and-feedback.md) when constructing
  or repairing movement, aiming, threats, contact, camera or audiovisual
  response, choosing reachable tuning parameters, or distinguishing an access
  barrier from challenge.
- [Discovery, expression and social play](references/discovery-expression-and-social-play.md)
  when shaping exploration, interpretation, narrative choice or participation,
  including when a conventional reward, contest or consequence would change
  their purpose.

## Shape learning, variation and rhythm

Not knowing the controls, misunderstanding a rule, searching for a solution
and struggling to execute a move need different interventions. A hint for one
can spoil another. Progress can mean a new combination, understanding or
mastery; rest can make tension legible.

Open [Learning, pacing and play observation](references/learning-pacing-and-play-observation.md)
when players stall, repeat without learning, tire of an otherwise working
activity, or observations admit several explanations.

## Learn from the play the change affects

Separate a design hypothesis from a technical defect or a missing observation:
a dropped command is not an intentionally slow response. Try the channel that
carries the experience: a screenshot cannot show how aiming feels; a trigger
in code does not tell you whether the mix masks the cue. Observe uncoached
play when first-use learning is the question. If nobody can play it yet, leave
the feel unconfirmed and put tuning values where a player can change them,
with units and a move to try. Use [play observation](references/learning-pacing-and-play-observation.md)
to choose evidence that distinguishes what the player learned, did or enjoyed.

An installed `game-studio:game-studio` can route browser-game construction
to engine, UI, asset and playtest specialists. Its early questions about a
loop, failure and progression admit “none”: the plugin supplies production,
not a premise. This method needs no particular engine or plugin.
