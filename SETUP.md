# Phoenix Premium V5: first installation and autonomous operation

This version is designed to run without an additional personal access token, paid API, database, third-party image host, or manual daily publishing. The GitHub-hosted workflow uses the repository's built-in `GITHUB_TOKEN` for public GitHub API reads and publishing assets.

## One-time installation

1. In the public profile repository **`BlazeDashX/BlazeDashX`**, open **Settings → Actions → General** and ensure Actions are enabled. Under **Workflow permissions**, enable **Read and write permissions**, if your repository settings expose that control. Your repository's policy must permit GitHub Actions to commit generated SVG files.
2. Upload `scripts/build_live.py`, the `tests/` directory, and `.github/workflows/phoenix-autopilot.yml` **first**. Preserve the nested `.github/workflows/` path exactly.
3. Open **Actions → Phoenix Profile Autopilot → Run workflow**. Confirm that the run is green and that `assets/live/` contains `dashboard.svg`, `activity.svg`, `pulse.svg`, `languages.svg`, `radar.svg`, `constellation.svg`, `snake.svg`, and `snake-dark.svg`.
4. Only after that first successful run, upload the full `assets/static/` folder and replace the profile `README.md` with the included version. Do not upload the README before the live images exist, or GitHub will display broken links until the workflow succeeds.
5. Remove older automation files (`metrics.yml`, `snake.yml` in the root, or old `.github/workflows/profile-refresh.yml`) if they are no longer used. Leaving multiple workflows enabled causes redundant updates.

If the default branch is named something other than `main`, change the workflow's `push.branches` filter accordingly. Scheduled runs always use the repository's default branch.

## What runs on its own

- **Every day at 03:17 UTC:** fetch public account, repository, and event metadata via GitHub REST APIs. Generate the six Phoenix-themed live SVG panels.
- **Same run:** generate light and dark contribution snake SVGs using `Platane/snk/svg-only@v3` and the built-in GitHub token.
- **Finally:** commit generated assets to the same profile repository only when their content changed, using the built-in GitHub Actions bot identity. The README links point at those generated files.
- **Manual rerun:** available any time through **Actions → Phoenix Profile Autopilot → Run workflow**.

No extra personal access token or `METRICS_TOKEN` is used. No automatic commits are made to your project repositories. This automation only updates the profile repository's generated graphics.

## Definitions (avoids misleading metrics)

- **Public repos:** owned, non-fork, non-archived public repositories, excluding the profile README repository. It is not the count of completed products.
- **Repository stars:** total stars on those public repositories.
- **Recent events:** GitHub's recent public Events API responses, filtered to about 30 days. An event is not necessarily one commit.
- **Development pulse:** count of those public events per UTC day. This is not a contribution calendar or a performance score.
- **Language footprint:** count of public owned repositories by GitHub's primary-language metadata. Not percentages of expertise or total lines of code.
- **Repository radar:** the four most recently pushed eligible public repositories.
- **Repository constellation:** up to eight recently pushed public repositories plotted using deterministic illustrative positions; node size corresponds to public star count. Lines do not represent technical dependencies.
- **Contribution snake:** rendered from GitHub's actual contribution graph by the Platane action.

GitHub says public events can be delayed and the API retains only a recent window. The panels include a generation timestamp. Private repositories are deliberately excluded.

## Maintenance and limitations

- GitHub can delay scheduled workflows, and it may disable scheduled workflows on an inactive public repository after **60 days without repository activity**. If that happens, re-enable the workflow in the Actions tab. The generated graphics remain visible but can become stale; inspect their timestamps.
- If the workflow is not allowed to push to the default branch due to branch protection, use the repository's appropriate permissions or configure a separate publication branch. The package does **not** bypass branch protection.
- If the contribution snake service fails, the workflow fails visibly; an existing valid snake image remains from the last successful run. The other generated graphics are produced earlier in the job but do not publish until the job commits. Rerun after resolving the error.
- The three original third-party counter/ranking badges can occasionally be unavailable. The autopilot panels themselves do not rely on those services.
- GitHub README files do **not** run arbitrary JavaScript. The interactive sections use GitHub-compatible `<details>` panels and internal anchors.

## Testing without publishing

Local tests require Python 3.12+ and no external packages:

```bash
python -m unittest discover -s tests -v
python scripts/build_live.py --fixture tests/data/sample_api.json --now 2026-11-05T00:00:00Z --out /tmp/phoenix-preview
```

The fixture contains **test-only sample data**. Never commit its generated numbers as real account statistics. The main workflow does not use fixtures.

## Profile-side polish

The GitHub sidebar is separate from the README. Keep its bio, avatar, website and location accurate. Pin the most substantive repos in the same order as the README's Selected Systems section. The README should not duplicate the sidebar's contact links excessively.
