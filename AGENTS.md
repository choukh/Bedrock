# AGENTS.md

Working rules for AI coding agents contributing to Bedrock. This is the canonical,
agent-facing rulebook (and the one humans point their agent at). It is plain Markdown with no
required structure; every agent that loads `AGENTS.md` reads this. Claude Code loads it through
the root `CLAUDE.md` (`@AGENTS.md`); other agents read this file directly.

> **This project is very early, and this guide is incomplete.** The absence of a rule here
> does **not** mean there is no rule: it may simply not be documented yet. When you are unsure
> about anything, do **not** guess. Stop and ask the repository owner explicitly, and wait for
> an answer before proceeding. Surfacing a question is always preferred over a confident wrong
> assumption.

## Commands

- **`make check`** is the gate before any commit. It typechecks the masters
  (`agda src/Everything.lagda.md`), validates i18n markers, runs the prose linter, runs the
  glossary checker (`scripts/check-glossary.py` against the term data in
  [dev/glossary.toml](dev/glossary.toml), explained in [dev/GLOSSARY.md](dev/GLOSSARY.md)), and
  runs `reuse lint` for per-file licensing.
- **`make venv`** creates the project virtual environment (`.venv`) from Python 3.11+ and
  installs the pinned tooling in [requirements-dev.txt](requirements-dev.txt). Run it once per
  clone before `make check`.
- **`make site`** builds the multilingual hyperlinked site into `_build/site`; **`make serve`**
  previews it; **`make gen`** weaves the on-demand mono-lingual `.lagda.md` copies.
- **`make hooks`** activates the version-controlled pre-commit hook
  (`scripts/git-hooks/pre-commit`), which runs the prose linter and marker check on staged
  files. Run it once per clone.
- **`python3 scripts/lint-prose.py --fix <files>`** auto-fixes prose (CJK punctuation, quotes,
  paren spacing). Em dashes, single quotes, and quote nesting are reported but fixed by hand.

Requirements: Agda 2.8.0 + cubical 0.9 and Python 3.11+ for `make check`. Python tooling
dependencies (currently `reuse`) are pinned in [requirements-dev.txt](requirements-dev.txt) and
installed into the project `.venv` by `make venv`; `make` then uses that interpreter. The site
build also uses Node only at deploy time (KaTeX and fonts load from a CDN). Tooling:
[scripts/README.md](scripts/README.md).

## Boundaries

- **Always:** run `make check` before committing; author each document in English first, then
  translate; verify a load-bearing assumption cheaply before committing to heavy or
  hard-to-reverse work (large installs, forks, multi-hour builds, framework choices); install
  Python tooling with `make venv` and pin any new dependency in `requirements-dev.txt`.
- **Ask first:** genuine architecture forks (surface them to the owner with a recommendation
  rather than charging ahead on one interpretation); adding a top-level directory (then add its
  `README.md`); a translation term not yet in [dev/glossary.toml](dev/glossary.toml) (choose by
  meaning and surface the choice).
- **Never:** commit generated files (anything under `_build/`, or woven mono-lingual
  `.lagda.md`); translate developer docs; use an em dash in any language; use half-width
  sentence punctuation in CJK prose; commit or print deployment secrets; add an unpinned or
  globally-installed dependency (pin it in `requirements-dev.txt`, installed into `.venv`).

## Documentation taxonomy (user docs vs developer docs)

Bedrock separates documentation by audience, and the two follow different language rules:

- **User-facing docs** (the mathematics and the project itself) are **trilingual** in English,
  Chinese, and Japanese, and live under `docs/<lang>/` (e.g. `docs/{en,zh,ja}/CHARTER.md`).
- **Developer-facing docs** (how to contribute, conventions, specs) are **English only**. They
  live mostly in `dev/` (e.g. [dev/STYLE-i18n.md](dev/STYLE-i18n.md)), but the category is
  broader than that one directory: it also includes the two root developer docs (this
  `AGENTS.md`, the agent rulebook, and `CONTRIBUTING.md`, the human entry point), every
  per-directory `README.md` (listed below), and any other document written for contributors
  rather than readers. Do not translate developer docs.
- **`README.md` is the exception:** both audiences read it, so it follows the **user** rule and
  is trilingual (the English `README.md` at the repo root, with `docs/zh/README.md` and
  `docs/ja/README.md`). Any document that both audiences read is treated as a user doc.

This taxonomy is itself a rule, recorded here. If you add a document, place it by audience.

Developer docs are written **primarily for AI-agent readers** (humans second): favour explicit
structure and file-by-file description over narrative, so an agent can orient quickly. Every
top-level directory carries a short `README.md` to that end: [src/](src/README.md),
[docs/](docs/README.md), [dev/](dev/README.md), [site/](site/README.md),
[scripts/](scripts/README.md), and [.github/workflows/](.github/workflows/README.md). (The
`.github/` guide lives under `workflows/` because a `README.md` placed directly in `.github/`
would be shown as the repository homepage in place of the root `README.md`.) When you add a
top-level directory, add its README.

## Prose conventions (all languages)

Enforced by `scripts/lint-prose.py` and the pre-commit hook:

- **No em dash** anywhere (`—` U+2014, `―` U+2015, the Chinese `——`). Rewrite with a comma,
  colon, period, or parentheses, or split the sentence. The en dash `–` (numeric ranges) and
  the hyphen `-` are allowed. The Japanese long-vowel mark `ー` is not a dash and is fine.
