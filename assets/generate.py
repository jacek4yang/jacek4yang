#!/usr/bin/env python3
"""Generate all visual assets for the jacek4yang profile.

Outputs (in assets/):
  hero.svg / hero.png        README hero (2x for retina)
  mono.svg                   inline monogram used as the README prefix glyph
  avatar-source.svg          avatar master
  avatar-1024/512/256/64.png avatar exports
  favicon.svg / favicon.png  Pages favicon
  og-image.png               social preview card

Deterministic: no randomness, no network, no external images.

SVG-only mode: `python generate.py --svg-only` writes the SVG sources and
skips PNG export (PNGs are then rendered by `node render.js`, which uses
@resvg/resvg-js; useful on machines without native cairo).
"""

import os
import sys

if "--svg-only" not in sys.argv:
    import cairosvg

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- tokens ----
BG = "#05070d"
SURFACE = "#0b0f18"
GRID = "#1a2230"
FG = "#e8edf5"
FG_DIM = "#8b95a7"
ACCENT = "#5eead4"      # cyan
ACCENT2 = "#7c8cf8"     # violet
BLUE = "#4cc2ff"        # electric blue

FONT = "ui-monospace, 'Cascadia Code', 'JetBrains Mono', Menlo, Consolas, monospace"


# ---------------------------------------------------------------- helpers ---
def hex_to_rgb(h: str) -> tuple:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(c1: str, c2: str, t: float) -> str:
    a, b = hex_to_rgb(c1), hex_to_rgb(c2)
    return "#%02x%02x%02x" % tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def grid_pattern(pid: str, size: int = 32, stroke: str = GRID, opacity: float = 0.5) -> str:
    return (
        f'<pattern id="{pid}" width="{size}" height="{size}" patternUnits="userSpaceOnUse">'
        f'<path d="M {size} 0 L 0 0 0 {size}" fill="none" stroke="{stroke}" '
        f'stroke-width="1" opacity="{opacity}"/></pattern>'
    )


def write(name: str, content: str) -> str:
    path = os.path.join(HERE, name)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    return path


def svg_to_png(svg_path: str, png_path: str, width: int) -> None:
    if "cairosvg" not in sys.modules:
        return  # svg-only mode; PNGs rendered separately via render.js
    cairosvg.svg2png(url=svg_path, write_to=os.path.join(HERE, png_path), output_width=width)


