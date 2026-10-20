# Blinded review of prompt candidates

A blinded review controls a named bias: attachment to one's own draft,
an author's reputation, or a model's preference for text it wrote. Use it when
one of those could decide a close choice. Every reviewer receives the same
complete candidates and governing question, and sees no other review, emerging
ranking or expected winner.

## Packet helper

The manifest is a JSON object with a nonempty `question` and at least two
`variants`. Each variant has a unique private `id` and exactly one of `path`
or `text`; paths are relative to the manifest. Any other variant fields, such
as `source` or `author`, stay in the private mapping. An optional `top_n` adds
a ranking of that many candidates to the requested answer.

```json
{
  "question": "Which prompt makes the extractor keep table structure on scanned invoices?",
  "variants": [
    {"id": "baseline", "path": "baseline.md"},
    {"id": "rewrite", "path": "rewrite.md", "author": "drafted in this session"}
  ]
}
```

The optional helper needs Python 3 and only its standard library. Resolve it
beside the loaded `SKILL.md`, not against the caller's project directory, and
use explicit manifest and output paths:

```sh
python3 "<package-directory>/scripts/build_blind_packet.py" "/absolute/path/to/manifest.json" --output-dir "/absolute/path/to/prompt-review"
```

The helper shuffles the candidates under opaque labels (`C1`, `C2`, ...) and
writes `review-packet-1.md` and `review-packet-2.md`, which list the same
labels in opposite orders, plus the private `mapping.json`. With two
candidates the second packet swaps them. With three or more, reversal moves
every candidate except the center candidate when the count is odd; only the
two original end candidates are ever read first. The pair of packets therefore
does not balance every candidate across positions. Narrow to the two finalists
and review that pair in both orders before calling a preference. `--orders 1`
writes only the first packet; `--seed` makes the shuffle reproducible. Each
packet states the governing question and the answer it asks for: the
recommended candidate or a coherent synthesis, the decisive language, its
strongest plausible failure, and what makes the nearest alternative lose. The
helper creates each output exclusively, refusing existing files or symlinks,
and rejects duplicate candidate text. If a later output cannot be created, the
earlier files can survive as a partial packet set; use a new output directory
rather than retrying into it. It reads UTF-8 with universal newlines, so the
hashes in the mapping describe the decoded text; keep the source files when
byte identity matters.

Give each packet to a separate fresh reviewer context, or to the same judge in
two fresh contexts. Neither context sees the other packet or its verdict.
Keep the mapping from every reviewer. It records the labels, private ids and
metadata, candidate hashes, packet hashes and orders, and the seed.

## Integrating the reviews

Read the two orders together. Agreement supports a preference that survived
this order check, not its correctness. A flip leaves the preference unresolved:
the candidates may be close, the criterion unclear, or the judge sensitive to
position or ordinary sampling variation. Inspect the reasons against the
governing question; when the choice still matters, a direct trial or expert
judgment may settle more than additional verdicts. Integrate the substance of
disagreement, such as a different assumption or failure mode, instead of
tallying first places. A review that did not finish contributes no verdict.

Opaque labels hide identity, not authorship that the text's style reveals,
and they do not make a reviewer independent of the instructions it already
runs under. A reviewer from a different model family than the author controls
self-preference better than a label does. Several personas in one context are
one review. Record any contamination, such as a reviewer that saw another
review, where it changes how much independence can be claimed.
