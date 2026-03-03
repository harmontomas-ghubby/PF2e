# Campaign Template Schema

Template packs live in `data/templates/*.yaml`.

## Top-level keys

- `metadata`: identity and display info (`id`, `name`, `version`, `description`, `recommended_levels`, `tags`).
- `defaults.campaign`: optional campaign defaults set during apply (tone tags, safety notes, tension start, seed).
- `zones`: keyed zone definitions.
- `connections`: links between zones by `from` and `to` zone keys.
- `factions`, `clocks`, `beats`, `gates`, `discoverables`: scaffold entities created transactionally.

## Stability contract

- `metadata.id` is the canonical template id used by backend routing.
- All cross-references are by stable `key` values.
- `zone` references in beats/gates/discoverables must match a zone `key`.
- `prerequisites` in beats must reference other beat keys.

## Companion files

Templates may provide campaign-specific overrides by id:

- Wandering events: `data/wandering/<template-family>.yaml`
- Next questions: `data/next_questions/<template-family>.yaml`
- Tension suggestions: `data/tension_rules/<template-family>.yaml`
