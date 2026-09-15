# Generate the animated profile hero SVG from real contribution data.
#
# Reads assets/profile/contributions.json (produced by fetch_contributions.py)
# and writes two variants (dark + light) plus an animation-free static
# fallback. Animation is SMIL — rendered by GitHub's image proxy, no JS.
#
# Usage: python assets/profile/generate_hero.py
import base64
import html
import json
import os
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))  # repo root

W, H = 840, 400
PAD = 26

# tokens (dark / light)
T = {
    "dark": {
        "bg": "#05070d", "panel": "#0b0f18", "grid": "#1a2230",
        "fg": "#e8edf5", "dim": "#8b95a7",
        "acc": "#5eead4", "acc2": "#7c8cf8", "blue": "#4cc2ff",
    },
    "light": {
        "bg": "#f7f9fc", "panel": "#ffffff", "grid": "#d7dde8",
        "fg": "#0d1321", "dim": "#5a6577",
        "acc": "#0f766e", "acc2": "#6366f1", "blue": "#0369a1",
    },
}
CELL = 11
GAP = 3
FONT = "ui-monospace,'Cascadia Code',Menlo,Consolas,monospace"


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def load_data() -> dict:
    with open(os.path.join(HERE, "contributions.json"), encoding="utf-8") as f:
        return json.load(f)


def heat_color(count: int, theme: dict) -> str:
    if count == 0:
        return theme["grid"]
    if count < 3:
        return theme["acc2"] if theme is T["dark"] else "#a5b4fc"
    if count < 6:
        return theme["blue"]
    return theme["acc"]


def contribution_grid(data: dict, theme: dict, x0: float, y0: float, max_weeks: int = 53,
                      cell: int = CELL, gap: int = GAP) -> list:
    """Return SVG elements for the contribution calendar.

    The calendar keeps only weeks from first activity onward (plus one lead-in
    week) and stretches cell size so the field fills its allocation — the
    account is young, so a full 53-week grid would be mostly empty padding.
    """
    days = data["days"]
    if not days:
        return []
    # pad the first week so columns start on Sunday
    first = date.fromisoformat(days[0]["date"])
    pad = (first.weekday() + 1) % 7  # Monday=0 → Sunday offset
    cells = [None] * pad + days
    weeks = [cells[i:i + 7] for i in range(0, len(cells), 7)][-max_weeks:]
    # keep only from the first non-empty week, plus one week of lead-in
    first_active_idx = next(
        (i for i, wk in enumerate(weeks) if any(d and d["count"] > 0 for d in wk)),
        0,
    )
    weeks = weeks[max(0, first_active_idx - 1):]

    out = []
    for wi, week in enumerate(weeks):
        for di, d in enumerate(week):
            if d is None:
                continue
            c = d["count"]
            x = x0 + wi * (cell + gap)
            y = y0 + di * (cell + gap)
            recent = wi >= len(weeks) - 6
            out.append(
                f'<rect x="{x:.0f}" y="{y}" width="{cell}" height="{cell}" rx="2.5" '
                f'fill="{heat_color(c, theme)}">'
                + (
                    f'<animate attributeName="opacity" values="1;0.55;1" dur="3.2s" '
                    f'begin="{(wi * 7 + di) % 9 * 0.35:.2f}s" repeatCount="indefinite"/>'
                    if recent and c > 0 and theme is T["dark"] and animated_ok
                    else ""
                )
                + "</rect>"
            )
    return out


