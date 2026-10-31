# Customize your profile

Edit `profile.json`, then run:

```sh
python3 scripts/render_profile.py
python3 scripts/render_profile.py --check
```

Requires Python 3.9+ with timezone data; no Python packages are needed. GitHub Actions also regenerates the README when configuration changes reach your default branch. Edit the config instead of the generated README.

## Your details

Configured for **Xennus352**, with Arch Linux, Hyprland, your portfolio, email, and Telegram. The display name is Xennus. The timezone is taken from this workspace (`Asia/Yangon`); change it if needed. No city, job history, dates, or programming languages have been assumed. Empty sections stay hidden. Anime content and its automation have been removed.

| Field | Customization |
| --- | --- |
| `name` | Display name |
| `github_username` | Account used for GitHub stats and contributions |
| `repository` | Repository hosting the profile, as `owner/repo` |
| `tagline` | Short introduction |
| `typing_lines` | Array of lines for the animated heading |
| `location`, `timezone` | City/country and IANA timezone |
| `currently` | Current work or learning |
| `setup` | Any labels and values for OS, desktop, editor, terminal, hardware |
| `tech_stack` | Named groups of Skill Icons identifiers |
| `milestones` | Dated work, education, projects, or setup history |
| `links` | Labels mapped to full HTTPS or mailto URLs |
| `theme` | Six-digit colors without `#` |
| `sections` | Turn stats and the snake animation on or off |

Blank `github_username` and `repository` values use the repository owner and current repository in Actions. For a local preview, keep these fields set explicitly.

## Add stacks and dates

Replace the corresponding fields with your actual tools and dates. These are examples, not claims about your experience:

```json
{
  "typing_lines": ["Your focus", "What you're learning"],
  "tech_stack": {
    "Languages": ["python", "ts"],
    "Frameworks": ["react", "flutter"],
    "Tools": ["git", "docker", "linux"]
  },
  "milestones": [
    {
      "title": "Your role, course, or project",
      "start": "2025-01-01",
      "end": "",
      "location": "Remote",
      "description": "A short description"
    }
  ]
}
```

Dates use `YYYY-MM-DD` and display month/year. Empty or omitted `end` means “Present.” Supported icons are listed in the [Skill Icons catalog](https://github.com/tandpfun/skill-icons#icons-list).

## Put it on your GitHub profile

1. Create the public repository `Xennus352/Xennus352` and push these files there. This local checkout still points to the original author's repository, so update `origin` to your repository before pushing:

   ```sh
   git remote set-url origin https://github.com/Xennus352/Xennus352.git
   ```

2. Enable Actions if prompted. The workflows request `contents: write` to save generated files; your repository or organization policy must allow this.
3. Run **Update profile README** from the Actions tab. This workflow fetches your real GitHub data, generates both snake themes, and saves all images beside the README in `assets/`. It refreshes daily and after profile changes.

The workflow follows your repository's actual default branch. Stats and the snake are hosted in this repository. Contact badges, typing headings, and skill icons use external image services.

## What the statistics mean

`scripts/github_stats.py` reads GitHub's API as the account in `github_username`. It writes `assets/github-data.json` and two SVG cards. Repository and follower counts come from your public account. Stars and forks are summed across public repositories you own, excluding forks. Language percentages represent code bytes in your public non-fork repositories, not proficiency or time spent coding. Contributions cover the past year as returned by GitHub's contribution calendar with the workflow token. Private repository details are not requested. The cards show their refresh date; these are daily snapshots, not live counters.

The workflow uses its built-in `GITHUB_TOKEN`; no extra personal access token or stats hosting is required. If an API request fails, the workflow fails before publishing new cards, preserving the previous snapshot. To refresh manually, use **Actions → Update profile README → Run workflow**.

Workflow references: [GitHub workflow triggers](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow) and [contribution snake](https://github.com/Platane/snk).
