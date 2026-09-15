# Generate a typing-style subtitle strip (like readme-typing-svg) but
# fully self-hosted: animated with SMIL inside one SVG, no external service.
#
# Cycles through discipline lines with a typewriter reveal + blinking caret.
# Output: assets/profile/typing-{dark,light}.svg
#
# Usage: python assets/profile/generate_typing.py
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
CHAR_W = 8.4          # monospace advance at font-size 14
MAX_CHARS = max(len(s) for s in LINES)
TYPE_MS = 38          # per character
HOLD_MS = 1400
ERASE_MS = 14

T = {
    "dark": {"bg": "transparent", "fg": "#8b95a7", "acc": "#5eead4", "blue": "#4cc2ff"},
    "light": {"bg": "transparent", "fg": "#5a6577", "acc": "#0f766e", "blue": "#0369a1"},
}
FONT = "ui-monospace,'Cascadia Code',Menlo,Consolas,monospace"


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def build(mode: str) -> str:
    t = T[mode]
    total_chars = sum(len(s) for s in LINES)

    # build one <text> per line, each visible during its slot; typewriter
    # effect via a <set>/<animate> on a hidden>visible char count is not
    # possible in SMIL, so we emulate with clip-rect animation: a rect mask
    # sweeps right while typing and left while erasing.
    begin = 0
    texts = []
    masks = []
    for i, line in enumerate(LINES):
        width = len(line) * CHAR_W + 4
        type_dur = len(line) * TYPE_MS / 1000
        hold = HOLD_MS / 1000
        erase = len(line) * ERASE_MS / 1000
        slot = type_dur + hold + erase

        # clip rect grows while typing, shrinks while erasing
        key_times = f"0;{type_dur/slot:.3f};{(type_dur+hold)/slot:.3f};1"
        values = f"0;{width:.0f};{width:.0f};0"
        masks.append(
            f'<rect x="0" y="0" width="{width:.0f}" height="{H}" fill="#fff" visibility="hidden">'
            f'<animate attributeName="width" values="{values}" keyTimes="{key_times}" '
            f'dur="{slot:.2f}s" begin="{begin:.2f}s" fill="freeze" repeatCount="indefinite" calcMode="linear"/>'
            f'</rect>'
        )
        # visibility: element is shown only inside its slot via opacity animation
        fade_in = 0.001
        op_values = f"0;1;1;0;0"
        op_times = (
            f"0;{fade_in/slot:.4f};{(type_dur+hold)/slot:.4f};{(type_dur+hold+0.05)/slot:.4f};1"
        )
        texts.append(
            f'<text x="0" y="29" font-family="{FONT}" font-size="14.5" fill="{t["fg"]}" opacity="0" clip-path="url(#clip-{mode}-{i})">{esc(line)}<animate attributeName="opacity" values="{op_values}" keyTimes="{op_times}" dur="{slot:.2f}s" begin="{begin:.2f}s" repeatCount="indefinite"/></text>'
        )
        begin += slot

    total = begin
    caret_x = MAX_CHARS * CHAR_W + 16
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Rotating summary of current work">
  <defs>{''.join(f'<clipPath id="clip-{mode}-{i}"><rect x="0" y="0" width="0" height="{H}"/>' + m + '</clipPath>' for i, m in enumerate(masks))}</defs>
  <rect width="{W}" height="{H}" fill="{t["bg"]}"/>
  <text x="0" y="29" font-family="{FONT}" font-size="14.5" fill="{t["acc"]}">$</text>
  {''.join(texts)}
  <rect x="{caret_x:.0f}" y="16" width="9" height="17" fill="{t["blue"]}">
    <animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/>
  </rect>
  <!-- global loop restarts the sequence -->
  <animate attributeName="opacity" values="1;1" dur="{total:.2f}s" repeatCount="indefinite"/>
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
