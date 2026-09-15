# Generate the minimalist systems telemetry hero SVG from real contribution data.
#
# Reads assets/profile/contributions.json (produced by fetch_contributions.py)
# and outputs dark, light, and static variants.
#
# Usage: python assets/profile/generate_hero.py
import html
import json
import os
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA_PATH = os.path.join(HERE, "contributions.json")

W, H = 840, 264
FONT = "ui-monospace, 'Cascadia Code', 'Fira Code', Menlo, Consolas, monospace"

THEMES = {
    "dark": {
        "bg": "#090d16",
        "surface": "#0f1626",
        "panel": "#0c1220",
        "border": "#1e293b",
        "border_subtle": "#162032",
        "fg": "#f8fafc",
        "dim": "#8b95a7",
        "muted": "#475569",
        "acc": "#10b981",       # emerald
        "acc_glow": "#10b98144",
        "blue": "#38bdf8",      # cyan/sky
        "violet": "#818cf8",
        "grid_empty": "#141c2c",
        "grid_l1": "#1e3a5f",
        "grid_l2": "#0284c7",
        "grid_l3": "#0ea5e9",
        "grid_l4": "#10b981",
        "term_bg": "#060911",
    },
    "light": {
        "bg": "#ffffff",
        "surface": "#f8fafc",
        "panel": "#f1f5f9",
        "border": "#e2e8f0",
        "border_subtle": "#edf2f7",
        "fg": "#0f172a",
        "dim": "#64748b",
        "muted": "#94a3b8",
        "acc": "#059669",       # deep emerald
        "acc_glow": "#05966933",
        "blue": "#0284c7",      # deep blue
        "violet": "#6366f1",
        "grid_empty": "#e2e8f0",
        "grid_l1": "#bae6fd",
        "grid_l2": "#7dd3fc",
        "grid_l3": "#38bdf8",
        "grid_l4": "#059669",
        "term_bg": "#f8fafc",
    },
}

TERMINAL_LINES = [
    ("cargo build --release -p rust-reality", "zero-copy splice // vless+reality", "#10b981"),
    ("reverse-mcp --headless ida-9.2", "headless idalib mcp server // 17 tools", "#38bdf8"),
    ("egressdns --listen 127.0.0.1:53", "adaptive doh3/doq forwarder // dnssec", "#818cf8"),
    ("cline-proxy --listen :8080", "multi-key sse gateway for claude code", "#f59e0b"),
]

def esc(s: str) -> str:
    return html.escape(s, quote=True)

def heat_color(c: int, t: dict) -> str:
    if c == 0:
        return t["grid_empty"]
    if c < 3:
        return t["grid_l1"]
    if c < 6:
        return t["grid_l2"]
    if c < 12:
        return t["grid_l3"]
    return t["grid_l4"]

