# Charter · Game Design

A game gives form to what players do, attend to and make of what happens.
Rules, controls, space and presentation work together: the same action can
feel precise or precarious, a choice can express a character or allocate a
scarce resource, and an unexplained room can invite curiosity or leave someone
lost. Design the relationship that produces the intended experience.

This applies to creating a game before a prototype exists and to improving an
existing one, with continuous or discrete play, alone or with others. The
useful result is a concrete playable idea or change, not a compulsory design
document, feature inventory or loop diagram.

## Find what makes this play worth doing

Start with a particular situation: what the player notices, can do, expects,
and experiences next. In a new design, imagine a moment worth playing and the
rules, space or authored material that make it possible. In an existing game,
follow an actual moment that works or disappoints. Genre conventions are useful
expectations, but the intended fantasy and form of play decide which to keep.

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

Depth for the relevant problem:

- [Rules and balance](references/rules-and-balance.md) when choices collapse,
  resources fail to create trade-offs, information or randomness feels wrong,
  or an advantage appears to remove counterplay.
- [Control and feedback](references/control-and-feedback.md) when movement,
  aiming, contact, camera or audiovisual response fails the intended feel, or
  an access barrier is being mistaken for challenge.
- [Discovery, expression and social play](references/discovery-expression-and-social-play.md)
  when shaping exploration, interpretation, narrative choice or participation,
  including when a conventional reward, contest or consequence would change
  their purpose.

## Shape learning, variation and rhythm

Not knowing how to act, misunderstanding a rule, not yet finding a solution
and executing a difficult move are different obstacles. A hint that removes
one may spoil another. Let layout, safe encounters and feedback teach where
they can; text or explicit demonstration is useful when it communicates what
the game cannot otherwise make clear.

Progression can open new combinations, deepen understanding, change a
relationship or develop mastery. Larger numbers need a changed decision or
desired sensation to justify them. Vary pressure, discovery and opportunities
to use what was learned; rest can make tension legible, and familiarity can
make a small change significant. A quiet interval is not automatically lost
engagement.

Open [Learning, pacing and play observation](references/learning-pacing-and-play-observation.md)
when players stall, repeat without learning, tire of an otherwise working
activity, or observations admit several explanations.

## Learn from the play the change affects

A design hypothesis concerns what players will do or experience. A technical
defect concerns whether the implementation performs its intended behavior.
Missing observation concerns what has not been seen, heard or attempted. They
can coexist: first distinguish a dropped command from an intentionally slow
response before redesigning the action around it.

Inspect the channel that carries the claimed experience. A screenshot can
show visual hierarchy, not how aiming feels; audio code can show a trigger,
not whether the mix masks the cue. When the relevant experience is unavailable,
make the design contribution supported by the available material and leave
that perceptual question open. Do not substitute another round of code checks
for hearing or playing it.

Connect the intervention to a specific expectation and a revealing observation:
giving up a firing opportunity to reposition, anticipating a turn earlier,
forming a new theory about a room, or another player gaining a meaningful
contribution. Observe without coaching when first-use learning is the question.
Completion, repetition and reported enjoyment each say something different;
none alone establishes that the intended experience occurred.

## Work with the other owners

`charter-product-experience` owns the wider journey, including entering,
resuming and keeping the result of play. `charter-web-interface-design` and
`charter-apple-interface-design` own platform interaction and implementation;
a menu focus bug need not become a game-design investigation. Game Design owns
the gameplay reason for an input or information choice; the platform owner
supplies a usable, accessible realization.

`charter-3d-art` owns the visual construction of interactive models and
scenes: form, materials, illumination and their appearance in motion within the
renderer. Game Design owns what the player needs to notice, what a response
communicates about a rule, and what may remain ambiguous. Camera behavior,
response timing and routes that affect control or play are game decisions;
3D Art composes their visual expression.
`charter-visual-asset-production` owns standalone image/video assets and can
supply concepts or texture imagery.

If Game Studio is available, its construction and verification workflow and
initial design guidance can support the work. Use this expertise to make the
game-specific decisions within the requested experience, without assuming a
particular engine, plugin or production pipeline. Styling, asset production
and technical QA alone do not require this skill.
