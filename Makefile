# Bedrock build orchestration.
#
#   make venv    create .venv (Python 3.11+) and install pinned tooling (requirements-dev.txt)
#   make check   typecheck + prose lint + marker + glossary + reuse-lint integrity (the gate)
#   make site    build the multilingual hyperlinked site into _build/site
#   make serve   preview the built site locally
#   make gen     weave per-language mono-lingual .lagda.md (agda --html compatibility)
#   make hooks   activate the version-controlled git pre-commit hook
#
# Run `make venv` once per clone; `make` then uses the venv interpreter and tools. Type-checking
# needs Agda; everything Python (lint, markers, glossary, reuse, the site build) runs from .venv
# (Python 3.11+). No node, no GHC; math fonts and KaTeX load from a CDN at view time. Everything
# generated lives under _build/ (git-ignored).

AGDA      := agda
VENV      := .venv
# Bootstrap interpreter for `make venv` (must be >= 3.11); override in CI, e.g. PYTHON=python3.
PYTHON    ?= python3.11
# Interpreter and tools used by all targets (the venv); override only if needed, e.g. PY=python3.
PY        ?= $(VENV)/bin/python
REUSE     ?= $(VENV)/bin/reuse
EVERYTHING := src/Everything.lagda.md
HTML_DIR  := _build/html
SITE_OUT  := _build/site
LANGS     := en,zh
BASE_URL  :=
PORT      := 8000
CF_PROJECT := bedrock

.PHONY: check typecheck lint markers glossary reuse gen html types site serve clean hooks test deploy venv venv-check

check: venv-check typecheck markers lint glossary reuse

venv:
	$(PYTHON) -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else "make venv: need Python 3.11+ (got %s); pass PYTHON=<python3.11+>" % sys.version.split()[0])'
	$(PYTHON) -m venv $(VENV)
	$(PY) -m pip install --quiet --upgrade pip
	$(PY) -m pip install --quiet -r requirements-dev.txt
	@echo "venv ready: $(VENV) ($$($(PY) --version))"

venv-check:
	@test -x $(PY) || { echo "No virtualenv at $(VENV)/. Run: make venv"; exit 1; }

typecheck:
	$(AGDA) $(EVERYTHING)

lint:
	$(PY) scripts/lint-prose.py --check

markers:
	$(PY) scripts/weave-i18n.py --check

glossary:
	$(PY) scripts/check-glossary.py --check

reuse:
	$(REUSE) lint

gen:
	$(PY) scripts/weave-i18n.py --gen --out _build/woven

html:
	$(AGDA) --html --html-highlight=code --html-dir=$(HTML_DIR) $(EVERYTHING)

types:
	$(PY) scripts/extract-types.py --out _build/types.json

site: html types
	$(PY) scripts/render-site.py --html-dir $(HTML_DIR) --out $(SITE_OUT) \
		--langs $(LANGS) --base-url "$(BASE_URL)"

serve:
	@echo "Serving $(SITE_OUT) at http://localhost:$(PORT)/ (Ctrl-C to stop)"
	$(PY) -m http.server $(PORT) --directory $(SITE_OUT)

# Deploy the site (built at domain root) to Cloudflare Pages. Needs `wrangler login`
# or CLOUDFLARE_API_TOKEN + CLOUDFLARE_ACCOUNT_ID in the environment.
deploy: site
	npx wrangler pages deploy $(SITE_OUT) --project-name=$(CF_PROJECT)

test:
	$(PY) scripts/tests/test_i18n.py
	$(PY) scripts/tests/test_glossary.py

clean:
	rm -rf _build

hooks:
	git config --local core.hooksPath scripts/git-hooks
	@echo "pre-commit hook activated (core.hooksPath = scripts/git-hooks)"
