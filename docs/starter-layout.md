# PF2e Starter Layout Proposal

This document explains a concrete, minimal structure to grow the repository from bootstrap to production-ready.

## Design principles
- **Separation of concerns:** domain logic should not depend on web framework details.
- **Testability first:** each layer should be independently testable.
- **Contract-driven API:** keep an OpenAPI draft in `api/openapi.yaml` and test against it.
- **Docs as part of code:** architecture and decisions should evolve with implementation.

## Proposed module responsibilities

### `src/pf2e/domain/`
Core entities and rules for PF2e concepts.
- Examples: `feat.py`, `spell.py`, `traits.py`
- No framework imports.

### `src/pf2e/services/`
Application use-cases orchestrating domain + adapters.
- Examples: `search_feats.py`, `list_spells.py`

### `src/pf2e/adapters/`
Interfaces and implementations for external systems.
- Examples: postgres repository, file loader, HTTP client

### `src/pf2e/api/`
Transport layer and HTTP concerns only.
- routers
- request/response schemas
- error mapping

### `tests/unit`
Fast tests for domain and small services.

### `tests/integration`
Cross-component tests with storage/API wiring.

### `tests/contract`
OpenAPI and endpoint behavior contract checks.

## Suggested first milestone (M1)
- Health check endpoint.
- One resource endpoint (for example: `GET /v1/feats/{id}`).
- One domain model (`Feat`) with validation.
- Repository interface + in-memory adapter.
- 10-20 tests across unit/integration/contract layers.

## Suggested ADR roadmap
- **ADR-0001:** language/framework/tooling choice.
- **ADR-0002:** persistence strategy (JSON vs SQL first).
- **ADR-0003:** versioning strategy for API and data schema.
