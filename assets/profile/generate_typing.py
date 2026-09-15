# Generate a typing-style subtitle strip (like readme-typing-svg) but
# fully self-hosted: animated with SMIL inside one SVG, no external service.
#
# Cycles through discipline lines with a typewriter reveal. Each line has its
# own caret that rides the clip sweep (caret x animated in lockstep with the
# clip-rect width), so the caret is always at the typing position.
#
# Output: assets/profile/typing-{dark,light}.svg
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

LINES = [
    "building high-performance network software in Rust",
    "from-scratch VLESS + REALITY + XTLS Vision",
    "DNS resolvers that measure instead of guessing",
    "AI agents driving IDA Pro for binary analysis",
    "cryptographic primitives benchmarked on real shapes",
    "protocol gateways for coding agents",
]

W, H = 700, 44
PROMPT_W = 16            # "$ " prefix width
CHAR_W = 8.4             # monospace advance at font-size 14.5
TYPE_MS = 38             # per character
HOLD_MS = 1500
ERASE_MS = 14

T = {
    "dark": {"bg": "transparent", "fg": "#8b95a7", "acc": "#5eead4", "blue": "#4cc2ff"},
    "light": {"bg": "transparent", "fg": "#5a6577", "acc": "fill", "blue": "#0369a1"},
}
T["light"]["acc"] = "#0f766e"
FONT = "ui-monospace,'Cascadia Code',Menlo,Consolas,monospace"


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def build(mode: str) -> str:
    t = T[mode]
    begin = 0.0
    texts, clips, carets = [], [], []
    for i, line in enumerate(LINES):
        full_w = len(line) * CHAR_W + 4
        type_dur = len(line) * TYPE_MS / 1000
        hold = HOLD_MS / 1000
        erase = len(line) * ERASE_MS / 1000
        slot = type_dur + hold + erase
        d = f"{slot:.2f}s"
        b = f"{begin:.2f}s"
        kt = f"0;{type_dur / slot:.4f};{(type_dur + hold) / slot:.4f};1"

        # clip rect: 0 -> full -> full -> 0
        clips.append(
            f'<clipPath id="clip-{mode}-{i}"><rect x="0" y="0" width="0" height="{H}">'
            f'<animate attributeName="width" values="0;{full_w:.0f};{full_w:.0f};0" '
            f'keyTimes="{kt}" dur="{d}" begin="{b}" repeatCount="indefinite" calcMode="linear"/>'
            f'</rect></clipPath>'
        )
        # line text, visible only within its slot
        texts.append(
            f'<text x="0" y="29" font-family="{FONT}" font-size="14.5" fill="{t["fg"]}" opacity="0" '
            f'clip-path="url(#clip-{mode}-{i})">{esc(line)}'
            f'<animate attributeName="opacity" values="0;1;1;0;0" '
            f'keyTimes="0;0.001;{(type_dur + hold) / slot:.4f};{(type_dur + hold + 0.03) / slot:.4f};1" '
            f'dur="{d}" begin="{b}" repeatCount="indefinite"/></text>'
        )
        # caret rides the same sweep: x from 0 -> full_w -> full_w -> 0
        # caret hidden while the line is hidden (same opacity gate)
        carets.append(
            f'<g clip-path="url(#clip-{mode}-{i})" opacity="0">'
            f'<rect x="{full_w - 8:.1f}" y="16" width="8" height="17" fill="{t["blue"]}">'
            f'<animate attributeName="x" values="0;{full_w - 8:.1f};{full_w - 8:.1f};0" '
            f'keyTimes="{kt}" dur="{d}" begin="{b}" repeatCount="indefinite" calcMode="linear"/>'
            f'</rect>'
            f'<animate attributeName="opacity" values="0;1;1;0;0" '
            f'keyTimes="0;0.001;{(type_dur + hold) / slot:.4f};{(type_dur + hold + 0.03) / slot:.4f};1" '
            f'dur="{d}" begin="{b}" repeatCount="indefinite"/></g>'
        )
        begin += slot

    total = begin
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Rotating summary of current work">
  <defs>{''.join(clips)}</defs>
  <rect width="{W}" height="{H}" fill="{t["bg"]}"/>
  <text x="0" y="29" font-family="{FONT}" font-size="14.5" fill="{t["acc"]}">$</text>
  <g transform="translate({PROMPT_W},0)">
    {''.join(texts)}
    {''.join(carets)}
  </g>
</svg>'''


def main() -> None:
    out_dir = os.path.join(ROOT, "assets", "profile")
    os.makedirs(out_dir, exist_ok=True)
    for mode in ("dark", "light"):
        svg = build(mode)
        with open(os.path.join(out_dir, f"typing-{mode}.svg"), "w", encoding="utf-8", newline="\n") as f:
            f.write(svg)
    print("typing strips written")


if __name__ == "__main__":
    main()
