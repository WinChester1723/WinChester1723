"""Generate animated SVG assets for the GitHub profile README (same style as assets/header.svg).

Usage: python tools/make_assets.py   (from github-profile/)
Outputs: assets/card-<repo>.svg, assets/stack.svg, assets/divider.svg

Facts on cards come from each repo's .csproj / files (checked 2026-10-02). Keep them true.
Animation: one-time entrance only (transform/opacity), respects prefers-reduced-motion.
SVGs are embedded via <img>, so no web fonts / scripts / links inside — links live in Markdown.
"""
from html import escape
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

BASE_STYLE = """
    .sans { font-family: 'Segoe UI', 'Inter', -apple-system, 'Helvetica Neue', Arial, sans-serif; }
    .mono { font-family: 'Cascadia Code', 'JetBrains Mono', Consolas, 'SF Mono', Menlo, monospace; }
    .rise { opacity: 0; animation: rise .8s cubic-bezier(.22,1,.36,1) forwards; }
    @keyframes rise { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
    .draw { transform: scaleX(0); animation: draw 1.1s cubic-bezier(.22,1,.36,1) forwards; }
    @keyframes draw { to { transform: scaleX(1); } }
    @media (prefers-reduced-motion: reduce) {
      .rise, .draw { animation: none; opacity: 1; transform: none; }
    }
"""

CARDS = [
    {
        "slug": "integration-service",
        "icon": "sync",
        "desc": ["ASP.NET Core service that syncs stock and", "loyalty data with a 1C system"],
        "chips": ["ASP.NET Core", "SignalR", ".NET 9"],
    },
    {
        "slug": "service-bus-demo",
        "icon": "queue",
        "desc": ["Azure Service Bus queue consumed by an", "Azure Function (batched trigger)"],
        "chips": ["Azure Functions", "Service Bus", ".NET 8"],
    },
    {
        "slug": "OcelotDemo",
        "icon": "gateway",
        "desc": ["API gateway routing to a downstream", "service with Ocelot"],
        "chips": ["Ocelot", "ASP.NET Core", "Swagger"],
    },
    {
        "slug": "demoBookStoreSOAP",
        "icon": "soap",
        "desc": ["Layered SOAP web service with EF Core,", "Elasticsearch, Docker Compose and tests"],
        "chips": ["SoapCore", "EF Core", "xUnit + Moq"],
    },
    {
        "slug": "DemoElasticSearch",
        "icon": "search",
        "desc": ["Search queries against Elasticsearch", "from a .NET console app"],
        "chips": ["Elasticsearch", "NEST", ".NET 8"],
    },
    {
        "slug": "winchester1723.github.io",
        "icon": "web",
        "desc": ["Personal portfolio — selected work,", "experience and CV downloads"],
        "chips": ["HTML", "CSS", "JavaScript"],
    },
]

# Minimal line icons (24x24 grid), stroke-only
ICONS = {
    "sync": '<path d="M4 12a8 8 0 0 1 13.7-5.6L20 8"/><path d="M20 3v5h-5"/><path d="M20 12a8 8 0 0 1-13.7 5.6L4 16"/><path d="M4 21v-5h5"/>',
    "queue": '<rect x="3" y="5" width="18" height="4" rx="1"/><rect x="3" y="10" width="18" height="4" rx="1"/><rect x="3" y="15" width="18" height="4" rx="1"/>',
    "gateway": '<path d="M3 12h6"/><path d="M15 6h6"/><path d="M15 12h6"/><path d="M15 18h6"/><path d="M9 12l6-6M9 12h6M9 12l6 6"/>',
    "soap": '<path d="M8 4H5v16h3"/><path d="M16 4h3v16h-3"/><path d="M9.5 9h5M9.5 12h5M9.5 15h3"/>',
    "search": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M20 20l-4.8-4.8"/>',
    "web": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a14 14 0 0 1 0 18a14 14 0 0 1 0-18"/>',
}

CHIP_CHAR_W = 7.6   # approx. width per char at 13px mono
CHIP_PAD = 12