def generate_svg(data: dict, mode: str, animated: bool = True) -> str:
    t = THEMES[mode]
    total = data.get("total", 0)
    commits = data.get("commits", 0)
    streak = data.get("best_streak", 0)
    active = data.get("active_days", 0)
    prs = data.get("prs", 0)
    reviews = data.get("reviews", 0)
    max_day = data.get("max_day", 0)

    # 1. Process contribution days into last 14 weeks
    days = data.get("days", [])
    if days:
        first_dt = date.fromisoformat(days[0]["date"])
        pad = (first_dt.weekday() + 1) % 7
        cells = [None] * pad + days
        weeks = [cells[i:i+7] for i in range(0, len(cells), 7)][-14:]
    else:
        weeks = []

    # Build Grid SVG elements
    grid_els = []
    gx0, gy0 = 526, 68
    cell_s, gap = 12, 4
    for wi, wk in enumerate(weeks):
        for di, d in enumerate(wk):
            if d is None:
                continue
            x = gx0 + wi * (cell_s + gap)
            y = gy0 + di * (cell_s + gap)
            c = d["count"]
            fill = heat_color(c, t)
            # Pulse latest active days slightly
            is_recent = (wi >= len(weeks) - 2) and (c > 0)
            anim = ""
            if animated and is_recent and mode == "dark":
                delay = f"{(wi * 7 + di) % 5 * 0.4:.1f}s"
                anim = f'<animate attributeName="opacity" values="1;0.6;1" dur="2.8s" begin="{delay}" repeatCount="indefinite"/>'
            grid_els.append(
                f'<rect x="{x}" y="{y}" width="{cell_s}" height="{cell_s}" rx="2.5" fill="{fill}">{anim}</rect>'
            )

    # 2. Build Single-Clock Synchronized Terminal Lines
    # Total period = 16s, 4 lines -> 4s per line
    total_t = 16.0
    slot_t = total_t / len(TERMINAL_LINES)
    term_els = []
    term_clips = []
    full_w = 410

    for idx, (cmd, desc, color) in enumerate(TERMINAL_LINES):
        t_start = idx * slot_t
        t_type_end = t_start + 1.2
        t_hold_end = t_start + 3.4
        t_end = (idx + 1) * slot_t

        clip_id = f"term-clip-{mode}-{idx}"

        if idx == 0:
            kt_w = f"0;{1.2 / total_t:.4f};{3.4 / total_t:.4f};{4.0 / total_t:.4f};0.9999;1"
            val_w = f"0;{full_w};{full_w};0;0;0"
            kt_op = f"0;{3.4 / total_t:.4f};{3.9 / total_t:.4f};{4.0 / total_t:.4f};0.9999;1"
            val_op = "1;1;0;0;0;0"
        else:
            k_before = f"{(t_start - 0.001) / total_t:.4f}"
            k_start = f"{t_start / total_t:.4f}"
            k_typed = f"{t_type_end / total_t:.4f}"
            k_hold = f"{t_hold_end / total_t:.4f}"
            k_fade = f"{(t_end - 0.1) / total_t:.4f}"
            k_end = f"{t_end / total_t:.4f}"

            kt_w = f"0;{k_before};{k_start};{k_typed};{k_hold};{k_end};1"
            val_w = f"0;0;0;{full_w};{full_w};0;0"
            kt_op = f"0;{k_before};{k_start};{k_hold};{k_fade};{k_end};1"
            val_op = "0;0;1;1;0;0;0"

        init_w = full_w if idx == 0 else 0
        init_op = 1 if idx == 0 else 0

        if animated:
            term_clips.append(
                f'<clipPath id="{clip_id}">'
                f'<rect x="52" y="110" width="{init_w}" height="54">'
                f'<animate attributeName="width" values="{val_w}" keyTimes="{kt_w}" dur="{total_t}s" repeatCount="indefinite"/>'
                f'</rect></clipPath>'
            )
            opacity_anim = (
                f'<animate attributeName="opacity" values="{val_op}" keyTimes="{kt_op}" dur="{total_t}s" repeatCount="indefinite"/>'
            )
        else:
            term_clips.append(f'<clipPath id="{clip_id}"><rect x="52" y="110" width="{init_w}" height="54"/></clipPath>')
            opacity_anim = '<set attributeName="opacity" to="1"/>' if idx == 0 else '<set attributeName="opacity" to="0"/>'

        term_els.append(
            f'<g clip-path="url(#{clip_id})" opacity="{init_op}">'
            f'{opacity_anim}'
            f'<text x="56" y="130" font-family="{FONT}" font-size="11.5" font-weight="600" fill="{t["fg"]}">{esc(cmd)}</text>'
            f'<text x="56" y="148" font-family="{FONT}" font-size="9.5" font-weight="500" fill="{color}">&gt; {esc(desc)}</text>'
            f'</g>'
        )

    # 3. Status pulse
    pulse_dot = (
        f'<circle cx="34" cy="24" r="3.5" fill="{t["acc"]}">'
        f'<animate attributeName="opacity" values="1;0.35;1" dur="2.4s" repeatCount="indefinite"/>'
        f'</circle>'
        if animated else f'<circle cx="34" cy="24" r="3.5" fill="{t["acc"]}"/>'
    )

    # Cursor animation
    cursor_anim = (
        f'<rect x="40" y="120" width="7" height="13" fill="{t["acc"]}">'
        f'<animate attributeName="opacity" values="1;0;1" dur="0.85s" repeatCount="indefinite"/>'
        f'</rect>'
        if animated else f'<rect x="40" y="120" width="7" height="13" fill="{t["acc"]}"/>'
    )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Jacek Yang — Systems &amp; Protocols Engineer. {total} contributions in 1 year.">
  <defs>
    <clipPath id="card-clip-{mode}"><rect width="{W}" height="{H}" rx="12"/></clipPath>
    {''.join(term_clips)}
    <linearGradient id="glow-{mode}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{t["acc"]}" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="{t["acc"]}" stop-opacity="0"/>
    </linearGradient>
    <pattern id="dot-grid-{mode}" width="20" height="20" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="0.8" fill="{t["border_subtle"]}"/>
    </pattern>
  </defs>

  <g clip-path="url(#card-clip-{mode})">
    <!-- Base Background -->
    <rect width="{W}" height="{H}" fill="{t["bg"]}"/>
    <rect width="{W}" height="{H}" fill="url(#dot-grid-{mode})"/>
    <rect x="0" y="0" width="{W}" height="60" fill="url(#glow-{mode})"/>

    <!-- Subtle Outer Border -->
    <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="11.5" fill="none" stroke="{t["border"]}" stroke-width="1"/>

    <!-- Top Status Bar -->
    {pulse_dot}
    <text x="46" y="27" font-family="{FONT}" font-size="10" font-weight="700" letter-spacing="1.5" fill="{t["acc"]}">ACTIVE NODE</text>
    <text x="142" y="27" font-family="{FONT}" font-size="10" font-weight="500" letter-spacing="0.5" fill="{t["muted"]}">//</text>
    <text x="158" y="27" font-family="{FONT}" font-size="9.5" font-weight="500" letter-spacing="0.5" fill="{t["dim"]}">RUST 1.85+ · WIRE PROTOCOLS · REVERSE ENG</text>

    <!-- Top Divider -->
    <line x1="26" y1="38" x2="480" y2="38" stroke="{t["border_subtle"]}" stroke-width="1"/>

    <!-- Left Main: Identity -->
    <text x="26" y="66" font-family="{FONT}" font-size="21" font-weight="700" letter-spacing="2" fill="{t["fg"]}">JACEK YANG</text>
    <rect x="176" y="52" width="146" height="18" rx="4" fill="{t["surface"]}" stroke="{t["border_subtle"]}" stroke-width="1"/>
    <text x="184" y="65" font-family="{FONT}" font-size="9" font-weight="600" letter-spacing="1" fill="{t["blue"]}">SYSTEMS &amp; PROTOCOLS</text>

    <text x="26" y="88" font-family="{FONT}" font-size="11" font-weight="400" letter-spacing="0.2" fill="{t["dim"]}">Zero-copy proxy engines, headless IDA Pro agent servers &amp; DNS resolvers.</text>

    <!-- Left Main: Terminal Console Strip -->
    <rect x="26" y="104" width="454" height="64" rx="6" fill="{t["term_bg"]}" stroke="{t["border"]}" stroke-width="1"/>
    {cursor_anim}
    <g transform="translate(6, 0)">{''.join(term_els)}</g>

    <!-- Bottom Stats Pillar -->
    <line x1="26" y1="184" x2="480" y2="184" stroke="{t["border_subtle"]}" stroke-width="1"/>

    <g transform="translate(26, 194)">
      <!-- Metric 1 -->
      <text x="0" y="18" font-family="{FONT}" font-size="19" font-weight="700" fill="{t["fg"]}">{total:,}</text>
      <text x="0" y="32" font-family="{FONT}" font-size="9" font-weight="500" letter-spacing="0.8" fill="{t["dim"]}">CONTRIBUTIONS / 1Y</text>

      <!-- Metric 2 -->
      <text x="122" y="18" font-family="{FONT}" font-size="19" font-weight="700" fill="{t["fg"]}">{streak}d</text>
      <text x="122" y="32" font-family="{FONT}" font-size="9" font-weight="500" letter-spacing="0.8" fill="{t["dim"]}">BEST STREAK</text>

      <!-- Metric 3 -->
      <text x="226" y="18" font-family="{FONT}" font-size="19" font-weight="700" fill="{t["fg"]}">{active}d</text>
      <text x="226" y="32" font-family="{FONT}" font-size="9" font-weight="500" letter-spacing="0.8" fill="{t["dim"]}">ACTIVE DAYS</text>

      <!-- Metric 4 -->
      <text x="328" y="18" font-family="{FONT}" font-size="19" font-weight="700" fill="{t["acc"]}">{prs + reviews}</text>
      <text x="328" y="32" font-family="{FONT}" font-size="9" font-weight="500" letter-spacing="0.8" fill="{t["dim"]}">PRS + REVIEWS</text>
    </g>

    <!-- Right Panel: Telemetry Radar Box -->
    <rect x="506" y="18" width="310" height="228" rx="8" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1"/>

    <!-- Radar Header -->
    <text x="522" y="38" font-family="{FONT}" font-size="9.5" font-weight="700" letter-spacing="1.5" fill="{t["fg"]}">ACTIVITY MATRIX</text>
    <text x="798" y="38" text-anchor="end" font-family="{FONT}" font-size="8.5" font-weight="600" letter-spacing="1" fill="{t["acc"]}">14-WEEK PULSE</text>
    <line x1="518" y1="48" x2="804" y2="48" stroke="{t["border_subtle"]}" stroke-width="1"/>

    <!-- Contribution Grid -->
    <g transform="translate(-4, -6)">
      {''.join(grid_els)}
    </g>

    <!-- Day Indicators -->
    <text x="798" y="72" text-anchor="end" font-family="{FONT}" font-size="8" fill="{t["muted"]}">MON</text>
    <text x="798" y="104" text-anchor="end" font-family="{FONT}" font-size="8" fill="{t["muted"]}">WED</text>
    <text x="798" y="136" text-anchor="end" font-family="{FONT}" font-size="8" fill="{t["muted"]}">FRI</text>
    <text x="798" y="168" text-anchor="end" font-family="{FONT}" font-size="8" fill="{t["muted"]}">SUN</text>

    <!-- Radar Footer Metrics -->
    <line x1="518" y1="184" x2="804" y2="184" stroke="{t["border_subtle"]}" stroke-width="1"/>

    <g transform="translate(522, 194)">
      <text x="0" y="14" font-family="{FONT}" font-size="8.5" font-weight="500" letter-spacing="0.5" fill="{t["dim"]}">PEAK DAILY COMMITS</text>
      <text x="0" y="30" font-family="{FONT}" font-size="13" font-weight="700" fill="{t["fg"]}">{max_day} commits</text>

      <text x="276" y="14" text-anchor="end" font-family="{FONT}" font-size="8.5" font-weight="500" letter-spacing="0.5" fill="{t["dim"]}">SYSTEM VELOCITY</text>
      <text x="276" y="30" text-anchor="end" font-family="{FONT}" font-size="13" font-weight="700" fill="{t["blue"]}">{commits:,} dispatched</text>
    </g>
  </g>
</svg>'''
    return svg

def main():
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)

    out_dir = os.path.join(ROOT, "assets", "profile")
    os.makedirs(out_dir, exist_ok=True)

    for mode in ("dark", "light"):
        svg = generate_svg(data, mode, animated=True)
        out_file = os.path.join(out_dir, f"hero-{mode}.svg")
        with open(out_file, "w", encoding="utf-8", newline="\n") as f:
            f.write(svg)
        print(f"wrote {out_file}")

    static_svg = generate_svg(data, "dark", animated=False)
    with open(os.path.join(out_dir, "hero-static.svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(static_svg)
    print("wrote static")

if __name__ == "__main__":
    main()
