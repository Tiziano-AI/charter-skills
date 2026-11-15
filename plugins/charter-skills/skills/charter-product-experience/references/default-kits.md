# Kits that arrive whatever the product

Vague briefs for onboarding, engagement, retention or an assistant leave room
for familiar kits. The candidates here help recognize a starting answer that
has not yet been chosen for the occasion; they are not a measured ranking of
current output. Each has fitting uses. Preserve a requested pattern and
established choices that serve the journey, and examine the fit where the
brief leaves the decision open.

Each section describes a kit, says where it fits and where it stands in for
design, and most end with a contrast written with real content. The contrasts
are constructed illustrations from deliberately different worlds; copy their
reasoning, not their surface.

## The tour, the checklist and the celebration

A welcome modal, a tooltip tour of the features, a setup checklist with a
progress bar, an illustrated empty state with "Get started" and confetti at
the end. It relies on explaining the interface before use, on the pull of an
unfinished bar, and on a reward for finishing.

In a study of 70 prior iOS users trying four relatively simple iPhone apps,
deck-of-cards tutorials produced no statistically significant improvement in
task success or time; participants who read them rated the explained tasks as
more difficult
([NN/g, Mobile tutorials](https://www.nngroup.com/articles/mobile-tutorials/)).
That result concerns these tutorials and tasks, not every form of teaching.
Apple's guidance recommends teaching through interaction, context-specific
tips rather than one onboarding flow, and postponing nonessential setup
([HIG, Onboarding](https://developer.apple.com/design/human-interface-guidelines/onboarding)).

An unfamiliar interaction, such as a spatial or gesture interface, may need
interactive teaching or contextual help. Required setup may need a checklist,
gone once done: a clinic needs practitioners and opening hours before it can
offer their slots. Those conditions do not by themselves justify a welcome
modal, a tour of every feature or confetti. A tour stands in for design when
it compensates for a main action people cannot recognise where it happens.
Keep progress tied to required work and celebration tied to an achievement the
person values; let optional exploration remain optional.

**A party game played on a living-room television.**

- Default: "Welcome to Quizparty! 👋 Let's take a quick tour." Five cards
  explain rounds, scoring and settings, then "Create an account to host".
- From the occasion: the television shows "Join on your phone · Room KQZD"
  and each player's name appears as their phone joins. The host's phone says
  "Start when everyone's in". The first round teaches the rules by being
  played; scoring is explained the first time points land. An account is
  offered after the game, to keep the room's scores for next time.

## The mascot empty state

An illustration, a friendly line and a generic call to action. The
illustration and line make an empty space feel intentional; they do not by
themselves tell someone what belongs there or how to begin.

The kit fits an emptiness that is itself an achievement, such as a kitchen
rail cleared at the end of service, and a brand whose character people already
know and enjoy, at a pause rather than a missing next step. On first launch,
the empty screen is where the product shows what it will hold and the action
that fills it, from the person's own material where possible.

**A photocard collection.**

- Default: a drawing of an empty binder, "No cards yet! Start your
  collection ✨", and an "Add card" button.
- From the occasion: the album the collector picks shows its whole set as
  outlines, grouped by version and member, with "Daybreak · 4 versions · 28
  cards · you have 0". Tapping an outline marks it pulled; a second copy goes
  straight to the trade pile.

## Streaks, badges and points

A flame and a day count, badges for activity, points and levels. They rely on
not wanting to break a chain and on tokens for doing more.

A streak can support a chosen practice, such as a daily vocabulary drill or
instrument practice, when consecutive performance is part of the goal.
Distinguish that count from accumulated skill or work: a gap can end a streak
without erasing progress. A spare day or a weekly target fits planned rest or
irregular schedules better than a daily chain; a strict continuity goal should
count its gaps accurately. Badges can recognize achievements the person
values, including ones the practice already names, such as a grade, a set or a
personal best. Choose the measure for that purpose rather than counting
product visits as progress.

**A bouldering log.**

- Default: "🔥 6-day streak! Don't break it now." and a "Night Owl" badge for
  logging after ten at night.
- From the occasion: the log's headline is the climber's own, "First 7A,
  sent on the fourth session", in the grading scale they read. It keeps the
  notes across attempts ("left heel, then the sloper") and shows the rest days
  of the plan they chose. The record that matters is progress in climbing, not
  visits to the app.

## Notification nudges and permission at launch

A launch-time permission request makes the interruption channel available
before the person has seen what it will deliver. A reminder chosen only to
increase return visits lacks the event or next step that would make it useful
to its recipient.

Ask for notification permission when the person chooses a concrete
notification service and can understand its benefit. A refusal should leave
the remaining work usable and make the permission-dependent limit clear. When
notifications are essential to the promised job, explain that before the
person invests in setup.

Prompting and recovery differ across platforms and versions: iOS stores the
authorization response and supports provisional delivery; Android behavior
depends on OS version, target version and notification exemptions; browser
requests require the relevant permission and user interaction. For
implementation, read the current
[Apple authorization guidance](https://developer.apple.com/documentation/usernotifications/asking-permission-to-use-notifications),
[Android notification-permission contract](https://developer.android.com/develop/ui/compose/notifications/notification-permission)
or
[web Notifications guidance](https://developer.mozilla.org/en-US/docs/Web/API/Notifications_API/Using_the_Notifications_API).
Follow the platform's rules for any explanatory screen before its system
prompt. Apple's guidelines advise against requesting permission at launch
unless the app cannot function without it, as a navigation app needs location,
and say such a screen's button should not say "Allow", because nothing is
allowed there
([HIG, Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy)).

A notification fits a deadline the person wants to meet, a background result
they need, an agreed next step or another person's action requiring attention.
During grief or illness, distinguish that help from pressure to engage. The
reason, timing and recipient's choices determine whether to interrupt; the
product's wish to be opened does not supply a reason.

**A fantasy-football league in Italy.**

- Default, at first launch: "Attiva le notifiche per non perderti nulla! 🔔"
  ("Turn on notifications so you never miss a thing!") with "Consenti" and
  "Più tardi".
- From the occasion, after the first *formazione* is saved: "Ti avviso un'ora
  prima che si chiudano le formazioni?" ("Shall I remind you an hour before
  lineups lock?") with "Sì, avvisami" and "Non ora". The system prompt follows
  only on yes. This is a choice to create a reminder within the saved lineup,
  not a dedicated permission-primer screen; a separate primer follows the
  platform's current contract.

## The chat box with suggestion chips

A large composer, a greeting, and chips such as "Summarize", "Brainstorm
ideas" or "Write a poem", whatever the product does. It relies on the composer
as a universal input and on chips to fill a blank page.

It fits when the conversation is the job: open questions, thinking aloud,
practising a language by talking. When the result is an artifact people
compare, edit and keep, a queue of decisions or a plan, that belongs at the
center with conversation beside it, as the conversational section of the body
describes. Generic chips teach nothing about what this product can reach;
examples built from the person's own material teach its scope.

**Seating plan for a wedding.**

- Default: "Hi! I'm your wedding assistant ✨ How can I help?" with chips
  "Plan my seating", "Give me ideas" and "Write a toast".
- From the occasion: the floor plan is the center, with round tables and every
  guest as a named token. The couple's constraints sit beside it: "Keep Marco
  and Giulia apart", "Nonna near the door, away from the speakers". A request
  proposes a whole arrangement drawn on the plan, with conflicts marked;
  accepting it moves the tokens, and every guest stays draggable. The example
  requests come from the guest list: "Put the university friends together at
  table 6".

## A setting offered in place of a decision

A toggle added because two groups of people want different things. It relies
on deferring the disagreement to each person.

A setting fits a stable preference that genuinely differs among people: the
grading scale a climber reads, units, language, or a fantasy league's own
rules, held in one place by whoever runs the league. When two needs conflict
and a better default, a different place for the control or a design serving
both would settle them, the toggle postpones the decision and makes every
person discover it.

**A kitchen display.**

- Default: Settings › Tickets › "Confirm before bump" and "Hide bumped
  tickets", added because some cooks bumped by mistake and others found the
  confirmation slow.
- From the occasion: a bump is immediate, and bumped tickets stay on a recall
  strip at the edge of the rail, each one touch from coming back, so nobody
  has to find a setting mid-service. A mistaken bump tends to be noticed only
  when someone looks for the plate, so the strip keeps tickets for the whole
  service rather than for a few seconds. This serves both cooks while a bump
  only moves the ticket; where it also prints, fires the next course or
  messages the floor, those effects need their own way back.

## The dashboard home

"Welcome back, Ana 👋" over stat cards, charts, recent activity and quick
actions. It relies on home as an overview of the product's own activity.

An overview fits when changes across several things determine what the person
should do next, as in an operations room. For other occasions, test whether
the opening should instead restore an object, a case or the next action. A
yearly task can need an overview, and an all-day creative tool can need a
canvas; frequency alone does not choose between them.

**Returning to a residence-permit renewal.**

- Default: "Welcome back! 📊" with cards for Applications: 1, Documents: 7 and
  an old recent-activity list.
- From the occasion: "Your permit expires on 14 May. Your last application
  is saved. The proof of address filed with it needs checking again." The old
  application is shown apart from the current requirements, with a link to
  the responsible authority's current guidance, and retained answers and
  documents are marked unconfirmed until they are checked against it.

## The research template

A named persona with an age, a job and a quote; a journey map with stages
such as awareness, consideration, onboarding, usage and retention under an
emotion curve; findings sorted by heuristic with severity ratings; "quick
wins" and "long-term".

A research-grounded persona can help a team share an understanding of whom it
serves; a journey map can reveal dependencies across touchpoints; a heuristic
report can identify defects and may be the requested result. Invented people
and feelings remain hypotheses. When the commission is to redesign an
experience, an inventory alone leaves the handling of the work undecided: show
the transition to change, the evidence or assumptions behind that choice, and
the proposed interaction with concrete content and words.
[Journey investigation](audit-workflow.md) distinguishes competing
explanations.