# ------------------------------------------------------------------- hero ---
# 1600x640. Layered: grid -> topology -> packets -> frame -> wordmark.
def build_hero() -> str:
    W, H = 1600, 640

    # ---- deterministic network topology ---------------------------------
    # nodes placed on a loose hex lattice; edges connect near neighbours
    import math
    nodes = []
    cols, rows = 22, 7
    for r in range(rows):
        for c in range(cols):
            x = 60 + c * 70 + (35 if r % 2 else 0)
            y = 90 + r * 78
            # deterministic drift so the lattice is not mechanically regular
            dx = 14 * math.sin(c * 1.7 + r * 0.9)
            dy = 11 * math.cos(c * 0.6 + r * 1.3)
            # fade nodes toward the centre where the wordmark sits
            cx, cy = W / 2, H / 2
            d = math.hypot((x + dx) - cx, (y + dy) - cy)
            fade = max(0.0, min(1.0, (d - 320) / 300))
            nodes.append((x + dx, y + dy, fade, c, r))

    def near(a, b):
        (x1, y1, _, c1, r1), (x2, y2, _, c2, r2) = a, b
        return abs(c1 - c2) + abs(r1 - r2) == 1 or (abs(c1 - c2) == 1 and r1 != r2 and abs(r1 - r2) == 1)

    edges, edge_mid = [], []
    for i, a in enumerate(nodes):
        for b in nodes[i + 1:]:
            if near(a, b):
                edges.append((a, b))

    top = []
    top.append(f'<rect width="{W}" height="{H}" fill="{SURFACE}"/>')
    top.append(f'<rect width="{W}" height="{H}" fill="url(#hg)"/>')
    # vignette to keep centre readable
    top.append(
        f'<radialGradient id="vig" cx="50%" cy="50%" r="72%">'
        f'<stop offset="0%" stop-color="{BG}" stop-opacity="0.88"/>'
        f'<stop offset="55%" stop-color="{BG}" stop-opacity="0.55"/>'
        f'<stop offset="100%" stop-color="{BG}" stop-opacity="0.05"/></radialGradient>'
    )
    top.append(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')

    net = ['<g stroke-linecap="round">']
    for (a, b) in edges:
        fade = min(a[2], b[2])
        if fade <= 0.02:
            continue
        op = 0.10 + 0.30 * fade
        col = ACCENT if (a[3] + a[4]) % 5 == 0 else GRID
        net.append(
            f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" '
            f'stroke="{col}" stroke-width="1" opacity="{op:.2f}"/>'
        )
    net.append('</g>')

    dots = ['<g>']
    for (x, y, fade, c, r) in nodes:
        if fade <= 0.03:
            continue
        op = 0.25 + 0.6 * fade
        col = ACCENT if (c + r) % 7 == 0 else mix(GRID, FG_DIM, fade * 0.6)
        rad = 2.2 if (c + r) % 7 else 3.0
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad}" fill="{col}" opacity="{op:.2f}"/>')
    dots.append('</g>')

    # packets: small dashes travelling along a few edges
    packets = ['<g>']
    for k, (a, b) in enumerate(edges[::9]):
        fade = min(a[2], b[2])
        if fade <= 0.1:
            continue
        x1, y1, x2, y2 = a[0], a[1], b[0], b[1]
        col = ACCENT if k % 2 == 0 else BLUE
        packets.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{col}" stroke-width="2" opacity="{0.75:.2f}" '
            f'stroke-dasharray="10 {140:.0f}" stroke-dashoffset="{-k * 37 % 140}"/>'
        )
    packets.append('</g>')

    # ---- hex + frame annotations ----------------------------------------
    hexes = ["0A 4F", "FF 21", "7C D9", "E3 05", "9B 77", "04 8C", "DE AD", "B1 06"]
    annot = ['<g font-family="%s" font-size="13">' % FONT]
    for i, hx in enumerate(hexes):
        x = 74 + (i % 4) * 92
        y = 40 + (i // 4) * 24
        annot.append(f'<text x="{x}" y="{y}" fill="{FG_DIM}" opacity="0.55">{hx}</text>')
    # right-side protocol layers
    layers = ["TLS 1.3", "QUIC", "DNSSEC", "MCP/stdio", "VLESS", "TCP"]
    for i, lay in enumerate(layers):
        y = 60 + i * 26
        op = 0.75 - i * 0.09
        annot.append(f'<text x="{W - 84}" y="{y}" text-anchor="end" fill="{ACCENT2}" opacity="{op:.2f}">{lay}</text>')
        annot.append(f'<line x1="{W - 176}" y1="{y - 4}" x2="{W - 92}" y2="{y - 4}" stroke="{GRID}" stroke-width="1"/>')
    # debugger-style coordinates bottom-left
    annot.append(
        f'<text x="74" y="{H - 28}" fill="{FG_DIM}" opacity="0.6" font-size="13">'
        f'break&#8202;point&#8202;::&#8202;0x00007FF6&#8202;A1D4&#8202;10E8 &#8594; jacek4yang</text>'
    )
    annot.append('</g>')

    # corner brackets (terminal frame)
    m, L = 28, 34
    frame = f'''<g stroke="{FG_DIM}" stroke-width="2" opacity="0.7" fill="none">
  <path d="M {m} {m + L} V {m} H {m + L}"/>
  <path d="M {W - m - L} {m} H {W - m} V {m + L}"/>
  <path d="M {W - m} {H - m - L} V {H - m} H {W - m - L}"/>
  <path d="M {m + L} {H - m} H {m} V {H - m - L}"/>
</g>'''

    # ---- wordmark --------------------------------------------------------
    word = f'''<g>
  <text x="{W / 2}" y="292" text-anchor="middle" font-family="{FONT}"
        font-size="104" font-weight="700" letter-spacing="14" fill="{FG}">JACEK YANG</text>
  <text x="{W / 2}" y="352" text-anchor="middle" font-family="{FONT}"
        font-size="22" font-weight="500" letter-spacing="10.5" fill="{ACCENT}">SYSTEMS / NETWORK / SECURITY / AI</text>
  <text x="{W / 2}" y="402" text-anchor="middle" font-family="{FONT}"
        font-size="17" letter-spacing="1.2" fill="{FG_DIM}">Building fast systems and tools close to the metal.</text>
</g>'''
    # accent rule with terminal cursor
    word += f'''<g>
  <line x1="{W / 2 - 210}" y1="322" x2="{W / 2 - 30}" y2="322" stroke="{ACCENT}" stroke-width="1.5" opacity="0.65"/>
  <line x1="{W / 2 + 30}" y1="322" x2="{W / 2 + 210}" y2="322" stroke="{ACCENT}" stroke-width="1.5" opacity="0.65"/>
  <rect x="{W / 2 - 6}" y="316" width="12" height="12" fill="{BLUE}" opacity="0.9"/>
</g>'''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Jacek Yang — Systems / Network / Security / AI">
  <defs>
    {grid_pattern("hg")}
    <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{SURFACE}"/>
      <stop offset="1" stop-color="{BG}"/>
    </linearGradient>
  </defs>
  {''.join(top)}
  {''.join(net)}
  {''.join(dots)}
  {''.join(packets)}
  {''.join(annot)}
  {frame}
  {word}
</svg>'''
    return svg


# --------------------------------------------------------------- monogram ---
def build_mono() -> str:
    """32px-class inline glyph: angle-bracket J with terminal cursor dot."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 28 28" role="img" aria-label="j4y">
  <rect width="28" height="28" rx="6" fill="{BG}"/>
  <path d="M 7 8 L 12.5 14 L 7 20" fill="none" stroke="{ACCENT}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 17.5 8 V 17 Q 17.5 20 14.5 20 H 13" fill="none" stroke="{FG}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="20" y="17" width="3.4" height="3.4" fill="{BLUE}"/>
</svg>'''


# ----------------------------------------------------------------- avatar ---
def build_avatar() -> str:
    """512 master. Circular JY mark that reads as <J + cursor> and a routed node."""
    S = 512
    c = S / 2
    # routing arc: packet enters top-right, bends through the J bowl, exits left
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}" role="img" aria-label="jacek4yang avatar">
  <defs>
    <radialGradient id="abg" cx="34%" cy="28%" r="90%">
      <stop offset="0%" stop-color="{mix(SURFACE, '#101828', 0.9)}"/>
      <stop offset="100%" stop-color="{BG}"/>
    </radialGradient>
    {grid_pattern("ag", 32, GRID, 0.35)}
    <clipPath id="around"><circle cx="{c}" cy="{c}" r="{c}"/></clipPath>
  </defs>
  <g clip-path="url(#around)">
    <rect width="{S}" height="{S}" fill="url(#abg)"/>
    <rect width="{S}" height="{S}" fill="url(#ag)"/>
    <!-- faint orbit ring (network node motif) -->
    <circle cx="{c}" cy="{c}" r="196" fill="none" stroke="{GRID}" stroke-width="2"/>
    <circle cx="{c + 196}" cy="{c}" r="5" fill="{ACCENT2}" opacity="0.9"/>
    <!-- geometry: angle bracket + J -->
    <g fill="none" stroke-linecap="round" stroke-linejoin="round">
      <path d="M 150 168 L 252 256 L 150 344" stroke="{ACCENT}" stroke-width="34"/>
      <path d="M 330 152 V 316 Q 330 366 276 366 H 246" stroke="{FG}" stroke-width="34"/>
    </g>
    <!-- terminal cursor block, bottom right -->
    <rect x="344" y="336" width="44" height="44" rx="4" fill="{BLUE}"/>
  </g>
  <circle cx="{c}" cy="{c}" r="{c - 4}" fill="none" stroke="{GRID}" stroke-width="3" opacity="0.9"/>
