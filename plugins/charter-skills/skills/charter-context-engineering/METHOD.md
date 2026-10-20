# Charter · Context Engineering

An LLM product answers from what reaches the model on that call: the passages
retrieval selected, the history the loop kept, and the order and labels with
which they were assembled. Designing a new pipeline starts with representative
questions, source structure and the relationships an answer must preserve.
Choose the simplest retrieval and assembly path that can carry them; the
presence of documents does not by itself require a vector index.

When an answer is wrong although the sources hold the right one, information
may have been lost before the prompt, or received without being correctly
used. Those failures need different repairs. Raising top-k, moving to a larger
window or adding "always check exceptions" does not distinguish them.

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
missing from the parsed output needs
a parsing repair, not a better embedding model; a passage among the candidates
but cut before the prompt needs reranking or budget work, not new chunking.
Read the prompt the model actually received on the failing call: the
pipeline's configuration says what should have been assembled, not what was.
When sufficient evidence arrived intact, inspect applicability, generation and
the answer's use instead of treating retrieval recall as the remaining cause.

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

Chunk along the document's structure: sections, articles, clauses, functions,
a table with its header row and footnotes. Prefix each chunk with its document
title and heading path ("Travel policy › 4 Travel › 4.2 Flights"). Carry scope
statements that govern many sections (audience, jurisdiction, product version,
effective date) down to every chunk they govern, as text and as metadata, and
turn cross-references such as "for contractors see Annex C" into links that
retrieval can follow. Start from meaningful section boundaries and split long
sections where their relationships survive. Indexing small units while
returning their parent section can restore context when the unit alone is
ambiguous; measure the resulting evidence and distractors on actual questions.
Overlap between fixed windows only softens cuts in unstructured
prose; it cannot reattach a scope stated a page earlier.

## Retrieve with more than one signal

Dense embeddings find paraphrases; lexical search such as BM25 finds exact
identifiers, codes, names and rare terms that embeddings can blur. Combine them
when their observed misses differ; rank fusion can join scores that are not
directly comparable. Add a cross-encoder when its improved selection earns
its cost, rather than making a full hybrid stack the entry price for every
corpus. Rewrite the query when the raw message is a poor query: resolve
"and for contractors?" against the previous turn, pull out the attributes that
decide applicability (role, product, region, date), and search separately for
the rule and for its governing condition when the answer needs both.

Similarity alone does not enforce "applies to contractors", so explicit
applicability attributes belong in metadata. Filter hard on attributes that are reliable and
exclusionary, such as tenant and access rights, which must be enforced at
retrieval rather than requested in the prompt. Boost rather than filter on an
attribute inferred from the question: a wrong inference behind a hard filter
silently removes the answer.

## Assemble for the model that reads it

More passages are not more help. Near misses (the employee rule when a
contractor asks, a policy outside the relevant effective period) mislead more
than unrelated text. An older policy may govern the transaction in question;
superseded does not mean irrelevant. Keep the versions needed to answer or
compare, and exclude one for inapplicability, not age alone. Position can also
change how a model uses long context; test the intended model and task rather
than assuming one universal order. Put decisive passages where they are easy
to connect to their conditions, merge adjacent chunks of one section back into
document order, drop redundant copies, and label each passage with its source,
section and effective scope so the model can apply and cite it. Let the product
say that the sources do not settle the question, or ask for the missing
attribute, instead of forcing an answer from whatever arrived.

In a product-owned agent loop, history and tool output may consume much of the
budget. Preserve current intent, constraints, decisions and reasons, unresolved
effects and exact recovery handles. Keep wording verbatim where its precise
meaning matters; compress settled or reproducible evidence according to its
future use, not merely its age. A runtime's own context lifecycle remains with
that runtime rather than becoming something this skill changes. A tool that returns 50,000 tokens
where a filtered excerpt would do has a contract problem, which
`charter-agent-tool-design` owns.

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
Classify each miss by the supported mechanism, including received evidence
that was misused. Change one stage at a time when attributing an improvement
matters, and rerun the relevant cases. Recall cannot establish answer quality;
a generation change cannot recover evidence that the call needed but never
received.

[Pipeline stages in depth](references/retrieval-and-assembly.md) covers
parsing checks, chunk design for tables, code and legal text, query rewriting,
filter design, ordering and budget, compaction in agent loops, agents that
search for themselves, and how to build and read the evaluation set. Open it
when designing a pipeline, or when the failing stage is known and its repair
is not obvious.