- Inside ` ```agda ` code blocks: **English only**, no CJK and no full-width symbols. Agda's
  own Unicode operators (`≡ ℕ λ Δ₀ →` and the like) are fine. The CJK prose rules below do not
  apply inside code blocks.

### CJK prose (Chinese and Japanese)

- **Full-width sentence punctuation.** Chinese uses `，。；：！？`; Japanese uses the
  ideographic comma and period `、。` (and full-width `；：！？` where needed). Do not use
  half-width `, ; : ! ?` in CJK context (they are fine in code, URLs, and Latin fragments like
  `Cohen (1963)`). Do not "correct" a Japanese `、` to `，`.
- **Quotes** use the corner brackets `「」`. No `"…"`, no `'…'` as quotation marks, and no quote
  nesting. English apostrophes (`V's`) are kept.
- **Parentheses stay half-width `()`** (not full-width), with English-style outer spacing: one
  space before `(` and after `)` (e.g. `经典原理 (LEM、AC) 是…`), no space just inside.
- **No space between two CJK characters**; **no space adjacent to a full-width symbol**.
  Latin-to-CJK spacing elsewhere (`V 的`, `ZF 公理`) is normal and kept.
- **Reflow long CJK paragraphs onto one line.** A hard line break between two CJK characters
  renders as a stray space in Markdown, so write CJK paragraphs as single long lines; break
  only at a Latin word boundary where the space is wanted.

Most of the above is auto-fixable: run `python3 scripts/lint-prose.py --fix <files>`. Em
dashes, single quotes, and quote nesting are reported but must be rewritten by hand.

## Literate Agda and the i18n marker grammar

- Each module is **one master `.lagda.md`** under `src/`: the Agda code appears once, prose for
  every language lives in the same file wrapped in `<!--en--> / <!--zh--> / <!--ja--> / <!--/-->`
  markers, and code blocks are language-neutral (shared). The code can never drift between
  languages because it exists once. Full grammar: [dev/STYLE-i18n.md](dev/STYLE-i18n.md).
- Markers appear only in prose, never inside a ` ```agda ` fence.
- The initial site is **bilingual (en + zh)**; Japanese is **pre-supported** (add a `<!--ja-->`
  block and enable `ja` in the build). Adding a language never touches the code.
- **Woven mono-lingual `.lagda.md` are not committed.** They are an on-demand `make gen` output
  (for `agda --html` compatibility). Everything generated lives under `_build/` (git-ignored);
  never commit generated files.

## Translation workflow

Author each document **in English first**, then translate both the Chinese and the Japanese
from the English. Finally, **cross-check the Chinese and Japanese against each other** once more
for mistranslation, omission, addition, and term drift, and fix before finalizing. Prefer
**meaning over literal calque**.

Confirmed term renderings live in the **canonical glossary data
[dev/glossary.toml](dev/glossary.toml)** (explained in [dev/GLOSSARY.md](dev/GLOSSARY.md)), which
`scripts/check-glossary.py` machine-enforces via `make check` (so a wrong rendering is caught in
CI, not review). Consult it before translating, and when you confirm a new load-bearing term,
**add a `[[term]]` entry there** rather than recording it anywhere else. For a term not yet in the
glossary, choose by meaning and surface the choice to the owner.

## Licensing

Bedrock is multi-licensed under a three-bucket rule, declared per file in [`REUSE.toml`](REUSE.toml)
and enforced by `reuse lint` (part of `make check`):

- **CC BY-NC-SA 4.0**: the mathematical development and user prose (`src/`, `docs/`), the `README`,
  and the brand assets under `site/static/assets/`.
- **OFL-1.1**: the self-hosted third-party web fonts under `site/static/fonts/`.
- **AGPL-3.0-only** (the default): every other first-party file, the tooling, the site front-end,
  build and config, and the prose developer docs (`dev/`, this `AGENTS.md`, `CONTRIBUTING.md`).
  This folds in the front-end adapted from [the 1lab](https://1lab.dev) and the vendored
  `site/vendor/1lab/` tree, which are AGPL-3.0.

A newly added file inherits AGPL-3.0 automatically via the `**` default in `REUSE.toml`; the
carve-outs are the finite content/font set. Full texts are in [`LICENSES/`](LICENSES/) (mirrored as
root `LICENSE-*` files so GitHub's detector lists all three); attributions and the AGPL section 13
corresponding-source statement are in [NOTICE](NOTICE).

All per-file licensing is declared centrally in `REUSE.toml` and verified by `reuse lint`. **Do not
add in-file `SPDX-*` headers** to any file: licensing has one source of truth (like the glossary in
[dev/glossary.toml](dev/glossary.toml) and the i18n masters), so there is nothing per-file to keep
consistent. A new file inherits the `**` default (AGPL-3.0-only) automatically; if it should instead
be CC or OFL, add its path to the matching carve-out in `REUSE.toml`.

## Deployment

Deployment is automatic: on every merge to `main`, GitHub Actions builds the site and publishes
it to Cloudflare Pages (bedrock.institute) and GitHub Pages. Contributors need do nothing and
never handle deployment credentials.

The Cloudflare credentials live only as GitHub Actions encrypted organization secrets (on the
BedrockInstitute org, inherited by this repo); they are never committed, never printed in logs,
and not visible to contributors. The one-time owner
setup is documented in `.github/workflows/cloudflare.yml`.
