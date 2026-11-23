"""Refresh contributions and project artwork from public GitHub data."""

import argparse
from datetime import datetime, timezone
import html
import json
from pathlib import Path
import re
import subprocess

from render_artwork import write_assets

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- UPSTREAM:START -->"
END = "<!-- UPSTREAM:END -->"
USER = "Ritesh17rb"
PROJECTS = ("rag-audit", "schemaport", "skill-fit", "swiftcart")


def escape_cell(value):
    escaped = html.escape(" ".join(value.split()), quote=True)
    return re.sub(r"([\\`*_\[\]])", r"\\\1", escaped).replace("|", "&#124;")


def render(items):
    candidates = []
    seen = set()
    for item in items:
        match = re.fullmatch(r"https://github\.com/([A-Za-z0-9-]+)/([A-Za-z0-9_.-]+)/pull/(\d+)", item['html_url'])
        if match is None:
            raise ValueError("Unexpected pull-request URL")
        owner, repo, number = match.groups()
        if owner.lower() == USER.lower() or item['html_url'] in seen:
            continue
        seen.add(item['html_url'])
        status = ('Merged' if item['pull_request'].get('merged_at')
                  else 'Open' if item['state'] == 'open' else 'Closed')
        candidates.append((item, owner, repo, number, status))
    # Show accepted work alongside current contributions, without hiding either.
    merged = [row for row in candidates if row[-1] == 'Merged'][:3]
    opened = [row for row in candidates if row[-1] == 'Open'][:6-len(merged)]
    closed = [row for row in candidates if row[-1] == 'Closed'][:6-len(merged)-len(opened)]
    selected = merged + opened + closed
    if not selected:
        raise ValueError("No upstream pull requests returned; keeping existing content")
    rows = [f'| **{escape_cell(owner)}/{escape_cell(repo)}** | [{escape_cell(item["title"])} · #{number}]({item["html_url"]}) | {status} |'
            for item, owner, repo, number, status in selected]
    return '\n'.join(['| Project | Contribution | Status |', '| :--- | :--- | :--- |', *rows])


def replace_section(readme, section, start=START, end=END):
    if readme.count(start) != 1 or readme.count(end) != 1 or readme.index(start) > readme.index(end):
        raise ValueError("Expected exactly one correctly ordered managed section")
    before, rest = readme.split(start)
    _, after = rest.split(end)
    return f'{before}{start}\n{section}\n{end}{after}'


def github(endpoint, **params):
    command = ['gh', 'api', endpoint, '--method', 'GET']
    for key, value in params.items():
        command.extend(['-f', f'{key}={value}'])
    process = subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8')
    return json.loads(process.stdout)


def fetch_profile():
    query = f'is:pr is:public author:{USER} -user:{USER}'
    result = github('search/issues', q=query, sort='updated', order='desc', per_page=100)
    merged = github('search/issues', q=f'{query} is:merged', per_page=1)
    opened = github('search/issues', q=f'{query} is:open', per_page=1)
    if any(response.get('incomplete_results') for response in (result, merged, opened)):
        raise ValueError('Incomplete GitHub search; keeping existing content')
    projects = []
    for name in PROJECTS:
        repo = github(f'repos/{USER}/{name}')
        if repo['fork'] or repo['private'] or repo['owner']['login'].lower() != USER.lower():
            raise ValueError('Featured projects must be public repositories owned by the profile')
        fallback = ('A full-stack commerce application with authentication and payments.'
                    if name == 'swiftcart' else 'Explore the source code and project documentation.')
        projects.append({
            'name': repo['name'], 'description': repo['description'] or fallback,
            'language': repo['language'], 'url': repo['html_url'], 'homepage': repo['homepage'],
        })
    # Retain only the public fields needed to render the profile.
    items = [{key: item[key] for key in ('html_url', 'title', 'state', 'pull_request')}
             for item in result['items']]
    return {
        'updated_at': datetime.now(timezone.utc).strftime('%d %b %Y'),
        'merged_count': merged['total_count'], 'open_count': opened['total_count'],
        'items': items, 'projects': projects,
    }


def render_projects(projects):
    cards = []
    for project in projects:
        name = project['name']
        if name not in PROJECTS or project['url'] != f'https://github.com/{USER}/{name}':
            raise ValueError('Unexpected featured repository')
        alt = html.escape(f'{name}: {project["description"]}', quote=True)
        cards.append(f'''<p><a href="{project['url']}">
  <picture>
    <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="./assets/{name}-mobile-dark.svg">
    <source media="(max-width: 600px) and (prefers-color-scheme: light)" srcset="./assets/{name}-mobile-light.svg">
    <source media="(prefers-color-scheme: dark)" srcset="./assets/{name}-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./assets/{name}-light.svg">
    <img src="./assets/{name}-light.svg" width="1000" alt="{alt}">
  </picture>
</a></p>''')
    if not cards:
        raise ValueError('No projects returned; keeping existing content')
    return '\n\n'.join(cards)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, help='Use a saved profile-data.json snapshot')
    parser.add_argument('--check', action='store_true', help='Check sections without writing')
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding='utf-8')) if args.input else fetch_profile()
    current = (ROOT / 'README.md').read_text(encoding='utf-8-sig')
    updated = replace_section(current, render(data['items']))
    updated = replace_section(updated, render_projects(data['projects']), '<!-- PROJECTS:START -->', '<!-- PROJECTS:END -->')
    if args.check:
        if current != updated:
            raise SystemExit('Profile sections need a refresh')
        print('Profile sections are current')
        return
    # Network requests and section validation finish before any file is replaced.
    write_assets(data)
    (ROOT / 'assets/profile-data.json').write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'README.md').write_text(updated, encoding='utf-8')
    print('Updated project cards, upstream work, and contribution counts')


if __name__ == '__main__':
    main()
