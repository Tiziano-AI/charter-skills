# Pipeline stages in depth

Use this when designing a retrieval pipeline, or when the stage that loses or
misuses evidence is known and its repair is not obvious. Each section extends one stage
of the entrypoint; none of them needs to run when that stage already works.

## Parsing

Check the extracted text of the hardest pages before tuning anything after
it: search the parsed output for a phrase from a table cell, a footnote, a
two-column page and a scanned annex. A phrase that cannot be found there
cannot be retrieved.

Keep tables as tables, in Markdown or HTML with their header row; split a long
table into row groups that each repeat the header, and resolve footnote
markers into the text of the same unit. Strip running headers, footers and
page numbers, which split sentences and create false matches. Run OCR in the
document's language on scanned pages and keep page numbers as metadata for
citation. Record document-level metadata at ingest, while the structure is
still visible: title, version, effective date, audience, owner and location.

## Chunk design by document type

**Policies, contracts and regulations.** Use the article or clause as the
unit. Definitions, scope statements and chapter preambles govern the clauses
under them, and exceptions often sit in another article or an annex; attach
the governing text to each clause, or link it so that it is retrieved with
the clause.

**Tables.** A footnote that changes every row must travel with the table. A
section boundary that suits a manual can cut such a table from its meaning.

**Code.** A function or class with its signature, file path and imports is
the usual unit. A transaction that spans functions needs its callers and
callees, which a symbol graph finds better than text similarity.

**Tickets, chats and email.** A thread, or a question with its answer, is the
unit; a single message loses the question it answers.

