# Solo PF2e Runner

## Campaign templates

Campaign pages now include a **Templates** section with an HTMX flow:

1. Click **Apply Template: Shattered Titan Vault**.
2. Confirm the modal prompt.
3. The app posts to `/campaigns/{campaign_id}/templates/shattered-titan-vault/apply`.
4. On success, the template is inserted transactionally and the user is redirected back to the campaign dashboard.

Template application is blocked when the campaign already has scaffold content (zones/beats/gates/factions/clocks/discoverables) or already has a `template_id`.

## Template data files

- Main pack: `data/templates/shattered_titan_vault.yaml`
- Wandering override: `data/wandering/titan_vault.yaml`
- Next Question override: `data/next_questions/titan_vault.yaml`
- Tension suggestion override: `data/tension_rules/titan_vault.yaml`
- Schema docs: `data/templates/README.md`

## Template-specific engine behavior

When a campaign has `template_id = "shattered_titan_vault"`, loaders can prefer Titan-specific files:

- Wandering events -> `data/wandering/titan_vault.yaml`
- Next Question prompts -> `data/next_questions/titan_vault.yaml`
- Tension suggestions -> `data/tension_rules/titan_vault.yaml`

Fallback remains `default.yaml` in each domain when no template override exists.
