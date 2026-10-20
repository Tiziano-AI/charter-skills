# Worked cases and functional allocation

Use these contrasts when a product has plausible components but its useful
work remains unclear. The examples are illustrative designs, not claims about
an existing product or regulations.

## Evidence retrieval versus assessment

Suppose a buyer asks whether a supplier meets an internally defined control:
"Each privileged account must have a named owner and a completed review."
The input contains a procedure saying reviews are required, an account register
with two owners missing, and a review sheet that omits three accounts.

A retrieval product can return the relevant passages and rows. An assessment
must perform additional functions:

| Transformation | Substantive work | Meaning the result must preserve |
| --- | --- | --- |
| Documents to observations | Extract accounts, owners and review records; retain source identities | The procedure states a rule; it is not evidence of completed reviews |
| Observations to comparable evidence | Match account identities and establish the population covered | Unmatched identities or differing scope cannot be silently joined |
| Evidence to findings | Apply each part of the criterion to the relevant population | Missing evidence differs from evidence of noncompliance |
| Findings to disposition | Apply the buyer's adopted decision rule or expose the unresolved choice | A recommendation is not the buyer's approval |
| Findings to action | Name the missing owner assignments or review evidence to obtain | A concrete request differs from generic advice to improve controls |

For this example, a usable result could report the two accounts lacking owners,
the three without review evidence, their source locations and the effect under
the buyer's stated rule. If no decision rule is supplied, it can still deliver
the findings and the exact unresolved policy question. It should not invent a
score merely because the interface has a score field.

The account matching might be deterministic for shared identifiers, assisted
for aliases and unresolved for ambiguous matches. Interpretation of narrative
evidence may need a model. The acceptance rule may be executable once the buyer
has chosen it. This allocation follows the work; assigning everything to one
"assessment agent" obscures which part actually supplies the judgment.

Conversely, if the promised product is evidence search, passages with correct
scope and locations may be the entire useful result. Adding an assessment
workflow then expands the product rather than completing it.

## From knowledge to action

A service desk product receives "I cannot access the shared folder." Retrieving
an access policy does not resolve the request. The functional questions include
which identity and resource are meant, whether the problem is authentication or
authorization, what access already exists, which rule permits a change, and how
the outcome is communicated.

If the product may only advise, its whole result can be a grounded diagnosis and
the exact action for the authorized operator. If it promises to carry out access
changes, it also needs eligibility determination, any required approval, the
mutation, and a way to establish or recover its outcome. A polished explanation
cannot substitute for the action in that second promise.

An administrative approval and an uncertainty question are different handoffs.
"Approve access to resource R for identity I under policy P" transfers a
decision with its consequences. "Which of these two identities do you mean?"
supplies missing information. Treating both as generic human review makes the
interface unhelpful and can give reviewers a decision they never meant to take.

## Meaning at a preparation boundary

A document preparation service emits a normalized claim such as
`review_completed: true`. That loses meaning if it drops whether the original
said "reviews are required," "we usually review," or "these listed accounts
were reviewed." The consuming assessor cannot reconstruct a distinction the
preparer discarded.

A better handoff exposes what was asserted, by whom or by which source, for
which subject and scope, and any unresolved extraction ambiguity. The assessor
then owns the inference it makes from those observations. This does not require
a universal ontology: a small domain representation can retain exactly the
relationships used by the real decision.

The countercase is a mature upstream service that already owns the validated
decision and exposes its scope. Recomputing it from copied raw data can create
conflicting authorities. The consuming product may need to interpret the
decision's consequence, not repeat its internal work.

## Slices that preserve the whole product

Suppose the agreed product must compare suppliers, assess one supplier, identify
missing evidence and produce an action plan. The first complete slice might
assess one supplier against one adopted control family, with real evidence and
an actionable result. Comparison additionally needs comparable scope and rules;
an action plan needs priorities and concrete follow-up actions. Those functions
remain part of the design even when not in the first slice.

Infrastructure can be built first when it enables the next function. Label its
result accurately: searchable documents, not supplier assessment. A manually
performed step can reveal what the function requires before automation, but
only if the handoff fits the commissioned product. If the stated capability is
unattended assessment, permanent manual reasoning is an unresolved gap rather
than completion by relabeling.

The design is specific enough when an implementer can explain what a plausible
input produces, why it produces that result, and which component or person does
each consequential piece of work. More decomposition is useful only where an
unresolved function would otherwise be invented during implementation.
