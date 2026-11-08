# Renders the profile card shown in README.md as two SVGs, one per GitHub theme.
# Edit CODE below, then run from the repo root:
#   python3 scripts/profile_card.py
# Writes assets/profile-dark.svg and assets/profile-light.svg.
#
# GitHub shows README images through <img>, so the SVG cannot load web fonts:
# the text uses the viewer's system monospace, and widths shift slightly per OS.
import re
from pathlib import Path
from xml.sax.saxutils import escape

CODE = '''let kchojn = Engineer {
    role: "senior blockchain engineer",
    focus: "core protocol, EVM infrastructure",
    since: 2019,
    writes: ["go", "rust", "solidity", "python", "typescript"],
    works_on: [
        "distributed validators (bls threshold signing, libp2p)",
        "atomic cross-rollup transactions",
        "zk batch proving on the op stack (op-succinct/sp1)",
        "fully decoded evm state and storage data",
    ],
    upstream: ["go-ethereum", "reth", "optimism", "base", "ethereumjs"],
    links: ["x.com/kchojn", "linkedin.com/in/karol-chojnowski"],
};'''.split("\n")

# Rust, Go, Python, Ethereum: the left bar, top to bottom.
BAR = ["#DEA584", "#00ADD8", "#3776AB", "#627EEA"]

# Token colors: k keyword (Rust), t type (Ethereum), f field (Go),
# s string and n number (Python). Light values are darkened for contrast on white.
THEMES = {
    "dark": {"bg": "#0d1117", "border": "#30363d", "fg": "#c9d1d9", "punct": "#6e7681", "num": "#3a414b",
             "k": "#DEA584", "t": "#7B93F0", "f": "#00ADD8", "s": "#FFD43B", "n": "#5A9BD5"},
    "light": {"bg": "#ffffff", "border": "#d0d7de", "fg": "#24292f", "punct": "#8c959f", "num": "#afb8c1",
              "k": "#B7410E", "t": "#4C5FD5", "f": "#007D9C", "s": "#8A6100", "n": "#3776AB"},
}

W, LH, FS, PADX, PADY, GUTTER = 760, 22, 14, 72, 44, 24
H = PADY * 2 + LH * len(CODE)
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
TOK = re.compile(r'(?P<s>"[^"]*")|(?P<k>\blet\b)|(?P<t>\bEngineer\b)|(?P<n>\b\d+\b)'
                 r'|(?P<f>\b[a-z_]+(?=:))|(?P<p>[{}\[\](),;:=])|(?P<o>\s+|[^"\s{}\[\](),;:=]+)')


def render(c):
    lines = []
    for i, line in enumerate(CODE):
        y = PADY + LH * (i + 1) - 6
        spans = "".join(
            f'<tspan fill="{c["fg"] if m.lastgroup == "o" else c["punct"] if m.lastgroup == "p" else c[m.lastgroup]}">'
            f"{escape(m.group())}</tspan>"
            for m in TOK.finditer(line))
        lines.append(f'<text x="{PADX - GUTTER}" y="{y}" text-anchor="end" fill="{c["num"]}">{i + 1}</text>')
        lines.append(f'<text x="{PADX}" y="{y}" xml:space="preserve">{spans}</text>')
    seg = H / len(BAR)
    bar = "".join(f'<rect y="{i * seg:.1f}" width="4" height="{seg:.1f}" fill="{col}"/>' for i, col in enumerate(BAR))
    body = "\n".join(lines)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>text{{font-family:{FONT};font-size:{FS}px}}</style>
<clipPath id="r"><rect width="{W}" height="{H}" rx="10"/></clipPath>
<g clip-path="url(#r)"><rect width="{W}" height="{H}" fill="{c["bg"]}"/>{bar}</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="none" stroke="{c["border"]}"/>
{body}
</svg>
'''


out = Path("assets")
out.mkdir(exist_ok=True)
for name, colors in THEMES.items():
    (out / f"profile-{name}.svg").write_text(render(colors))
