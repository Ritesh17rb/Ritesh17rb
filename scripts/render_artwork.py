"""Generate theme-aware profile artwork from public GitHub data."""

from html import escape
from pathlib import Path
import json
import textwrap

ROOT = Path(__file__).resolve().parents[1]


def palette(dark):
    return (("#0d1117", "#f0f6fc", "#9198a1", "#30363d", "#58a6ff") if dark
            else ("#ffffff", "#1f2328", "#59636e", "#d1d9e0", "#0969da"))


def svg(width, height, content, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">'
            f'<title id="title">{escape(title)}</title>'
            '<style>text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}</style>'
            + content + '</svg>\n')


def hero(data, dark, mobile=False):
    bg, ink, muted, line, accent = palette(dark)
    w, h = (600, 300) if mobile else (1000, 236)
    merged, opened = int(data['merged_count']), int(data['open_count'])
    if merged < 0 or opened < 0:
        raise ValueError('Contribution counts cannot be negative')
    content = f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="12" fill="{bg}" stroke="{line}"/>'
    content += f'<path d="M32 32h36" stroke="{accent}" stroke-width="3"/>'
    content += f'<text x="32" y="97" font-size="52" font-weight="650" letter-spacing="-2" fill="{ink}">Ritesh</text>'
    content += f'<text x="34" y="137" font-size="{22 if mobile else 20}" fill="{ink}">AI Engineer at Straive</text>'
    content += f'<text x="34" y="172" font-size="{22 if mobile else 17}" fill="{muted}">Developer tools · Data systems · Open source</text>'
    if mobile:
        content += f'<path d="M34 200h532" stroke="{line}"/>'
        positions = [(34, merged, 'merged upstream PRs'), (310, opened, 'open upstream PRs')]
        y = 245
    else:
        content += f'<path d="M660 48v140" stroke="{line}"/>'
        positions = [(700, merged, 'Merged PRs'), (850, opened, 'Open PRs')]
        y = 112
    for x, value, label in positions:
        content += f'<text x="{x}" y="{y}" font-size="36" font-weight="600" fill="{accent}">{value}</text>'
        content += f'<text x="{x}" y="{y+26}" font-size="{20 if mobile else 14}" fill="{muted}">{label}</text>'
    if not mobile:
        content += f'<text x="700" y="185" font-size="12" fill="{muted}">GitHub · {escape(data["updated_at"])}</text>'
    return svg(w, h, content, 'Ritesh — AI Engineer at Straive. Live upstream contribution counts.')


def project_card(project, dark, mobile=False):
    bg, ink, muted, line, accent = palette(dark)
    w = 600 if mobile else 1000
    title = project['name']
    description = project['description']
    lines = textwrap.wrap(description, width=46 if mobile else 110)
    h = (112 + 28 * min(3, len(lines))) if mobile else (106 + 24 * min(2, len(lines)))
    content = f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="10" fill="{bg}" stroke="{line}"/>'
    content += f'<text x="28" y="40" font-size="{28 if mobile else 23}" font-weight="600" fill="{ink}">{escape(title)}</text>'
    content += f'<text x="{w-36}" y="40" text-anchor="end" font-size="23" fill="{accent}">↗</text>'
    for i, text in enumerate(lines[:3 if mobile else 2]):
        content += f'<text x="28" y="{(80+i*28) if mobile else (76+i*24)}" font-size="{22 if mobile else 16}" fill="{muted}">{escape(text)}</text>'
    content += f'<circle cx="33" cy="{h-23}" r="4" fill="{accent}"/>'
    content += f'<text x="46" y="{h-19}" font-size="{20 if mobile else 12}" fill="{muted}">{escape(project["language"] or "Source code")}</text>'
    content += f'<text x="{w-28}" y="{h-19}" text-anchor="end" font-size="{20 if mobile else 12}" fill="{muted}">View repository</text>'
    return svg(w, h, content, f'{title}: {description}')


def write_assets(data):
    assets = ROOT / 'assets'
    assets.mkdir(exist_ok=True)
    for mode in ('dark', 'light'):
        for mobile in (False, True):
            suffix = f'{"mobile-" if mobile else ""}{mode}'
            (assets / f'hero-{suffix}.svg').write_text(hero(data, mode == 'dark', mobile), encoding='utf-8')
            for project in data['projects']:
                (assets / f'{project["name"]}-{suffix}.svg').write_text(
                    project_card(project, mode == 'dark', mobile), encoding='utf-8')


if __name__ == '__main__':
    write_assets(json.loads((ROOT / 'assets/profile-data.json').read_text(encoding='utf-8')))
