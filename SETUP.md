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
3. Run **Update profile README** and **Contribution snake** from the Actions tab. The snake appears after its first successful run creates the `output` branch, then refreshes daily.

The workflows follow your repository's actual default branch. GitHub stats, typing headings, and skill icons depend on external image services. GitHub Actions has not been run locally.

Workflow references: [GitHub workflow triggers](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow) and [contribution snake](https://github.com/Platane/snk).
