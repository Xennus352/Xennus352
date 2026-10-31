"""Fetch real public GitHub data and render repository-hosted SVG cards."""
import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]


def api(path, data=None):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'Xennus-profile'}
    if os.environ.get('GITHUB_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
    payload = json.dumps(data).encode() if data else None
    if payload:
        headers['Content-Type'] = 'application/json'
    with urlopen(Request('https://api.github.com/' + path, data=payload, headers=headers), timeout=30) as response:
        return json.load(response)


def card(title, subtitle, rows, colors, updated):
    elements = [f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="300" viewBox="0 0 480 300" role="img" aria-label="{escape(title)}">',
                f'<rect x="1" y="1" width="478" height="298" rx="18" fill="#{colors["background"]}" stroke="#{colors["secondary"]}" stroke-opacity=".3"/>',
                f'<path d="M24 36h24" stroke="#{colors["accent"]}" stroke-width="4" stroke-linecap="round"/>']
    def text(x, y, value, size=14, fill=None):
        elements.append(f'<text x="{x}" y="{y}" fill="#{fill or colors["text"]}" font-family="Verdana,Arial,sans-serif" font-size="{size}">{escape(str(value))}</text>')
    text(24, 69, title, 21, colors['accent'])
    text(24, 93, subtitle, 11)
    for index, (label, value) in enumerate(rows[:5]):
        y = 130 + index * 28
        text(24, y, label)
        text(340, y, value, 16, colors['secondary'])
    text(24, 281, f'GitHub API · {updated[:10]} UTC', 10)
    return '\n'.join(elements + ['</svg>', ''])


def main():
    p = json.loads((ROOT / 'profile.json').read_text())
    user = p['github_username'] or os.environ['GITHUB_REPOSITORY_OWNER']
    account = api('users/' + user)
    repos = []
    page = 1
    while True:
        batch = api(f'users/{user}/repos?type=owner&per_page=100&page={page}')
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    owned = [r for r in repos if not r['fork']]
    languages = Counter()
    for repo in owned:
        if repo['language']:
            languages.update(api(f'repos/{user}/{repo["name"]}/languages'))
    updated = datetime.now(timezone.utc).isoformat()
    rows = [('Public repositories', account['public_repos']), ('Followers', account['followers']),
            ('Stars earned', sum(r['stargazers_count'] for r in owned)),
            ('Forks earned', sum(r['forks_count'] for r in owned))]
    contributions = None
    if os.environ.get('GITHUB_TOKEN'):
        response = api('graphql', {'query': 'query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{totalContributions}}}}', 'variables': {'login':user}})
        if response.get('errors'):
            raise RuntimeError(response['errors'])
        contributions = response['data']['user']['contributionsCollection']['contributionCalendar']['totalContributions']
        rows.append(('Contributions · past year', contributions))
    total = sum(languages.values())
    language_rows = [(name, f'{count / total:.1%}') for name, count in languages.most_common(5)]
    if not language_rows:
        language_rows = [('No public language data', '—')]
    assets = ROOT / 'assets'
    assets.mkdir(exist_ok=True)
    (assets / 'github-stats.svg').write_text(card('GitHub activity', '@' + user + ' · public profile', rows, p['theme'], updated))
    (assets / 'top-languages.svg').write_text(card('Code in the wild', 'Public non-fork repositories · share of code bytes', language_rows, p['theme'], updated))
    (assets / 'github-data.json').write_text(json.dumps({'username':user, 'updated_at':updated, 'public_repos':account['public_repos'], 'followers':account['followers'], 'stars':sum(r['stargazers_count'] for r in owned), 'forks':sum(r['forks_count'] for r in owned), 'contributions_past_year':contributions, 'language_bytes':dict(languages)}, indent=2) + '\n')
    print(f'Updated stats for {user} from {len(repos)} public repositories')


if __name__ == '__main__':
    main()
