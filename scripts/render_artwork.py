"""Render the profile's self-contained SVG artwork in both GitHub themes."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def palette(dark: bool) -> tuple[str, ...]:
    return (
        ("#0b1017", "#111a24", "#eef4f7", "#91a2b6", "#263547", "#c4f56a")
        if dark
        else ("#f4f7ef", "#e9efdf", "#15231d", "#526452", "#c9d5c0", "#4b7516")
    )


def hero(dark: bool) -> str:
    bg, panel, ink, muted, line, accent = palette(dark)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="420" viewBox="0 0 1200 420" role="img" aria-labelledby="title desc">
  <title id="title">Ritesh — Build. Contribute. Repeat.</title>
  <desc id="desc">A custom engineering log with a branching circuit that connects an idea to a patch and an upstream contribution.</desc>
  <defs>
    <pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="{line}" stroke-width=".7"/></pattern>
    <radialGradient id="wash"><stop stop-color="{accent}" stop-opacity=".10"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
    <linearGradient id="route" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{accent}"/><stop offset="1" stop-color="#4ea9aa"/></linearGradient>
    <style>.mono{{font-family:Consolas,'Liberation Mono',monospace}}.sans{{font-family:'Segoe UI',Arial,sans-serif}}@media(prefers-reduced-motion:reduce){{.signal{{display:none}}}}</style>
  </defs>
  <rect x="1" y="1" width="1198" height="418" rx="24" fill="{bg}" stroke="{line}"/>
  <rect x="710" y="2" width="466" height="416" rx="24" fill="url(#grid)" opacity=".7"/>
  <ellipse cx="995" cy="208" rx="245" ry="205" fill="url(#wash)"/>
  <path d="M56 79H1144" stroke="{line}"/>
  <circle cx="63" cy="45" r="5" fill="{accent}"/>
  <text x="82" y="50" fill="{muted}" font-size="14" letter-spacing="2" class="mono">RITESH17RB / ENGINEERING LOG</text>
  <text x="1144" y="50" text-anchor="end" fill="{accent}" font-size="13" letter-spacing="1" class="mono">ALWAYS A WORK IN PROGRESS</text>
  <text x="50" y="199" fill="{ink}" font-size="112" font-weight="800" letter-spacing="-6" class="sans">RITESH<tspan fill="{accent}">.</tspan></text>
  <text x="56" y="254" fill="{ink}" font-size="32" font-weight="500" letter-spacing="-.8" class="sans">Build. Contribute. Repeat.</text>
  <text x="57" y="297" fill="{muted}" font-size="18" class="mono">Full-stack products. Developer tools. Open source.</text>
  <rect x="56" y="338" width="278" height="35" rx="17.5" fill="{panel}" stroke="{line}"/>
  <text x="75" y="361" fill="{accent}" font-size="14" class="mono">idea → code → contribution</text>
  <g fill="none" stroke-linecap="round">
    <path d="M817 155H1077M887 155C922 155 916 272 957 272H1077" stroke="{line}" stroke-width="3"/>
    <path d="M817 155H887C922 155 916 272 957 272H1007C1042 272 1038 155 1077 155" stroke="url(#route)" stroke-width="3"/>
    <path d="M817 155V319M1077 155V319" stroke="{line}" stroke-dasharray="3 7"/>
  </g>
  <g stroke="{accent}" stroke-width="2" fill="{bg}">
    <circle cx="817" cy="155" r="10"/><circle cx="887" cy="155" r="7"/>
    <circle cx="957" cy="272" r="10"/><circle cx="1077" cy="155" r="10"/>
  </g>
  <circle cx="817" cy="155" r="4" fill="{accent}"/>
  <path d="M953 272H961M957 268V276M1073 155H1081M1077 151V159" stroke="{accent}" stroke-width="2"/>
  <circle class="signal" r="4" fill="{accent}"><animateMotion dur="7s" repeatCount="indefinite" path="M817 155H887C922 155 916 272 957 272H1007C1042 272 1038 155 1077 155"/></circle>
  <g fill="{muted}" font-size="14" letter-spacing="1.5" class="mono">
    <text x="817" y="127" text-anchor="middle">IDEA</text>
    <text x="957" y="310" text-anchor="middle">PATCH</text>
    <text x="1077" y="127" text-anchor="middle">UPSTREAM</text>
  </g>
  <text x="946" y="366" text-anchor="middle" fill="{ink}" font-size="17" class="mono">small diffs. real progress.</text>
</svg>
'''


def mobile_hero(dark: bool) -> str:
    bg, panel, ink, muted, line, accent = palette(dark)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="420" viewBox="0 0 600 420" role="img" aria-labelledby="title desc">
  <title id="title">Ritesh — Build. Contribute. Repeat.</title>
  <desc id="desc">Full-stack products, developer tools, and open source. A branching path from an idea to an upstream patch.</desc>
  <defs>
    <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="{line}" stroke-width=".6"/></pattern>
    <style>.mono{{font-family:Consolas,'Liberation Mono',monospace}}.sans{{font-family:'Segoe UI',Arial,sans-serif}}@media(prefers-reduced-motion:reduce){{.signal{{display:none}}}}</style>
  </defs>
  <rect x="1" y="1" width="598" height="418" rx="22" fill="{bg}" stroke="{line}"/>
  <rect x="2" y="280" width="596" height="138" rx="22" fill="url(#grid)"/>
  <circle cx="37" cy="41" r="4" fill="{accent}"/>
  <text x="52" y="46" fill="{muted}" font-size="16" letter-spacing="1.1" class="mono">RITESH17RB / ENGINEERING LOG</text>
  <path d="M34 66H566" stroke="{line}"/>
  <text x="29" y="170" fill="{ink}" font-size="108" font-weight="800" letter-spacing="-5" class="sans">RITESH<tspan fill="{accent}">.</tspan></text>
  <text x="36" y="218" fill="{ink}" font-size="31" font-weight="500" letter-spacing="-.8" class="sans">Build. Contribute. Repeat.</text>
  <text x="37" y="258" fill="{muted}" font-size="20" class="mono">products · tools · open source</text>
  <path d="M70 330H530" fill="none" stroke="{line}" stroke-width="3"/>
  <path d="M70 330H190C235 330 235 370 300 370H390C435 370 435 330 530 330" fill="none" stroke="{accent}" stroke-width="3"/>
  <g fill="{bg}" stroke="{accent}" stroke-width="2"><circle cx="70" cy="330" r="9"/><circle cx="300" cy="370" r="9"/><circle cx="530" cy="330" r="9"/></g>
  <circle class="signal" r="4" fill="{accent}"><animateMotion dur="7s" repeatCount="indefinite" path="M70 330H190C235 330 235 370 300 370H390C435 370 435 330 530 330"/></circle>
  <g fill="{muted}" font-size="16" letter-spacing="1" class="mono"><text x="70" y="307" text-anchor="middle">IDEA</text><text x="300" y="402" text-anchor="middle">PATCH</text><text x="530" y="307" text-anchor="middle">UPSTREAM</text></g>
</svg>
'''


def main() -> None:
    assets = ROOT / "assets"
    assets.mkdir(exist_ok=True)
    for mode in ("dark", "light"):
        (assets / f"hero-{mode}.svg").write_text(hero(mode == "dark"), encoding="utf-8")
        (assets / f"hero-mobile-{mode}.svg").write_text(mobile_hero(mode == "dark"), encoding="utf-8")


if __name__ == "__main__":
    main()