def sparkline(data: dict, theme: dict, x0: float, y0: float, w: float, h: float) -> str:
    """Weekly contribution totals as a polyline with a moving signal dot."""
    days = data["days"]
    if not days:
        return ""
    weeks = {}
    for d in days:
        dt = date.fromisoformat(d["date"])
        wk = dt - timedelta(days=(dt.weekday() + 1) % 7)
        weeks[wk] = weeks.get(wk, 0) + d["count"]
    vals = [weeks[k] for k in sorted(weeks)][-52:]
    maxv = max(vals) or 1
    step = w / max(len(vals) - 1, 1)
    pts = " ".join(f"{x0 + i * step:.1f},{y0 + h - (v / maxv) * h:.1f}" for i, v in enumerate(vals))
    area = (
        f"M {x0:.1f},{y0 + h} "
        + " ".join(f"L {x0 + i * step:.1f},{y0 + h - (v / maxv) * h:.1f}" for i, v in enumerate(vals))
        + f" L {x0 + (len(vals) - 1) * step:.1f},{y0 + h} Z"
    )
    last_x = x0 + (len(vals) - 1) * step
    last_y = y0 + h - (vals[-1] / maxv) * h
    return (
        f'<path d="{area}" fill="{theme["acc"]}" opacity="0.07"/>'
        f'<polyline points="{pts}" fill="none" stroke="{theme["acc"]}" '
        f'stroke-width="1.4" opacity="0.75"/>'
        f'<circle cx="{last_x:.1f}" cy="{last_y:.1f}" r="3" fill="{theme["blue"]}">'
        f'<animate attributeName="r" values="3;4.6;3" dur="2s" repeatCount="indefinite"/>'
        f'</circle>'
    )


