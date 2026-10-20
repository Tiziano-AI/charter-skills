# Mutations, Transactions, And Raw Requests

Mutation design should make target, effect, progress, and recovery legible to both humans and
automation.

## One lifecycle transition per command

Prefer commands such as `draft create`, `release promote`, `job retry`, or `member remove` over a
broad `sync`, `fix`, or `apply-everything`. A command may coordinate several provider calls when they
form one product transition, but it should expose that transaction's identity and partial-failure
behavior.

Inputs should identify the narrowest stable target. Resolve human names before mutation when they
are ambiguous. Display or return account, workspace, project, environment, region, and resource IDs
that materially affect the destination.

## Preview and apply

Use preview or plan when the final target set is computed, high-volume, destructive, expensive, or
difficult to reverse. The preview should contain the same normalized inputs and resolver output the
apply path will use, including:

- exact objects and destinations;
- create, update, delete, transfer, or external-effect classification;
- conflicts, missing prerequisites, and no-op rows;
- irreversible or recovery-limited effects;
- a plan identity or preimage when state can drift before apply.

Apply should re-read state that can invalidate the preview. Do not implement `--dry-run` as a log
message while taking the same remote path as a real write.

For an obvious, reversible, single-object action, a separate plan command may be needless friction.
Make the verb and target explicit and return the changed identity.

## Idempotency and retries

Design create and external-effect commands around an idempotency or operation key when the provider
supports it. On timeout, distinguish:

- request definitely not sent;
- provider rejected before effect;
- outcome unknown;
- operation accepted and queryable;
- operation completed;
- compensation or rollback required.

Never recommend blind retry when the prior effect is unknown. Give the caller the request or
operation identity and a status path that can discriminate. If a key is how the caller finds the
operation again, ship the command that reads an operation by that key, and say in help whether the
key is required or what a call without one risks.

## Multi-phase operations

Uploads, deployments, migrations, exports, and media processing often have phases such as allocate,
transfer, process, attach, promote, and observe. Represent phase state explicitly. Preserve the
identity produced by each successful phase so recovery can resume rather than restart.

If one phase fails, report which effects survive and which next transitions are legal. Avoid broad
error handling that collapses partial completion into generic failure.

## Destructive commands

Use unmistakable verbs and target identities. Prefer recoverable product operations—archive,
disable, trash, revoke, rollback—when they match the domain. If permanent removal is the real action,
do not disguise it as cleanup.

Bulk destructive commands should accept an explicit plan or bounded selector and should not expand
their target set between review and execution without reporting the change.

## Raw escape hatch

A raw command covers provider surface area not yet modeled by high-level commands and helps isolate
protocol defects. It should reuse the CLI's target resolution, authentication, timeout, serialization,
error, and diagnostic machinery.

Example shape:

```bash
tool --json raw get /v1/jobs/job_123
tool --json raw post /v1/drafts --body-file draft.json --preview
```

Use typed body files for non-trivial requests. Classify raw methods by actual effect; a POST named
`query` may still be read-only, while a GET to a legacy endpoint may trigger work. Make live raw
mutations visually and structurally distinct from diagnostic reads.

Do not let raw requests become the documented golden path. When the same raw sequence recurs, model
the domain command and its lifecycle instead.
