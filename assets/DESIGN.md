# Visual identity — design tokens

Single source of truth for every asset in this repository and the
[jacek4yang.github.io](https://github.com/jacek4yang/jacek4yang.github.io)
portfolio. `assets/generate.py` reads nothing else; keep values in sync with
`pages-site/src/style/tokens.css`.

| token | value | used for |
| --- | --- | --- |
| `--bg` | `#05070d` | base background (near-black, slight blue) |
| `--surface` | `#0b0f18` | panels, hero backdrop |
| `--grid` | `#1a2230` | grid lines / hairlines |
| `--fg` | `#e8edf5` | primary text |
| `--fg-dim` | `#8b95a7` | secondary text |
| `--accent` | `#5eead4` | cyan — primary accent |
| `--accent-2` | `#7c8cf8` | violet — secondary accent |
| `--accent-3` | `#f0f` → `#4cc2ff` | electric blue — terminal cursor / signals |

Typography: system UI stack + `ui-monospace` for technical metadata. No
webfont dependency for the README assets; the Pages site uses the same stack.

## Regenerating

```sh
python assets/generate.py            # rebuilds hero.svg, mono.svg, avatar-*.png,
                                     # favicon.svg/png, og-image.png
```

Requires Python 3 with `cairosvg` (`pip install cairosvg`). The SVGs are the
canonical sources; PNGs are derived exports.