def card_svg(card: dict, index: int) -> str:
    w, h = 440, 176
    delay = 0.08 + (index % 2) * 0.12
    name = escape(card["slug"])
    desc = "".join(
        f'<text x="24" y="{92 + i * 22}" class="sans desc">{escape(line)}</text>' for i, line in enumerate(card["desc"])
    )
    chips, x = [], 24
    for chip in card["chips"]:
        cw = len(chip) * CHIP_CHAR_W + CHIP_PAD * 2
        chips.append(
            f'<g transform="translate({x:.0f} 134)"><rect width="{cw:.0f}" height="24" rx="5" class="chip"/>'
            f'<text x="{cw / 2:.0f}" y="16.5" text-anchor="middle" class="mono chip-t">{escape(chip)}</text></g>'
        )
        x += cw + 8
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t">
  <title id="t">{name}: {escape(' '.join(card['desc']))}</title>
  <defs>
    <radialGradient id="g" cx="100%" cy="0%" r="90%">
      <stop offset="0" stop-color="#3b82f6" stop-opacity="0.16"/><stop offset="1" stop-color="#3b82f6" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="rule" x1="0" x2="1"><stop offset="0" stop-color="#3b82f6"/><stop offset="1" stop-color="#3b82f6" stop-opacity="0"/></linearGradient>
  </defs>
  <style>{BASE_STYLE}
    .name {{ font-size: 18px; font-weight: 600; fill: #e6eaf2; }}
    .desc {{ font-size: 15px; fill: #a3aec2; }}
    .chip {{ fill: #94a3b8; fill-opacity: .07; stroke: #94a3b8; stroke-opacity: .22; }}
    .chip-t {{ font-size: 12px; fill: #a3aec2; }}
    .icon {{ fill: none; stroke: #7fb0ff; stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round; }}
    .arrow {{ fill: none; stroke: #6f7b91; stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round; }}
    .rule {{ transform-origin: 24px 0; }}
  </style>
  <rect width="{w}" height="{h}" rx="14" fill="#0f1627"/>
  <rect width="{w}" height="{h}" rx="14" fill="url(#g)"/>
  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="13.5" fill="none" stroke="#94a3b8" stroke-opacity=".16"/>
  <g class="rise" style="animation-delay:{delay:.2f}s">
    <g transform="translate(24 24)"><rect width="32" height="32" rx="8" fill="#3b82f6" fill-opacity=".12" stroke="#3b82f6" stroke-opacity=".38"/>
      <g transform="translate(5 5) scale(.917)" class="icon">{ICONS[card['icon']]}</g></g>
    <text x="68" y="46" class="mono name">{name}</text>
    <g transform="translate({w - 40} 32)" class="arrow"><path d="M2 14L14 2M5 2h9v9"/></g>
  </g>
  <rect x="24" y="68" width="160" height="1.5" fill="url(#rule)" class="draw rule" style="animation-delay:{delay + 0.25:.2f}s"/>
  <g class="rise" style="animation-delay:{delay + 0.15:.2f}s">{desc}</g>
  <g class="rise" style="animation-delay:{delay + 0.3:.2f}s">{''.join(chips)}</g>
</svg>
"""


STACK = ["X++", "C#", ".NET", "ASP.NET Core", "SQL Server", "OData", "SOAP", "SSRS",
         "Azure DevOps", "Docker", "AKS", "Python"]


def stack_svg() -> str:
    w, h = 1200, 64
    chips, x, char_w, pad = [], 0, 9.2, 16
    for i, item in enumerate(STACK):
        cw = len(item) * char_w + pad * 2
        chips.append(
            f'<g transform="translate({x:.0f} 12)"><g class="rise" style="animation-delay:{0.05 + i * 0.07:.2f}s">'
            f'<rect width="{cw:.0f}" height="38" rx="8" class="chip"/>'
            f'<text x="{cw / 2:.0f}" y="24.5" text-anchor="middle" class="mono t">{escape(item)}</text></g></g>'
        )
        x += cw + 10
    total = x - 10
    offset = (w - total) / 2
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t">
  <title id="t">Stack: {escape(', '.join(STACK))}</title>
  <style>{BASE_STYLE}
    .chip {{ fill: #0f1627; stroke: #94a3b8; stroke-opacity: .24; }}
    .t {{ font-size: 15px; fill: #e6eaf2; }}
  </style>
  <g transform="translate({offset:.0f} 0)">{''.join(chips)}</g>
</svg>
"""


def divider_svg() -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="24" viewBox="0 0 1200 24" role="presentation">
  <defs><linearGradient id="l" x1="0" x2="1">
    <stop offset="0" stop-color="#94a3b8" stop-opacity="0"/><stop offset=".5" stop-color="#3b82f6" stop-opacity=".7"/><stop offset="1" stop-color="#94a3b8" stop-opacity="0"/>
  </linearGradient></defs>
  <style>{BASE_STYLE}
    .draw {{ transform-origin: 600px 12px; }}
  </style>
  <rect x="0" y="11.5" width="1200" height="1" fill="url(#l)" class="draw"/>
  <circle cx="600" cy="12" r="3" fill="#3b82f6" class="rise" style="animation-delay:.6s"/>
</svg>
"""


BUTTONS = [
    # slug, label, icon, primary
    ("portfolio", "Portfolio", "web", True),
    ("linkedin", "LinkedIn", "linkedin", False),
    ("cv-d365", "CV · D365 F&O", "download", False),
    ("cv-net", "CV · .NET", "download", False),
]

BUTTON_ICONS = {
    "web": ICONS["web"],
    "download": '<path d="M12 4v11"/><path d="M7 10l5 5 5-5"/><path d="M5 20h14"/>',
    "linkedin": '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M8 10v7"/><path d="M8 7v.01"/><path d="M12 17v-4a2 2 0 0 1 4 0v4"/><path d="M12 10v7"/>',
}


def button_svg(label: str, icon: str, primary: bool, index: int) -> str:
    h, char_w, pad, icon_w = 48, 9.4, 22, 26
    w = int(len(label) * char_w + pad * 2 + icon_w)
    delay = 0.1 + index * 0.12
    fill = "#3b82f6" if primary else "#0f1627"
    stroke = "#ffffff" if primary else "#94a3b8"
    stroke_op = ".10" if primary else ".30"
    text = "#ffffff" if primary else "#e6eaf2"
    icon_c = "#ffffff" if primary else "#7fb0ff"
    sheen = (
        f'<rect x="-60" y="0" width="40" height="{h}" fill="url(#sheen)" class="sheen" style="animation-delay:{delay + 0.7:.2f}s"/>'
        if primary else ""
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">
  <defs>
    <linearGradient id="sheen" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <clipPath id="c"><rect width="{w}" height="{h}" rx="9"/></clipPath>
  </defs>
  <style>{BASE_STYLE}
    .label {{ font-size: 16px; font-weight: 600; fill: {text}; }}
    .ic {{ fill: none; stroke: {icon_c}; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }}
    .sheen {{ animation: sheen 1.1s cubic-bezier(.65,0,.35,1) forwards; }}
    @keyframes sheen {{ to {{ transform: translateX({w + 120}px); }} }}
    @media (prefers-reduced-motion: reduce) {{ .sheen {{ display: none; }} }}
  </style>
  <g class="rise" style="animation-delay:{delay:.2f}s">
    <g clip-path="url(#c)">
      <rect width="{w}" height="{h}" fill="{fill}"/>
      {sheen}
    </g>
    <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="8.5" fill="none" stroke="{stroke}" stroke-opacity="{stroke_op}"/>
    <g transform="translate({pad} 14) scale(.83)" class="ic">{BUTTON_ICONS[icon]}</g>
    <text x="{pad + icon_w}" y="29.5" class="sans label">{escape(label)}</text>
  </g>
</svg>
"""


def main():
    ASSETS.mkdir(exist_ok=True)
    for i, (slug, label, icon, primary) in enumerate(BUTTONS):
        (ASSETS / f"btn-{slug}.svg").write_text(button_svg(label, icon, primary, i), encoding="utf-8", newline="\n")
    for i, card in enumerate(CARDS):
        (ASSETS / f"card-{card['slug']}.svg").write_text(card_svg(card, i), encoding="utf-8", newline="\n")
    (ASSETS / "stack.svg").write_text(stack_svg(), encoding="utf-8", newline="\n")
    (ASSETS / "divider.svg").write_text(divider_svg(), encoding="utf-8", newline="\n")
    print("written:", sorted(p.name for p in ASSETS.glob("*.svg")))


if __name__ == "__main__":
    main()
