# PF2e

> **Status:** Bootstrap phase. This repository now includes a starter structure and docs so new contributors can onboard quickly.

## What this project is
PF2e is intended to be a home for Pathfinder 2e-related tooling and data services. This README is a newcomer-ready template you can keep and refine as features are added.

## Goals (initial)
- Provide a consistent API surface for PF2e entities (ancestries, classes, feats, spells, etc.).
- Keep a clean domain model that is independent from transport (HTTP/API) concerns.
- Make changes safe through automated tests and CI checks.
- Maintain contributor-friendly docs and architecture notes.

## Suggested tech direction (editable)
- **Language/runtime:** Python 3.12+
- **API framework:** FastAPI
- **Validation/modeling:** Pydantic
- **Testing:** pytest
- **Tooling:** ruff + mypy + pre-commit

> If you choose a different stack, keep the same folder responsibilities where possible.

## Quickstart (template)
```bash
# 1) Create and activate virtualenv
python -m venv .venv
source .venv/bin/activate

# 2) Install dependencies (once pyproject.toml exists)
pip install -e .[dev]

# 3) Run tests
pytest

# 4) Run local API (once app exists)
uvicorn pf2e.api.main:app --reload
```

## Repository layout
```text
.
├── README.md                    # onboarding + commands + contribution flow
├── api/
│   └── openapi.yaml             # API contract draft / examples
├── docs/
│   ├── starter-layout.md        # structure decisions and responsibilities
│   └── adr/                     # architecture decision records
├── src/
│   └── pf2e/
│       ├── api/                 # HTTP layer (routers, request/response schemas)
│       ├── domain/              # core business rules and entities
│       ├── services/            # use-cases/application services
│       ├── adapters/            # DB/external integrations
│       └── settings.py          # app configuration
├── tests/
│   ├── unit/                    # fast isolated tests
│   ├── integration/             # DB/API integration tests
│   └── contract/                # API contract tests against openapi expectations
├── scripts/                     # local automation helpers (seed, lint-all, etc.)
└── .github/workflows/           # CI pipelines
```

## First issues to open
1. Create `pyproject.toml` with dev tooling and test config.
2. Add `src/pf2e/api/main.py` with health endpoint.
3. Add first domain model (for example `Feat`) and validation rules.
4. Add one unit test + one API test + one CI workflow.
5. Write ADR-0001 (stack selection + why).

## Contribution workflow (template)
1. Create a feature branch from `main`.
2. Make small, reviewable commits.
3. Run local quality checks (`ruff`, `mypy`, `pytest`).
4. Open PR with:
   - context/problem
   - approach
   - test evidence
   - follow-up tasks

## Definition of done (starter)
- Behavior documented in README/docs.
- Unit/integration tests added where relevant.
- CI checks pass.
- Backward compatibility or migration notes included.

## Learning path for new contributors
1. Read `docs/starter-layout.md` for folder responsibilities.
2. Read ADRs in `docs/adr/` to understand major decisions.
3. Start in `src/pf2e/domain/` to learn core concepts before API plumbing.
4. Run tests and inspect `tests/unit` examples first.
