"""Generate the public profile from profile.json; Python 3.9+, no dependencies."""
import argparse
import html
import json
import os
from datetime import date
from pathlib import Path
from urllib.parse import quote, urlencode, urlsplit
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]


def esc(value):
    return html.escape(str(value), quote=True)


def image(url, alt, width=None):
    size = f' width="{width}"' if width else ''
    return f'<img src="{esc(url)}" alt="{esc(alt)}"{size} />'


def render(p):
    user = p['github_username'] or os.environ.get('GITHUB_REPOSITORY_OWNER', '')
    repo = p['repository'] or os.environ.get('GITHUB_REPOSITORY', '') or (f'{user}/{user}' if user else '')
    ZoneInfo(p['timezone'])
    colors = p['theme']
    for color in colors.values():
        if len(color) != 6 or any(c not in '0123456789abcdefABCDEF' for c in color):
            raise ValueError('Colors must be six hexadecimal digits without #')
    lines = ['<!-- Generated from profile.json. See SETUP.md for customization. -->',
             '<div align="center">', f'<h1>{esc(p["name"])}</h1>']
    if p['typing_lines']:
        query = urlencode(dict(font='Fira Code', size=24, pause=1000, color=colors['accent'],
                               center='true', vCenter='true', width=600, lines=';'.join(p['typing_lines'])))
        lines.append(image('https://readme-typing-svg.demolab.com/?' + query, 'Interests and focus'))
    if p['tagline']:
        lines.append(f'<p><em>{esc(p["tagline"])}</em></p>')
    details = [esc(p[k]) for k in ('location', 'timezone') if p[k]]
    if details:
        lines.append(f'<p>{" · ".join(details)}</p>')
    contacts = []
    for label, url in p['links'].items():
        if urlsplit(url).scheme not in {'https', 'http', 'mailto'}:
            raise ValueError(f'Unsupported URL for {label}')
        contacts.append(f'<a href="{esc(url)}">{esc(label)}</a>')
    if contacts:
        lines.append(f'<p>{" · ".join(contacts)}</p>')
    lines.extend(['</div>', ''])
    if p['currently']:
        lines.extend(['### Currently', '', f'<p>{esc(p["currently"])}</p>', ''])
    if p['setup']:
        lines.extend(['### My setup', '', '<ul>'])
        lines.extend(f'<li><strong>{esc(k)}:</strong> {esc(v)}</li>' for k, v in p['setup'].items())
        lines.extend(['</ul>', ''])
    if any(p['tech_stack'].values()):
        lines.extend(['### Tech stack', ''])
        for label, skills in p['tech_stack'].items():
            if skills:
                query = urlencode(dict(i=','.join(skills), perline=8, theme='dark'))
                lines.extend([f'<p><strong>{esc(label)}</strong></p>',
                              image('https://skillicons.dev/icons?' + query, f'{label}: {", ".join(skills)}'), ''])
    if p['milestones']:
        lines.extend(['### Timeline', '', '<ul>'])
        for event in p['milestones']:
            start = date.fromisoformat(event['start'])
            end = date.fromisoformat(event['end']) if event.get('end') else None
            if end and end < start:
                raise ValueError('Milestone end precedes its start')
            period = f'{start:%b %Y} – {end.strftime("%b %Y") if end else "Present"}'
            location = f' · {esc(event["location"])}' if event.get('location') else ''
            description = f'<br>{esc(event["description"])}' if event.get('description') else ''
            lines.append(f'<li><strong>{esc(event["title"])}</strong>{location}<br>{period}{description}</li>')
        lines.extend(['</ul>', ''])
    if p['sections']['stats'] and user:
        query = dict(username=user, hide_border='true', bg_color=colors['background'],
                     title_color=colors['accent'], icon_color=colors['secondary'], text_color=colors['text'])
        base = 'https://github-readme-stats-eight-theta.vercel.app/api'
        lines.extend(['### GitHub stats', '', '<div align="center">',
                      image(base + '?' + urlencode({**query, 'show_icons':'true'}), f"{user}'s GitHub stats", '48%'),
                      image(base + '/top-langs/?' + urlencode({**query, 'layout':'compact'}), 'Top languages', '48%'), '</div>', ''])
    if p['sections']['snake'] and repo:
        raw = 'https://raw.githubusercontent.com/' + quote(repo, safe='/') + '/output/'
        lines.extend(['### Contributions', '', '<picture>',
                      f'<source media="(prefers-color-scheme: dark)" srcset="{raw}github-contribution-grid-snake-dark.svg">',
                      image(raw + 'github-contribution-grid-snake.svg', 'Contribution snake animation'), '</picture>', ''])
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--config', type=Path, default=ROOT / 'profile.json')
    parser.add_argument('--output', type=Path, default=ROOT / 'README.md')
    args = parser.parse_args()
    content = render(json.loads(args.config.read_text()))
    if args.check:
        if not args.output.exists() or args.output.read_text() != content:
            raise SystemExit('README is outdated. Run python3 scripts/render_profile.py')
        print('README matches profile.json')
    else:
        args.output.write_text(content)
        print(f'Generated {args.output.name}')


if __name__ == '__main__':
    main()