</svg>'''


def build_favicon() -> str:
    """32px-class mark distilled from the avatar."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="7" fill="{BG}"/>
  <path d="M 8 9 L 14.5 16 L 8 23" fill="none" stroke="{ACCENT}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 20.5 9 V 19.5 Q 20.5 23 17 23 H 15.5" fill="none" stroke="{FG}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="23" y="19.5" width="3.5" height="3.5" fill="{BLUE}"/>
</svg>'''


# --------------------------------------------------------------- og image ---
def build_og() -> str:
    """1200x630 social card, same system as the hero."""
    W, H = 1200, 630
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="jacek4yang — systems developer">
  <defs>{grid_pattern("og", 32, GRID, 0.4)}</defs>
  <rect width="{W}" height="{H}" fill="{SURFACE}"/>
  <rect width="{W}" height="{H}" fill="url(#og)"/>
  <rect width="{W}" height="{H}" fill="{BG}" opacity="0.35"/>
  <g fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M 110 210 L 190 315 L 110 420" stroke="{ACCENT}" stroke-width="26"/>
    <path d="M 250 190 V 385 Q 250 428 202 428 H 178" stroke="{FG}" stroke-width="26"/>
  </g>
  <rect x="262" y="398" width="34" height="34" rx="3" fill="{BLUE}"/>
  <text x="360" y="300" font-family="{FONT}" font-size="72" font-weight="700" letter-spacing="6" fill="{FG}">JACEK YANG</text>
  <text x="362" y="352" font-family="{FONT}" font-size="24" letter-spacing="7" fill="{ACCENT}">SYSTEMS / NETWORK / SECURITY / AI</text>
  <text x="362" y="400" font-family="{FONT}" font-size="19" fill="{FG_DIM}">github.com/jacek4yang</text>
  <g stroke="{GRID}" stroke-width="1">
    <line x1="360" y1="430" x2="1090" y2="430"/>
  </g>
  <text x="360" y="470" font-family="{FONT}" font-size="16" fill="{FG_DIM}" opacity="0.8">rust-reality &#183; egressdns &#183; reverse-mcp &#183; fastcrypto-rs &#183; cline-proxy &#183; rnc</text>
  <g stroke="{FG_DIM}" stroke-width="2" opacity="0.7" fill="none">
    <path d="M 40 76 V 40 H 76"/>
    <path d="M {W - 76} 40 H {W - 40} V 76"/>
    <path d="M {W - 40} {H - 76} V {H - 40} H {W - 76}"/>
    <path d="M 76 {H - 40} H 40 V {H - 76}"/>
  </g>
</svg>'''


# ------------------------------------------------------------------ main ----
def main() -> None:
    hero = write("hero.svg", build_hero())
    svg_to_png(hero, "hero.png", 1600)
    write("mono.svg", build_mono())
    avatar = write("avatar-source.svg", build_avatar())
    for size in (1024, 512, 256, 64):
        svg_to_png(avatar, f"avatar-{size}.png", size)
    fav = write("favicon.svg", build_favicon())
    svg_to_png(fav, "favicon.png", 32)
    og = write("og-image.svg", build_og())
    svg_to_png(og, "og-image.png", 1200)
    print("assets generated in", HERE)


if __name__ == "__main__":
    main()