**Ambiguous fragments.** When a chunk means little out of place ("revenue
grew 3% over the previous quarter", with no company or quarter), prepend a
generated sentence or two that situate it in its document before embedding
and lexical indexing. Derive the context from the source rather than guessed
names or dates, retain the original chunk, and distinguish generated context
from quoted evidence in the result. A useful search aid is not a new factual
authority. This adds generation at indexing time; keep it when representative
questions show better retrieval, not merely because chunks appear clearer.

**Size.** Small chunks give focused embeddings and precise matches, but they
lose conditions and multiply fragments that compete for the few prompt slots.
Large chunks keep context, but their embedding averages several topics, so
they match many questions weakly, and each one spends more of the budget.
Indexing small units and returning their parent section can combine precise
matching with fuller meaning, but adds budget and distractors. Fixed windows
with overlap are a fallback for prose without useful structure; choose their
size from the relationships and misses in the corpus rather than a percentage
alone.

## Retrieval and ranking

Separate the stage that finds candidates, which is judged by recall, from the
stage that orders them, which is judged by precision. A hybrid design can fuse
lexical and dense candidates, then use a cross-encoder to read query and
passage together. Candidate count and reranking depth depend on corpus,
recall, latency and the final answer; exact lookup or a single search route
may already suffice. Reciprocal rank fusion scores each document by the sum
of 1 / (k + rank) over the rankings that contain it. Its positive constant k
controls how strongly high ranks dominate. The [original RRF study](https://cormack.uwaterloo.ca/cormack/cormacksigir09-rrf.pdf)
used k = 60, a concrete starting point when no local evidence favors another
value; inspect it on the query set rather than treating it as optimal for
every corpus. RRF needs no normalization between BM25 scores and cosine similarities.

Use compatible query and document encoders in the same retrieval space. They
may be one embedding model with different input prefixes or a trained pair of
distinct encoders, as in [DPR](https://aclanthology.org/2020.emnlp-main.550/).
Do not mix unrelated model outputs merely because their dimensions match.
Re-embed the corpus when its document representation changes; a query-only
change needs evidence that it remains compatible with the existing index.
Follow the model's query and passage conventions. A multilingual corpus needs a multilingual embedding
model or a lexical index per language. Updates must reach the index; deletion
and access revocation must remove the affected content from retrieval, including
cached results. Historical versions retained intentionally and still permitted
need their version and effective scope with every chunk, so retrieval can select
what governed the requested event rather than making older and newer rules
compete without context. Historical relevance does not override deletion or
access rights.

An empty or weak result can mean no match, the wrong corpus or tenant, a stale
index, denied access or an unsupported format, and a top-k list only says what
ranked highest. Return the searched scope and coverage with results so the
next stage, or the agent, can tell these apart.

## Query rewriting

In a conversation, condense the latest turn and the history it depends on
into a standalone query. Split a question with several parts into
sub-questions and retrieve for each: "which of our German suppliers does the
new regulation affect?" needs the regulation's scope and the supplier list.
Map the user's vocabulary to the documents' vocabulary with synonym and
acronym lists, or with several generated phrasings. When questions and
documents are phrased very differently, embedding a generated hypothetical
answer (HyDE) can find the right neighborhood, but the generated text can
invent identifiers, so pair it with lexical search on the original words.

Keep the original query among the searches and log the rewritten one, since it
is what retrieval saw. A rewrite that drops the decisive attribute
("contractor") recreates the failure upstream of retrieval.

## Filters and applicability

Extract applicability metadata from structure at ingest (the chapter preamble
says "employees"), not by guessing per chunk. Filter hard on the tenant, on
access rights, and on a product or version the user chose explicitly. Treat
attributes inferred from the question, such as role or relevant date, as
boosts until the deciding attribute is established. An effective date is a real
filter when the question fixes one: the policy in force on the date of travel,
not the one in force today. A comparison or historical question may need
several versions; do not apply a current-only filter to it.

Apply document permissions before ranking. A model asked to withhold text it
has received is not access control. Retrieved text is data, and instructions
inside a document ("ignore the rules above") must not arrive where they read as
the product's own instructions: delimit and label every retrieved passage, and
keep it out of the system prompt.

## Ordering and budget

Choose k from the evaluation set: plot the share of questions whose gold
passage reaches the prompt, and answer accuracy, against k. Past the point
where that share flattens, more passages add distractors and cost. Reserve
budget for instructions, history, retrieved context and the answer, and put
the parts that do not change between calls first, where a prompt cache can
reuse them.

Relevance is not sufficiency. Ten relevant passages can repeat one claim and
miss its exception, so deduplicate copies of one source without merging
independent evidence, and keep contradictory passages visible, with their
dates and scopes, until one is known to govern. When a rule and its governing
scope are both retrieved, keep them adjacent. A label such as
`[Travel policy v7 · 4.2 Flights · effective 2026-03-01 · id tp-4-2]` lets the
model check scope and cite. The answer contract should ask for citations by
label, a plain statement of what the sources do not cover, and a question
back when a missing attribute decides the answer.

## Long agent loops and compaction

In a product whose context loop you own, keep the next decision's needs rather
than all past activity. A tool result may be reproducible detail or the only
evidence of an uncertain external effect; age and prior use do not decide
which. Retain intent, constraints, corrections, decisions and reasons, open
items and exact identifiers. Preserve exact wording where paraphrase could
change meaning, and keep a recoverable handle for omitted evidence when one
actually exists. A summary may accompany retained messages or other stores;
inspect the consumer's real inputs before deciding what it alone must carry.
Operating a host runtime follows its context lifecycle, not this product
design advice.

Handing exploration of a large source to a sub-agent keeps its noise out of the
main context, but the returned contribution may omit a needed relationship.
Give the integrating reader access to sources that must be understood together.

Prompt-cache behavior is provider-specific: where exact-prefix reuse applies,
changing tool definitions or earlier context can reduce cache hits. Preserve
useful stability without retaining wrong or irrelevant context merely for a
cache. Exercise a product-owned compaction at a point where it could lose a
constraint or unresolved effect, then inspect the next action and result. A
replay that never invokes that transition says nothing about its retention.

## When an agent searches for itself

An agent that reads a repository or a document folder with search and read
tools has no fixed retriever; file names, section titles and index files do
the index's job. An index line should state the condition for reading the
file ("release.md: before tagging or publishing a build"); "miscellaneous
notes" hides it. Put the discriminating condition in the always-loaded layer
and the depth behind the link. Knowledge every task needs cannot be made
optional by moving it behind a link the agent may never open.

Exact lookup suits known identifiers, filenames and symbols; lexical search
suits distinctive terms; semantic search helps when task and source use
different words. Combine routes when their misses differ. The code an agent
reads while working is context too: a convention against `print()` loses to
the neighboring modules that use it, so cleaning the most-edited files, or
providing the approved helper, can matter more than restating the rule.

## Building and reading the evaluation set

Choose questions that cover the distinctions the decision depends on: real
questions from logs where they exist, plus constructed hard cases for missing
mechanisms. Add production failures when they reveal an unrepresented one.
For each question record the text, the
gold locations (document, section, page span), the expected answer, the
category and whether the corpus can answer it.

Report, per category: candidate recall at k (the share of required gold evidence
retrieved), context recall (the share reaching the final prompt), the rank of
the first gold passage, answer correctness, abstention on unanswerable
questions and citation correctness. For multi-source answers, also report
whether all required evidence arrived: one correct passage can leave its
decisive exception missing. Record acceptable alternative evidence sets rather
than demanding every duplicate source. An average hides the one category, often
scope and exception, that caused the incident. Retrieval metrics need no
judge once gold locations exist; a model grader for answers is usable after
it agrees with a hand-graded sample.

For each miss, write the supported stage and mechanism in a line: "scope in the
previous chunk", "code split by the tokenizer", "superseded version ranked
first", or "correct exception received but not applied". Frequency, consequence
and the ability to intervene choose the next change. Change one stage
at a time, rerun the same set, compare per category, and keep a held-out slice
so the pipeline is not tuned to the questions it is scored on.
