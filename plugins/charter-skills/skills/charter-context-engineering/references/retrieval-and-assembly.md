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
budget for instructions, history, retrieved context and the answer. When
repeated context makes reuse worthwhile, put stable material before changing
material where its meaning and the model's use permit it. A changing snapshot
before an otherwise growing history breaks exact-prefix reuse of that history;
moving only the latest question does not repair an earlier changing field.
Keep necessary causal order, governing conditions and the current task clear.

Relevance is not sufficiency. Ten relevant passages can repeat one claim and
miss its exception, so deduplicate copies of one source without merging
independent evidence, and keep contradictory passages visible, with their
dates and scopes, until one is known to govern. When a rule and its governing
scope are both retrieved, keep them adjacent. A label such as
`[Travel policy v7 · 4.2 Flights · effective 2026-03-01 · id tp-4-2]` lets the
model check scope and cite. The answer contract should ask for citations by
label, a plain statement of what the sources do not cover, and a question
back when a missing attribute decides the answer.

### Prompt-cache reuse and cost

A provider prompt/KV cache reuses input computation; it is not a response cache,
a durable memory store or an application checkpoint. Diagnose the layer whose
reuse matters. Persisted history does not mean cached model input, and response
storage controls need not control prompt caching.

Separate the structural opportunity from its realization. Compare the effective
requests the provider receives, not just the application's context object:
tools and their order, schemas, instruction roles, message/content boundaries,
multimodal representations and SDK or gateway transformations can change the
rendered prefix. Deterministic serialization prevents accidental churn; it
cannot make a changing early field stable. Internal provider rendering may not
be visible, so a character-prefix comparison alone proves neither token
identity nor a cache hit.

Identical content still needs an admitted write and a reachable later lookup.
Check the target API/model's minimum, write policy, cacheable boundaries and
bounded lookback, or explicit-resource identity. A growing string can retain
all the old bytes but lose the old endpoint as a lookup boundary; moving a
marker to its new end need not find the earlier write. Then consider scope
(account, workspace, project, region or deployment), expiry and eviction,
routing affinity and concurrency: a parallel request can arrive before the
first write is available. A cache key may influence routing or accounting;
it neither makes changed input identical nor universally identifies a saved
entry. Follow its contract instead of transplanting it across APIs.

These provider distinctions change the design; use their current contracts
for the selected model, endpoint and deployment rather than freezing prices,
thresholds, retention values or support tables here:

| Provider path | What changes the choice |
| --- | --- |
| [OpenAI prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching) | Automatic token-prefix caching and breakpoint-aware model families have different write, lookup and pricing rules. In the latter, unchanged instructions can lack their own reusable entry if only a later changing boundary was written. Check the exact endpoint's schema and SDK as well as the guide; a longer common prefix alone does not establish eligibility. |
| [xAI prompt caching](https://docs.x.ai/developers/advanced-api-usage/prompt-caching/how-it-works) | Automatic prefix reuse and per-server availability make [affinity](https://docs.x.ai/developers/advanced-api-usage/prompt-caching/maximizing-cache-hits) relevant. The Responses body key and Chat Completions header are endpoint-specific controls, not interchangeable wire fields or hit guarantees. Faithful conversation continuation, including reasoning items where required, differs from rebuilding one snapshot string. |
| [Anthropic Messages caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) | Tool, system and message prefixes form an ordered hierarchy. Caching is opt-in per request: top-level automatic placement or explicit block markers select writes; a request with neither writes nothing. Backward lookup searches prior written boundaries within a bounded range. Minimums, availability of the initial write, invalidation and isolation depend on model/platform; a marker alone does not establish a cached prefix. |
| Google [Gemini Developer API](https://ai.google.dev/gemini-api/docs/caching) and [Cloud caching](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview) | Implicit reuse and explicit cache resources have different support, lifecycle and costs. Developer API Interactions and generateContent do not expose the same cache controls; availability also differs by model family and Cloud route. An explicit resource needs a valid model, scope/location and lifetime; storing content is a separate cost decision, not a universal Gemini recipe. |

Retain native usage and effective model/API, request or attempt identity and
relevant settings in the product's existing diagnostics when measurement is
needed. Missing usage is unknown, not zero. For streaming, usage may arrive in
the terminal event rather than the text deltas. Preserve it through the adapter
instead of inferring reads from latency or a prefix diff. Request identity also
prevents shared openings, retries or aggregate and per-step totals from being
counted twice.

Build disjoint billable categories before pricing. For example, Anthropic's
`input_tokens` excludes `cache_read_input_tokens` and
`cache_creation_input_tokens`; the latter's lifetime subfields partition that
creation total. OpenAI cached-input details and Google's generateContent
`cachedContentTokenCount` are already within their respective input totals;
Google Interactions has another usage schema. A write price can replace the
ordinary input rate rather than supplement it, and a read can refresh expiry
without becoming a write. Check [xAI usage](https://docs.x.ai/developers/advanced-api-usage/prompt-caching/usage-and-pricing),
[Gemini usage metadata](https://ai.google.dev/api/generate-content#UsageMetadata)
and the adopted endpoint's accounting before mapping fields with similar names.
Separate read-token coverage from the fraction of requests with any hit; for
coverage, divide summed reads by summed total input, not an unweighted average
of request percentages. Neither measure is money saved.

Compare total cost for equivalent useful results: uncached input, reads,
writes or refreshes where billed, storage over its retained lifetime, output
(including reasoning according to its accounting), tool charges and additional
attempts or warmup calls. Apply the actual tier and context-length rates to
the categories they govern; cached tokens can still count toward a context
threshold. A larger retained prompt can improve read coverage while raising
total cost, and writing a suffix that never recurs can cost more than ordinary
input. Longer retention earns its cost through useful later reads, not through
its advertised discount. Distinguish a conditional list-price calculation from
observed usage, provider billing and a forecast of future hits.

Choose the smallest comparison that can change the product decision, not a
cache audit for every RAG task. Offline checks can establish stable content,
preserved meaning and correctly emitted boundaries or keys; they cannot prove
provider admission or savings. When an admitted live observation is needed,
inspect reads, costs and answer quality separately. Reordering evidence or
changing compaction still needs the product's substantive quality check. Keep
freshness, access revocation and history correctness even when they invalidate
cache, and do not add cache infrastructure or change provider merely to improve
the metric. Context assembly belongs here; native controls and usage transport
belong in the product's provider adapter, without a second context workflow.

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

Compaction changes the next request as well as its size; apply the reuse and
cost distinctions above when that trade-off matters. Exercise a product-owned
compaction at a point where it could lose a
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
