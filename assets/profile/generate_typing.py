# Generate a clean, single-clock typing-style subtitle strip.
# Uses single global timeline (dur=total_dur) so lines never collide or desync.
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

W, H = 700, 36
PROMPT_W = 16            # "$ " prefix width
FONT = "ui-monospace, 'Cascadia Code', 'Fira Code', Menlo, Consolas, monospace"

T = {
    "dark": {"bg": "transparent", "fg": "#8b95a7", "acc": "#10b981", "blue": "#38bdf8"},
    "light": {"bg": "transparent", "fg": "#5a6577", "acc": "#059669", "blue": "#0284c7"},
}

def esc(s: str) -> str:
    return html.escape(s, quote=True)

def build(mode: str) -> str:
    t = T[mode]
    slot_dur = 3.5
    total_dur = len(LINES) * slot_dur
    texts, clips = [], []

    for i, line in enumerate(LINES):
        t_start = i * slot_dur
        t_type = t_start + 1.2
        t_hold = t_start + 3.1
        t_end = (i + 1) * slot_dur

        clip_id = f"clip-{mode}-{i}"
        full_w = 600

        if i == 0:
            kt_w = f"0;{1.2 / total_dur:.4f};{3.1 / total_dur:.4f};{3.5 / total_dur:.4f};0.9999;1"
            val_w = f"0;{full_w};{full_w};0;0;0"
            kt_op = f"0;{3.1 / total_dur:.4f};{3.4 / total_dur:.4f};{3.5 / total_dur:.4f};0.9999;1"
            val_op = "1;1;0;0;0;0"
        else:
            k_before = f"{(t_start - 0.001) / total_dur:.4f}"
            k_start = f"{t_start / total_dur:.4f}"
            k_typed = f"{t_type / total_dur:.4f}"
            k_hold = f"{t_hold / total_dur:.4f}"
            k_fade = f"{(t_end - 0.1) / total_dur:.4f}"
            k_end = f"{t_end / total_dur:.4f}"

            kt_w = f"0;{k_before};{k_start};{k_typed};{k_hold};{k_end};1"
            val_w = f"0;0;0;{full_w};{full_w};0;0"
            kt_op = f"0;{k_before};{k_start};{k_hold};{k_fade};{k_end};1"
            val_op = "0;0;1;1;0;0;0"

        init_w = full_w if i == 0 else 0
        init_op = 1 if i == 0 else 0

        clips.append(
            f'<clipPath id="{clip_id}">'
            f'<rect x="0" y="0" width="{init_w}" height="{H}">'
            f'<animate attributeName="width" values="{val_w}" keyTimes="{kt_w}" dur="{total_dur:.1f}s" repeatCount="indefinite"/>'
            f'</rect></clipPath>'
        )

        texts.append(
            f'<g clip-path="url(#{clip_id})" opacity="{init_op}">'
            f'<animate attributeName="opacity" values="{val_op}" keyTimes="{kt_op}" dur="{total_dur:.1f}s" repeatCount="indefinite"/>'
            f'<text x="0" y="23" font-family="{FONT}" font-size="13" font-weight="500" fill="{t["fg"]}">{esc(line)}</text>'
            f'</g>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Summary of focus areas">
  <defs>{''.join(clips)}</defs>
  <rect width="{W}" height="{H}" fill="{t["bg"]}"/>
  <text x="0" y="23" font-family="{FONT}" font-size="13" font-weight="700" fill="{t["acc"]}">$</text>
  <g transform="translate({PROMPT_W},0)">
    {''.join(texts)}
  </g>
</svg>'''

def main() -> None:
    out_dir = os.path.join(ROOT, "assets", "profile")
    os.makedirs(out_dir, exist_ok=True)
    for mode in ("dark", "light"):
        svg = build(mode)
        with open(os.path.join(out_dir, f"typing-{mode}.svg"), "w", encoding="utf-8", newline="\n") as f:
            f.write(svg)
    print("typing strips written with synchronized global timeline")

if __name__ == "__main__":
    main()
