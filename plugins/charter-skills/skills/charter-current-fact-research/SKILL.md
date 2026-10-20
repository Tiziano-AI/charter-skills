---
name: charter-current-fact-research
description: Resolve external facts whose freshness or applicability is uncertain;
  reconcile source authority, scope and effective dates to answer the actual question
  with supported conclusions and consequential uncertainty.
metadata:
  content_version: charter-current-fact-research@2026.10.16.0
---
# Charter · Current Fact Research

A current fact is a proposition bound to a subject, scope and time—not merely
a recently published sentence. "Available" can mean announced, generally
released, enabled for this account, legally permitted, installed, or observed
working. Those meanings can disagree without any source being false.

Research becomes tractable when the proposition is the one the person's
decision actually depends on. A feature announced for a premium plan does not
answer whether their existing account can use it; a headline price does not
answer total cost after usage charges and taxes. Check the question's premise
as well: "which plan includes the export API?" assumes the API exists and is
sold by plan, and when the premise is false, saying so is the answer.

What you remember about versions, prices, release states, rules or who holds a
role is a dated, partial snapshot. Use it to decide what to look up, never as
evidence of the current state. A fact that one defining source settles needs
no further method: give it with that source and the date you checked it.

## Authority depends on the kind of claim

Some sources define a fact; others observe or interpret it. A standards owner
defines its specification, an implementation supplies its actual behavior,
and a measurement can show that the implementation diverges. A vendor defines
its service terms but has no comparable authority to establish independent
market impact. The appropriate source follows the proposition, not a universal
ranking of prestigious domains. Note who publishes each source you rely on,
because that decides what it can establish: the Python developer guide and
its release PEPs define when a Python version reaches end of life, while an
aggregator such as endoflife.date restates it; a vendor's pricing page defines
its price, while a comparison site reports what it saw on some date.

For technical adoption, documented version, released artifact, installed
dependency and actual consumer can be different objects. For legal or medical
questions, jurisdiction, individual circumstances and professional context
can change applicability; general guidance does not silently become an
individual determination.

Corroboration also has a causal structure. Ten reports copied from one
announcement provide one evidential origin, not ten independent observations.
Secondary analysis is valuable when it supplies interpretation, comparison or
a new observation; repetition alone adds little. Nor can a majority of reports
outvote the authority that actually defines a contract.

## Time is several different variables

Publication time says when the claim was communicated. Event time says when
something happened. Effective time says when a rule or capability applies.
Observation time says when a source or state was checked. An updated page can
describe an old event; an old instrument can remain governing; a newly fetched
page can announce a future rollout.

This explains many apparent contradictions. A preview document and a production
API reference may describe different support. A regulation and an operator's
implementation may describe obligation and compliance. First align populations,
regions, versions, plans, definitions and effective dates; disagreement that
survives alignment is substantive rather than a reason to average incompatible
statements.

Search snippets and cached indexes are discovery aids. Their freshness cannot
establish the current content of the underlying owner. A precise citation to
an inapplicable source creates false confidence more efficiently than an
uncited guess.

## Lead with the verified answer

Give the answer first, in the form the person will use: the recommendation,
the figure, the draft ready to paste. Then show the few claims that carry it,
each with its direct support linked near the claim, and any step from evidence
to inference or recommendation. Attach a caveat only where it changes how the
answer is used, next to the claim it limits; an unverified detail that would
not change the use needs no sentence, and contrary evidence earns space only
when it changes the conclusion or its scope. In a draft that someone else will
send, put author-side confirmation requests above the draft. Keep any
qualification the recipient needs to understand or act on a claim in the
draft itself; readiness to paste does not make an unresolved claim certain.

If a missing detail decides between actions, name it and give each branch:
"if this account is on the eligible plan, use the feature; otherwise keep the
current path." If every plausible value leads to the same recommendation,
give the recommendation. Another source is worth fetching only when it could
change the answer.

## Literature and market reviews

A review asks for coverage of a field rather than one fact. Search widely
enough to find the whole set: several phrasings, the field's own terms, and
citation trails backward and forward from the key papers; for a market, the
vendors' own product, pricing and filing pages rather than ranked lists that
summarize them. Weight recency by how fast the field moves: start from the
newest survey or market report and look for what appeared after it. Cite the
primary study or the vendor's own page, not the press release, blog post or
aggregator that restates it, and say whether you read the full text or only
the abstract. Stop when new searches keep returning sources you already have
and nothing new would change the conclusion, and say where you stopped.

When sources still disagree after the first alignment, or the question bundles
several claims, [Reconciling a current claim](references/workflow.md) develops
decomposition, the functions of evidence and the mechanisms of apparent
contradiction. A conclusion that will be reused carries the date it was
checked and the change that would invalidate it.
