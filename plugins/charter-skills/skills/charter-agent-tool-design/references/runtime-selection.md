# Runtime Selection

Choose the runtime that makes the tool easiest to distribute and hardest to misuse where it must
run. Familiarity is a tiebreaker, not the governing criterion.

## What decides

The decisive constraints come from the environment the tool must reach, not from the language
easiest to start writing today:

- the repository's current language, build, test, and release toolchain;
- official SDKs or generated clients that own a changing protocol;
- operating systems and architectures the tool must reach;
- startup and concurrency requirements;
- document, media, browser, scientific, or native-system libraries the job depends on;
- install, upgrade, signing, and packaging expectations;
- whether the tool is a standalone product or one entrypoint into an existing application.

A single-binary goal matters when operators cannot maintain a language runtime; it matters less
when the tool is one entrypoint into an application that already ships its runtime. An SDK matters
when it owns a changing protocol, not merely because it saves a little HTTP code.

## How the usual candidates trade

- **The existing product runtime** is usually right when the tool joins an established product: it
  reuses domain models, configuration, migrations, authentication, and release machinery. Reject it
  when it couples an independently distributed tool to a large runtime.
- **Rust or another compiled language** fits a portable single binary with predictable startup,
  bounded dependencies, and streaming or systems work. Cost rises when the job depends on
  fast-moving provider SDKs, browser ecosystems, or libraries native to another language.
- **TypeScript** fits when the product already uses Node, the authoritative SDK lives there, or
  browser and web tooling dominate. Account for runtime distribution, module format, startup, and
  packaged resources.
- **Python** fits document processing, data and scientific work, local automation, and products
  already in Python. Ship it in an isolated application environment so callers do not assemble
  dependencies by hand.
- **Shell** fits a very small coordinator over existing commands. It becomes a liability once the
  tool owns parsing, HTTP, JSON transformation, state machines, or cross-platform behavior.

Admit a dependency because it owns a difficult contract: argument parsing, a provider protocol,
authentication, terminal behavior, serialization, migration, or platform integration. Check its
maintenance, license, runtime requirements, and transitive size; do not add a framework to avoid
writing a few stable commands.

State the choice with the constraint that decided it and the riskiest packaging assumption. Reopen
it when a real target platform, official SDK, or distribution requirement changes, not because
implementation reached an inconvenient edge.