def build(data: dict, mode: str, animated: bool) -> str:
    global animated_ok
    animated_ok = animated
    t = T[mode]
    total = data["total"]
    streak = data["best_streak"]
    active = data["active_days"]
    prs = data["prs"]
    reviews = data["reviews"]

    # calendar is the hero element: fills the width under the sparkline.
    # We don't know the kept-week count until we slice, so compute it here too.
    days_ = data["days"]
    first_dt = date.fromisoformat(days_[0]["date"])
    pad_ = (first_dt.weekday() + 1) % 7
    cells_ = [None] * pad_ + days_
    weeks_ = [cells_[i:i + 7] for i in range(0, len(cells_), 7)][-53:]
    fai = next((i for i, wk in enumerate(weeks_) if any(d and d["count"] > 0 for d in wk)), 0)
    n_weeks = len(weeks_) - max(0, fai - 1)
    # stretch cells so n_weeks columns fill ~740px; vertical layout must keep
    # the calendar clear of the stats row (divider y=342, numbers baseline 366):
    # y0=194, 7*17+6*3 = 137 -> calendar ends at 331
    cal_cell = min(17, max(CELL, (740 - (n_weeks - 1) * GAP) // n_weeks))
    cal_w = n_weeks * (cal_cell + GAP)
    # center the calendar horizontally when the account is too young to fill
    cal_x = max(PAD + 8, (W - cal_w) // 2)
    cal_y = 194
    grid = contribution_grid(data, t, cal_x, cal_y, cell=cal_cell)
    cal_center_x = cal_x + cal_w / 2

    if not animated:
        import re
        grid = [re.sub(r"<animate.*?</animate>", "", g, flags=re.S) for g in grid]

    x0, y0, w, h = PAD + 8, 92, 500, 84
    spark = sparkline(data, t, x0, y0, w, h)
    if not animated:
        import re
        spark = re.sub(r"<animate.*?</animate>", "", spark, flags=re.S)

    blink = (
        '<animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/>'
        if animated else ""
    )
    # typing-style caret immediately after the name (name ends ~x=215)
    caret_x = 232

    stats = [
        (f"{total}", "contributions / 1y"),
        (f"{streak}", "best streak (days)"),
        (f"{active}", "active days"),
        (f"{prs + reviews}", "PRs + reviews"),
    ]
    stat_els = []
    sx = PAD + 12
    for i, (num, label) in enumerate(stats):
        x = sx + i * 186
        stat_els.append(
            f'<text x="{x}" y="366" font-family="{FONT}" font-size="21" font-weight="700" '
            f'fill="{t["fg"]}">{esc(num)}</text>'
            f'<text x="{x}" y="384" font-family="{FONT}" font-size="10.5" '
            f'fill="{t["dim"]}">{esc(label)}</text>'
        )
    # divider between calendar and stats
    if animated:
        stat_els.append(
            f'<rect x="{PAD + 12}" y="342" width="720" height="1" fill="{t["grid"]}"/>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Jacek Yang — systems developer. {total} contributions in the last year, best streak {streak} days.">
  <defs>
    <clipPath id="round"><rect width="{W}" height="{H}" rx="14"/></clipPath>
    <pattern id="bg-grid-{mode}" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M 28 0 L 0 0 0 28" fill="none" stroke="{t["grid"]}" stroke-width="1" opacity="0.45"/>
    </pattern>
    <linearGradient id="sheen-{mode}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t["acc"]}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{t["acc"]}" stop-opacity="0.9"/>
      <stop offset="1" stop-color="{t["acc"]}" stop-opacity="0"/>
      {"<animate attributeName='x1' values='-1;1' dur='4.5s' repeatCount='indefinite'/>" if animated else ""}
      {"<animate attributeName='x2' values='0;2' dur='4.5s' repeatCount='indefinite'/>" if animated else ""}
    </linearGradient>
  </defs>
  <g clip-path="url(#round)">
    <rect width="{W}" height="{H}" fill="{t["bg"]}"/>
    <rect width="{W}" height="{H}" fill="url(#bg-grid-{mode})"/>
    <rect width="{W}" height="{H}" fill="{t["panel"]}" opacity="0.35"/>

    <!-- left rail: scanline sweep -->
    <rect x="0" y="0" width="3" height="{H}" fill="url(#sheen-{mode})" opacity="0.55"/>

    <!-- header -->
    <text x="{PAD}" y="52" font-family="{FONT}" font-size="27" font-weight="700" letter-spacing="2.5" fill="{t["fg"]}">JACEK YANG</text>
    <text x="{caret_x}" y="52" font-family="{FONT}" font-size="24" fill="{t["blue"]}">&#9608;{blink and blink or ""}</text>
    <text x="{PAD}" y="72" font-family="{FONT}" font-size="12.5" letter-spacing="4.5" fill="{t["acc"]}">SYSTEMS / NETWORK / SECURITY / AI</text>

    <!-- 1y activity sparkline -->
    <text x="{x0}" y="86" font-family="{FONT}" font-size="10" letter-spacing="2" fill="{t["dim"]}">COMMIT ACTIVITY — 52W</text>
    {spark}

    <!-- contribution calendar -->
    <text x="{cal_center_x:.0f}" y="194" text-anchor="middle" font-family="{FONT}" font-size="10" letter-spacing="2" fill="{t["dim"]}">CONTRIBUTION FIELD — 12M</text>
    {''.join(grid)}

    <!-- stats row -->
    {''.join(stat_els)}

    <!-- corner brackets -->
    <g stroke="{t["dim"]}" stroke-width="1.5" opacity="0.6" fill="none">
      <path d="M 12 26 V 12 H 26"/><path d="M {W - 26} 12 H {W - 12} V 26"/>
      <path d="M {W - 12} {H - 26} V {H - 12} H {W - 26}"/><path d="M 26 {H - 12} H 12 V {H - 26}"/>
    </g>
  </g>
</svg>'''
    return svg


def main() -> None:
    data = load_data()
    out_dir = os.path.join(ROOT, "assets", "profile")
    os.makedirs(out_dir, exist_ok=True)

    for mode in ("dark", "light"):
        svg = build(data, mode, animated=True)
        with open(os.path.join(out_dir, f"hero-{mode}.svg"), "w", encoding="utf-8", newline="\n") as f:
            f.write(svg)
    # static fallback (no SMIL, dark) for readers/clients that rasterize oddly
    static = build(data, "dark", animated=False)
    with open(os.path.join(out_dir, "hero-static.svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(static)
    print("hero variants written to assets/profile/")


if __name__ == "__main__":
    main()
