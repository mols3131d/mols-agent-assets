# Migration

## Replacement Boundary

Replace the legacy `src/skills/mols-agent-asset-studio/` directory with the new
canonical directory and add `src/skills/mols-agent-asset-tuner/`.

Do not merge the old CSV router and `workflows/` hierarchy into the new Studio.
The new `SKILL.md` and `references/operations.md` own routing and operation
discovery.

## Safe Migration

```bash
git switch -c agent/modernize-asset-studio
git mv src/skills/mols-agent-asset-studio \
  .tmp/mols-agent-asset-studio-legacy
cp -R <bundle>/src/skills/mols-agent-asset-studio src/skills/
cp -R <bundle>/src/skills/mols-agent-asset-tuner src/skills/
```

Validate the final paths:

```bash
python src/skills/mols-agent-asset-studio/scripts/validate_asset.py \
  src/skills/mols-agent-asset-studio \
  --profile agent-skill --strict
python src/skills/mols-agent-asset-studio/scripts/validate_asset.py \
  src/skills/mols-agent-asset-tuner \
  --profile agent-skill --strict
python src/skills/mols-agent-asset-studio/scripts/validate_asset.py \
  src/skills/mols-agent-asset-studio/agents/openai.yaml \
  --profile openai-interface --strict
python src/skills/mols-agent-asset-studio/scripts/validate_asset.py \
  src/skills/mols-agent-asset-tuner/agents/openai.yaml \
  --profile openai-interface --strict
python -m pytest -q tests -p no:cacheprovider
```

Package the canonical suite when validation passes:

```bash
python src/skills/mols-agent-asset-studio/scripts/package_asset_bundle.py \
  asset-bundle.yaml --output ../mols-agent-asset-studio-suite.bundle.zip
```

## Rollback

Use Git history as the primary rollback mechanism. Delete the `.tmp/` legacy
copy before committing after the diff, tests, and package contents are accepted.
Do not retain unbounded backup copies containing obsolete or sensitive content.

## Runtime Dogfooding

Install the candidate and legacy baseline into isolated target-runtime sessions,
run the supplied trigger suites, fill the generated observation sheets, and
compare them with `grade_runtime_eval.py`. Do not call migration production-ready
for a named runtime until this evidence is complete.

## v2 to v2.1

No asset name changes are required. Replace both skill directories as one coherent
upgrade because packaging, profile validation, structural validation, and
operations documentation changed together. Rebuild existing ZIP artifacts; v2.1
archives are reproducible and use manifest schema version 2.
