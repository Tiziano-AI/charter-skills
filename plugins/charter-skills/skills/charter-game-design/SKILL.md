---
name: charter-game-design
description: 'Design or improve how a game plays: rules, player choices, information,
  controls, pacing and progression. Use it for a paper game or an interactive scene,
  not for engine setup, visual polish or technical QA alone.'
metadata:
  content_version: charter-game-design@2026.11.25.0
---
# Charter · Game Design

Start with a playable moment: what the player notices, can do, expects and
experiences next. Rules, controls, space and presentation can make the same
action precise or precarious, an unexplained room intriguing or simply hard
to navigate. In an existing game, follow a moment that works or disappoints.
In a new one, commit to a playable idea rather than a design document,
feature list or loop diagram. The fantasy and form decide which genre
conventions to keep, solo or shared, continuous or discrete.

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
- Social play depends on what participants contribute and how their actions
  affect each other. Fair contest, shared discovery and fictional conflict
  need different rules.

These sources of interest can coexist. A repeatable loop helps explain a
resource cycle; a sequence of discoveries or changing relationships may
explain another game better. Winning, failure, numeric progression and sustained
intensity are design choices, not prerequisites for play.

## When the game does not exist yet

Find a relationship in the subject that makes a player act differently:
a crane hook keeps swinging after the jib stops, so the player brakes early.
Would the same choice work unchanged in a forklift that stops dead? In an
existing game, a new level asks a new question of a familiar rule; a local
repair needs no new premise.

Common first answers on an open brief—each right in its case, generic outside
it: a **reskinned arcade loop** of collecting and dodging (fits a requested
arcade variation); **score, hearts and power-ups** (fits performance and
survivable mistakes, not interpretation); **XP and rarity tiers** (fits
loadout or advancement play, not changed possibilities); **screen shake on
every hit** (fits a readable barrage, not tiered feedback); and
**kind/neutral/selfish replies** on a relationship meter (fits stance-picking,
not enacted character expression). Before committing an open premise to rules,
read [Creating from a subject](references/creating-from-a-subject.md) for the
full contrasts and a worked fireworks encore.

## Make the mechanism fit the experience

Trace how a proposed change alters what the player can perceive, attempt,
learn or express. A choice that looks different but has the same strategic
payoff may be cosmetic in a tactics game and meaningful self-expression in a
story. Keep the criterion attached to its purpose.

Under uncertainty, separate what the player knows from what the game resolves.
Telegraph enough for the intended anticipation while letting hidden information
carry suspense, bluffing or discovery. Surprise is not automatically unfair,
and exposing every probability can undo the intended uncertainty.

Treat input, simulation, camera, geometry and feedback as one relationship.
Fix the actual mismatch: a camera hiding landing space differs from
inconsistent acceleration. Sound and effects convey weight and contact, not an
unregistered input. Keep deliberate physical constraints while removing
unrelated access barriers.

For discovery, distinguish an invitation to interpret from information needed
to act. A room can support several readings without confirming an official
one; a hazard must support whatever recognition or surprise the encounter
depends on. In shared play, distinguish a character's loss from a player's
exclusion: fictional conflict can be enjoyable when participants retain agency
and a worthwhile contribution.

Settle *what must be noticed* before building a cue. For a silhouette, give
`charter-3d-and-visual-production` viewing distance, reaction time and allowed
ambiguity (scene handles form, light and motion; image makes textures; media
delivers stills or video). Check it in motion at playing distance; camera,
timing and play routes stay here. Hand controls, readouts and menu focus bugs
to `charter-web-apple-and-status-interfaces`, and entry, resume or retention
outside play to `charter-product-strategy-and-design`.

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

Separate a design hypothesis from a defect or missing observation: a dropped
command is not a slow response. Test the channel carrying the experience: a
screenshot cannot show aiming feel, nor a code trigger whether the mix masks a
cue. Observe uncoached play for first-use learning. Before anyone plays it,
leave feel unconfirmed and expose tuning values with units and a move to try.
Use [play observation](references/learning-pacing-and-play-observation.md) to
separate what players learned, did or enjoyed.

An installed `game-studio:game-studio` can route browser-game construction
to engine, UI, asset and playtest specialists. Its early questions about a
loop, failure and progression admit “none”: the plugin supplies production,
not a premise. This method needs no particular engine or plugin.
