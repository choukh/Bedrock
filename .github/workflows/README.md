# .github/workflows

CI and deployment for Bedrock. English developer doc; see
[AGENTS.md](../../AGENTS.md). This guide lives here rather than at
`.github/README.md` on purpose: GitHub renders a `.github/README.md` as the repository
homepage in place of the root [README.md](../../README.md), so the `.github/` folder is
documented one level down instead.

## Workflows

Triggered on push to `main` (typecheck also runs on pull requests):

- `typecheck.yml`: the **proof gate**. Runs `make check` (typecheck the masters, validate i18n
  markers, prose linter, glossary check).
- `cloudflare.yml`: builds the site (root base URL) and deploys to **Cloudflare Pages**, the
  primary host ([bedrock.institute](https://bedrock.institute)).
- `pages.yml`: builds the site (base URL `/Bedrock`) and deploys the **GitHub Pages** mirror.

## Secrets

The Cloudflare deploy uses organization secrets `CLOUDFLARE_API_TOKEN` and
`CLOUDFLARE_ACCOUNT_ID` (owner-configured GitHub Actions encrypted secrets on the BedrockInstitute
org, inherited by this repo, never committed or printed). Deployment is automatic and contributors handle no credentials. The one-time owner
setup is documented at the top of `cloudflare.yml`.
