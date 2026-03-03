# Solo PF2e Table

Offline-first local web toolkit for running a solo Pathfinder-style campaign. It includes trackers, generators, journal, combat, factions, clocks, map pins, and exports.

> No copyrighted Pathfinder 2e rulebook text is included. This app is a toolkit/tracker; all setting and system flavor text is short/original and user-editable via `data/*.yaml`.

## Setup

```bash
make setup
```

## Run

```bash
make run
# or
uv run uvicorn app.main:app --reload
```

## Test

```bash
make test
```

## Format / Lint

```bash
make fmt
```

## Reset DB

```bash
make db-reset
```

## Edit YAML tables

- Edit files in `data/` (e.g. `data/oracles.yaml`, `data/loot_tables.yaml`).
- Use **Settings → Reload YAML** to refresh without restarting.

Example oracle entry:

```yaml
- category: scene
  tables:
    - name: objective
      entries:
        - {text: "Secure an uneasy alliance", weight: 2}
```

## Export / Import

- Export JSON backup: **Exports → Export JSON**
- Export Markdown journal: **Exports → Export Markdown**
- Import JSON backup into selected campaign: **Exports → Import JSON**

## Keyboard shortcuts

- `/` focus global search
- `r` focus header dice roller
- `j` open journal page
- `n` open scene page
