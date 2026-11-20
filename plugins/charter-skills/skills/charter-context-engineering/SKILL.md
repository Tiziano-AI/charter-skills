---
name: charter-context-engineering
description: 'Design or repair retrieval and context assembly for LLM answers: trace
  missing evidence, exceptions and conversation history through parsing, lookup, ranking
  and the actual request. Not a prompt rewrite or recovery of a running session.'
metadata:
  content_version: charter-context-engineering@2026.11.20.0
---
# Charter · LLM Context Engineering

Trace an answer-bearing passage into the model's actual input. If the
source contains an exception but the model missed it, was the exception
absent or received and misused? A larger window, higher top-k or “always
check exceptions” cannot distinguish them. For a new pipeline, use real
questions and source structure to choose the simplest path that preserves
their relationships. Documents alone are not a reason to build a vector index.

## Trace evidence from source to answer

Take representative questions whose correct answer and source location you
know, including failures when they exist, and follow each one through the
proposed or running pipeline:

1. **Corpus.** Is the answer in the indexed sources at all, in the version that
   applies to the question? If not, the fix is acquisition or re-indexing, not
   retrieval.
2. **Parsing.** Is the answer-bearing text readable in the extracted text? PDF
   extraction flattens tables, splices running headers into sentences,
   scrambles multi-column order and returns nothing for scans without OCR.
3. **Chunking.** Does one chunk hold the rule together with the condition that
   limits it? A fixed 500-token window can leave "This chapter applies to
   employees; for contractors see Annex C" in the previous page's chunk and
   rule 4.2 without its scope.
4. **Retrieval.** Is the right chunk among the candidates for the query the
   system actually sent, which may differ from what the user typed?
5. **Ranking and cut.** Did it survive reranking and the cut to the passages
   that enter the prompt?
6. **Assembly and use.** Did the model receive it with a label and position
   that let it apply, and did it apply it?

Repair the first supported defect, then inspect the resulting answer. Text
missing from the parsed output needs a parsing repair, not a better embedding model; a passage among the candidates
but cut before the prompt needs reranking or budget work, not new chunking.
Read the prompt the model actually received on the failing call: the
pipeline's configuration says what should have been assembled, not what was.
When sufficient evidence arrived intact, inspect applicability, generation and
the answer's use instead of treating retrieval recall as the remaining cause.
If the received instructions caused the misreading, take the assembled request
and counterexample to `charter-prompt-instruction-and-skill-design`.

## When retrieval is the wrong tool

Retrieval earns its extra failure points when selective access improves
relevance, cost, freshness or permission handling. For a compact body that
applies to every task, direct context may be simpler: keep the indispensable
rules inline and link depth with a cue saying when to open it. Size alone
does not decide what deserves attention on every call. A rule a machine
can check, such as no `print()` or no force unwraps, belongs in a linter or a
test, where it holds whether or not the model read it. A known identifier (a
ticket number, a path, a SKU) wants exact lookup. In these cases the answer is
a short recommendation of where the information goes, not a pipeline design.

## Keep relationships inside the retrieved unit

Index a claim together with its scope. A price without its table headers or a
rule without “for contractors see Annex C” may match a query perfectly and
answer it wrongly. Carry down the governing heading, conditions, date, access
metadata and cross-references. Before choosing chunks, consult
[chunk design by document type](references/retrieval-and-assembly.md#chunk-design-by-document-type);
a parent section can restore a relationship that overlapping windows cannot.

## Retrieve with more than one signal

Use direct lookup for known IDs. Where lexical search finds exact codes and
dense retrieval finds paraphrases, combine them only if their observed misses
differ. Resolve follow-ups against history and look for both a rule and its
exception when the answer needs both. Enforce tenant and access boundaries at
retrieval; boost rather than hard-filter on uncertain inferred attributes.
[Retrieval and ranking](references/retrieval-and-assembly.md#retrieval-and-ranking)
covers query rewriting, score fusion, reranking and scope filters.

## Assemble for the model that reads it

A near miss (the employee rule for a contractor) can mislead more than
unrelated text. An old policy may still govern the transaction: exclude for
inapplicability, not age. Restore adjacent chunks to source order, drop
duplicates and label each passage with its section, source and scope.
Position can influence use; test the intended model and task rather than
assuming a universal order. Let the product ask for a missing attribute or
say its sources do not settle the question.

In a product-owned agent loop, history and tool output may consume much of the
budget. Preserve current intent, constraints, decisions and reasons, unresolved
effects and exact recovery handles. Keep wording verbatim where its precise
meaning matters; compress settled or reproducible evidence according to its
future use, not merely its age. A runtime's own context lifecycle remains with
that runtime rather than becoming something this skill changes. A tool that
returns 50,000 tokens where a filtered excerpt would do has a contract problem, which
`charter-agent-tool-design` owns.

Cache reuse is not continuity of reasoning, nor is a common prefix a cache hit.
If reuse or cost changes the design, inspect the effective request after
SDK transformations and read [ordering, reuse and cost](references/retrieval-and-assembly.md#ordering-and-budget).
Only the provider's actual cache scope, lifetime, usage categories and
charges can establish net savings on equivalent work. Do not retain stale
context or discard useful evidence to improve the hit ratio.

## Evaluate the answer and locate its failing stage

Build a set of questions with known answers and their source locations,
weighted toward hard cases: an answer that depends on a scope or exception, a
table, a cross-reference, which of two versions applies, an exact code, two
passages read together, and questions the corpus cannot answer. Label each
gold answer by document and section rather than chunk ID, so the set survives
re-chunking. Measure coverage of the required evidence among the candidates and
in the final prompt; when an answer needs a rule and its exception, finding only
one is not complete retrieval. Measure answer correctness and abstention
separately, per category of hard case.
To compare changes on answer quality beyond these individual traces, bring
the eligible questions, expected evidence and observed answers to
`charter-ai-evaluation-and-session-learning`. Classify each miss by mechanism, including
received evidence that was misused. Change one stage at a time when attributing an improvement
matters, and rerun the relevant cases. Recall cannot establish answer quality;
a generation change cannot recover evidence that the call needed but never
received.

[Pipeline stages in depth](references/retrieval-and-assembly.md) covers
parsing checks, chunk design for tables, code and legal text, query rewriting,
filter design, ordering, prompt-cache eligibility and cost, compaction in agent loops, agents that
search for themselves, and how to build and read the evaluation set. Open it
when designing a pipeline, or when the failing stage is known and its repair
is not obvious.
