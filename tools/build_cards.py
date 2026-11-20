"""Build the profile README's SVG banner and project cards into assets/.

Every figure on a card is copied from the project's own docs or CI and is listed
in FIGURES below with where it comes from, so a change is one edit here and a
re-run:  python tools/build_cards.py

Constraints of an SVG shown through GitHub's image proxy: no scripts, no web
fonts, no external references. Text uses system font stacks; animation is CSS
that plays once (or very slowly), is off under prefers-reduced-motion, and
starts from the finished state's opposite only inside @keyframes, so a viewer
that ignores CSS animation still shows the complete card.
"""

from __future__ import annotations

import math
import pathlib
import random
from html import escape

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"

SERIF = "'Iowan Old Style','Palatino Linotype','Book Antiqua',Palatino,Georgia,serif"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "'Cascadia Mono','SFMono-Regular',ui-monospace,Consolas,'Liberation Mono',Menlo,monospace"

W, H = 1000, 250

def t(x, y, s, size, fill, family=SANS, weight=400, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{escape(s)}</text>')


BASE_CSS = """
  @keyframes rise { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
  @keyframes fade { from { opacity: 0; } to { opacity: 1; } }
  @keyframes draw { from { stroke-dashoffset: var(--len); } to { stroke-dashoffset: 0; } }
  .r { animation: rise .7s cubic-bezier(.2,.7,.2,1) both; }
  .f { animation: fade .6s ease-out both; }
  @media (prefers-reduced-motion: reduce) { * { animation: none !important; } }
"""


def card(*, slug, palette, eyebrow, title, desc, stats, visual, css="", defs=""):
    p = palette
    body = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" aria-labelledby="title-{slug}">',
        f'<title id="title-{slug}">{escape(title)}</title>',
        f"<style>{BASE_CSS}{css}</style>",
        f"<defs>{defs}</defs>",
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="{p["bg"]}" stroke="{p["edge"]}"/>',
        # a lit top edge, like the surfaces on the project sites
        f'<rect x="18" y=".5" width="{W - 36}" height="1" fill="{p["accent"]}" opacity=".55"/>',
        f'<g class="r" style="animation-delay:.05s">{t(36, 48, eyebrow, 12.5, p["accent"], MONO, 600, extra="letter-spacing=\"1.6\"")}</g>',
        f'<g class="r" style="animation-delay:.12s">{t(36, 92, title, 34, p["ink"], SERIF, 600)}</g>',
    ]
    for i, line in enumerate(desc):
        body.append(f'<g class="r" style="animation-delay:{.2 + i * .05:.2f}s">'
                    f'{t(36, 126 + i * 23, line, 16.5, p["muted"])}</g>')
    x = 36
    for i, (value, label, w) in enumerate(stats):
        strike = value.startswith("-x-")
        value = value.removeprefix("-x-")
        delay = .35 + i * .08
        g = [t(x, 202, value, 27, p["muted"] if strike else p["accent"], SANS, 700)]
        if strike:
            width = len(value) * 15.5
            g.append(f'<line x1="{x - 2}" y1="193" x2="{x + width}" y2="193" stroke="{p["muted"]}" stroke-width="2"/>')
        g.append(t(x, 226, label, 12.5, p["muted"], MONO))
        body.append(f'<g class="r" style="animation-delay:{delay:.2f}s">{"".join(g)}</g>')
        x += w
    body.append(f'<rect x="604" y="28" width="1" height="{H - 56}" fill="{p["edge"]}"/>')
    body.append(visual)
    body.append("</svg>")
    (OUT / f"{slug}.svg").write_text("\n".join(body), encoding="utf-8")
    tall_card(slug=slug, palette=p, eyebrow=eyebrow, title=title, desc=desc, stats=stats,
              visual=visual, css=css, defs=defs)


def wrap(words: str, limit: int) -> list[str]:
    lines, line = [], ""
    for w in words.split():
        if line and len(line) + 1 + len(w) > limit:
            lines.append(line)
            line = w
        else:
            line = f"{line} {w}".strip()
    return lines + [line]


TW = 600


def tall_card(*, slug, palette, eyebrow, title, desc, stats, visual, css, defs):
    """The same card stacked for phones: text first at a larger size, the visual below.

    The wide card is 1000 units across, so on a 390px phone its body text renders
    at about 6px. This one is 600 across with bigger type, about 11px there.
    """
    p = palette
    lines = wrap(" ".join(desc), 47)
    y_desc = 142
    y_stats = y_desc + (len(lines) - 1) * 27 + 52
    y_div = y_stats + (len(stats) - 1) * 40 + 30
    h = y_div + 240
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{TW}" height="{h}" viewBox="0 0 {TW} {h}" '
        f'role="img" aria-labelledby="title-{slug}">',
        f'<title id="title-{slug}">{escape(title)}</title>',
        f"<style>{BASE_CSS}{css}</style>",
        f"<defs>{defs}</defs>",
        f'<rect x=".5" y=".5" width="{TW - 1}" height="{h - 1}" rx="18" fill="{p["bg"]}" stroke="{p["edge"]}"/>',
        f'<rect x="18" y=".5" width="{TW - 36}" height="1" fill="{p["accent"]}" opacity=".55"/>',
        f'<g class="r" style="animation-delay:.05s">{t(32, 50, eyebrow, 13.5, p["accent"], MONO, 600, extra="letter-spacing=\"1.2\"")}</g>',
        f'<g class="r" style="animation-delay:.12s">{t(32, 100, title, 37, p["ink"], SERIF, 600)}</g>',
    ]
    for i, line in enumerate(lines):
        out.append(f'<g class="r" style="animation-delay:{.2 + i * .05:.2f}s">{t(32, y_desc + i * 27, line, 19.5, p["muted"])}</g>')
    for i, (value, label, _) in enumerate(stats):
        strike = value.startswith("-x-")
        value = value.removeprefix("-x-")
        y = y_stats + i * 40
        g = [t(32, y, value, 28, p["muted"] if strike else p["accent"], SANS, 700)]
        if strike:
            g.append(f'<line x1="30" y1="{y - 10}" x2="{32 + len(value) * 16}" y2="{y - 10}" stroke="{p["muted"]}" stroke-width="2"/>')
        g.append(t(176, y - 2, label, 16, p["muted"], MONO))
        out.append(f'<g class="r" style="animation-delay:{.35 + i * .08:.2f}s">{"".join(g)}</g>')
    out.append(f'<rect x="28" y="{y_div}" width="{TW - 56}" height="1" fill="{p["edge"]}"/>')
    out.append(f'<g transform="translate(-500 {y_div - 12})">{visual}</g>')
    out.append("</svg>")
    (OUT / f"{slug}-tall.svg").write_text("\n".join(out), encoding="utf-8")


# --------------------------------------------------------------------------- 01
def rl_trader():
    p = dict(bg="#0a0b0c", edge="#26282c", ink="#eef0f2", muted="#9ba2ab", accent="#d4ff3f")
    x0, x1 = 640, 964
    rng = random.Random(7)
    v = []
    base = 128
    v.append(t(x0, 40, "30 seeds per experiment", 12, p["muted"], MONO))
    runs = []
    for k in range(30):
        y, pts = base, []
        for i in range(40):
            y += rng.gauss(-.35, 3.0)
            pts.append((x0 + i * (x1 - x0) / 39, y))
        runs.append(pts)
    xs = [runs[0][i][0] for i in range(40)]
    lo_ = [min(r[i][1] for r in runs) for i in range(40)]
    hi_ = [max(r[i][1] for r in runs) for i in range(40)]
    band = ("M" + " L".join(f"{xs[i]:.1f} {hi_[i]:.1f}" for i in range(40)) + " L"
            + " L".join(f"{xs[i]:.1f} {lo_[i]:.1f}" for i in reversed(range(40))) + " Z")
    v.append(f'<path class="f" style="animation-delay:.3s" d="{band}" fill="{p["accent"]}" fill-opacity=".07"/>')
    for k, pts in enumerate(runs):
        path = "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts)
        v.append(f'<path class="rr" style="--len:420;animation-delay:{k * .13:.2f}s" d="{path}" fill="none" '
                 f'stroke="#5d636b" stroke-opacity=".55" stroke-width="1.1" stroke-dasharray="420"/>')
    mean = [sum(r[i][1] for r in runs) / 30 for i in range(40)]
    mpath = "M" + " L".join(f"{xs[i]:.1f} {mean[i]:.1f}" for i in range(40))
    v.append(f'<path class="d" style="--len:420;animation-delay:1s" d="{mpath}" fill="none" stroke="{p["accent"]}" '
             f'stroke-width="2.6" stroke-linejoin="round" stroke-dasharray="420"/>')
    v.append(f'<circle class="mv" r="4.5" fill="{p["accent"]}">'
             f'<animateMotion dur="7s" begin="1s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;.6;1" '
             f'calcMode="linear" path="{mpath}"/></circle>')
    v.append(t(x1, 226, "mean across seeds", 12, p["accent"], MONO, anchor="end"))
    css = """
  .d { animation: draw 1.3s cubic-bezier(.4,0,.2,1) both; }
  @keyframes rerun { 0% { stroke-dashoffset: var(--len); opacity: 1; } 45% { stroke-dashoffset: 0; opacity: 1; }
                     85% { stroke-dashoffset: 0; opacity: 1; } 100% { stroke-dashoffset: 0; opacity: 0; } }
  .rr { animation: rerun 7s cubic-bezier(.4,0,.2,1) infinite backwards; }
  @media (prefers-reduced-motion: reduce) { .mv { display: none; } }
"""
    card(slug="02-rl-trader", palette=p,
         eyebrow="02 · RESEARCH PAPER · REINFORCEMENT LEARNING",
         title="RL Trader",
         desc=["Deep RL written from scratch, and a published paper on telling",
               "an agent that learned from one that got lucky."],
         stats=[("30", "seeds per experiment", 190), ("19 yrs", "of SPY, option hedging", 230),
                ("505", "tests in CI", 120)],
         visual="".join(v), css=css)


# --------------------------------------------------------------------------- 02
def quantumsafe():
    p = dict(bg="#0d1117", edge="#232a35", ink="#e6edf3", muted="#9aa6b5", accent="#8ea0f2")
    v = []
    # scan frame corner brackets, from the logo
    for (x, y, dx, dy) in ((632, 36, 1, 1), (968, 36, -1, 1), (632, 222, 1, -1), (968, 222, -1, -1)):
        v.append(f'<path d="M{x} {y + 18 * dy} V{y} H{x + 18 * dx}" fill="none" stroke="{p["accent"]}" stroke-width="2"/>')
    # a finding
    v.append(f'<rect x="652" y="86" width="296" height="70" rx="8" fill="#161b22" stroke="#2b3442"/>')
    v.append(t(666, 112, "rsa.generate_private_key(...)", 14, p["ink"], MONO))
    v.append(f'<rect x="666" y="127" width="50" height="20" rx="4" fill="#3d1d24" stroke="#f0606f" stroke-opacity=".6"/>')
    v.append(t(691, 141, "HIGH", 11.5, "#ff8a95", MONO, 700, anchor="middle"))
    v.append(t(728, 141, "→ ML-DSA · FIPS 204", 14, p["accent"], MONO, 600))
    v.append(f'<rect class="scan" x="636" y="40" width="328" height="2" fill="{p["accent"]}" opacity=".7"/>')
    css = """
  @keyframes scan { 0% { transform: translateY(0); opacity: 0; } 8% { opacity: .7; }
                    92% { opacity: .7; } 100% { transform: translateY(178px); opacity: 0; } }
  .scan { animation: scan 3.2s ease-in-out .4s infinite; opacity: 0; }
  @media (prefers-reduced-motion: reduce) { .scan { display: none; } }
"""
    card(slug="01-quantumsafe", palette=p,
         eyebrow="01 · SHIPPED PRODUCT · POST-QUANTUM SECURITY",
         title="QuantumSafe Scan",
         desc=["Finds the cryptography quantum computers will break, in 11",
               "languages, and names the NIST replacement for every finding."],
         stats=[("95%", "precision, real code", 190), ("88%", "recall, held-out code", 200),
                ("584", "tests in CI", 120)],
         visual="".join(v), css=css)


# --------------------------------------------------------------------------- 03
def alphaglyph():
    p = dict(bg="#0b0c0c", edge="#232726", ink="#f1f3f2", muted="#9aa39f", accent="#3fb950")
    v = []
    # in-sample equity curve that looks great, then its out-of-sample continuation
    rng = random.Random(3)
    pts, y = [], 158.0
    for i in range(33):
        y -= 2.4 + rng.uniform(-2.6, 2.6)
        pts.append((640 + i * 5.6, y))
    oos, y2 = [], y
    for i in range(1, 26):
        y2 += rng.uniform(-3.4, 3.4) + .9
        oos.append((pts[-1][0] + i * 5.6, y2))
    path = "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts)
    path2 = f"M{pts[-1][0]:.1f} {pts[-1][1]:.1f} L" + " L".join(f"{a:.1f} {b:.1f}" for a, b in oos)
    v.append(f'<line x1="{pts[-1][0]:.1f}" y1="54" x2="{pts[-1][0]:.1f}" y2="166" stroke="#2f3533" stroke-dasharray="2 4"/>')
    v.append(t(pts[-1][0] - 8, 46, "in-sample", 11.5, p["muted"], MONO, anchor="end"))
    v.append(t(pts[-1][0] + 8, 46, "out-of-sample", 11.5, p["muted"], MONO))
    v.append(f'<path class="d" style="--len:260" d="{path}" fill="none" stroke="{p["accent"]}" stroke-width="2.4" '
             f'stroke-linejoin="round" stroke-dasharray="260" stroke-dashoffset="0"/>')
    v.append(f'<path class="f" style="animation-delay:1.3s" d="{path2}" fill="none" stroke="#7d8682" stroke-width="2" '
             f'stroke-dasharray="4 4" stroke-linejoin="round"/>')
    for i, m in enumerate(("Deflated Sharpe", "PBO", "CPCV", "walk-forward")):
        v.append(f'<g class="f" style="animation-delay:{1.4 + i * .1:.2f}s">'
                 f'<rect x="{[640, 764, 814, 872][i]}" y="196" width="{[118, 44, 52, 92][i]}" height="24" rx="5" '
                 f'fill="#141716" stroke="#2a302e"/>'
                 f'<rect class="chip" style="animation-delay:{2 + i * 1.5:.1f}s" x="{[640, 764, 814, 872][i]}" y="196" '
                 f'width="{[118, 44, 52, 92][i]}" height="24" rx="5" fill="{p["accent"]}" stroke="{p["accent"]}"/>'
                 f'{t([640, 764, 814, 872][i] + [118, 44, 52, 92][i] / 2, 212, m, 11, p["accent"], MONO, anchor="middle")}</g>')
    v.append(f'<g class="sweep"><line x1="640" y1="54" x2="640" y2="176" stroke="{p["accent"]}" stroke-opacity=".7"/>'
             f'<rect x="640" y="54" width="22" height="122" fill="url(#trail)"/></g>')
    defs = (f'<linearGradient id="trail" x1="1" x2="0"><stop offset="0" stop-color="{p["accent"]}" stop-opacity=".14"/>'
            f'<stop offset="1" stop-color="{p["accent"]}" stop-opacity="0"/></linearGradient>')
    css = """
  .d { animation: draw 1.3s cubic-bezier(.4,0,.2,1) .4s both; }
  @keyframes sweep { 0% { transform: translateX(0); opacity: 0; } 6% { opacity: 1; }
                     88% { opacity: 1; } 100% { transform: translateX(320px); opacity: 0; } }
  .sweep { animation: sweep 6s cubic-bezier(.45,0,.55,1) 1.6s infinite; opacity: 0; }
  .sweep rect { transform: translateX(-22px); }
  @keyframes chip { 0% { opacity: 0; } 4% { opacity: .2; } 22% { opacity: .2; } 27% { opacity: 0; } 100% { opacity: 0; } }
  .chip { animation: chip 6s ease-in-out infinite; opacity: 0; }
  @media (prefers-reduced-motion: reduce) { .sweep { display: none; } }
"""
    card(slug="04-alphaglyph", palette=p,
         eyebrow="04 · STATISTICAL RIGOR · QUANTITATIVE FINANCE",
         title="AlphaGlyph",
         desc=["A backtesting lab with overfitting detection built in: Deflated",
               "Sharpe, PBO and walk-forward tests on every strategy."],
         stats=[("106k", "param transformer", 190), ("512 MB", "served as ONNX", 200),
                ("374", "tests in CI", 120)],
         visual="".join(v), css=css, defs=defs)


# --------------------------------------------------------------------------- 04
def chess():
    p = dict(bg="#1d140e", edge="#3a2818", ink="#efe3cb", muted="#c4b08f", accent="#c9a368")
    v = []
    s, bx, by = 22, 712, 37
    v.append(f'<rect x="{bx - 6}" y="{by - 6}" width="{s * 8 + 12}" height="{s * 8 + 12}" rx="4" fill="#2b1b10"/>')
    for r in range(8):
        for c in range(8):
            fill = "#e7cd9c" if (r + c) % 2 == 0 else "#9b6842"
            v.append(f'<rect x="{bx + c * s}" y="{by + r * s}" width="{s}" height="{s}" fill="{fill}"/>')
    pieces = {(0, 6): ("♚", 0), (1, 5): ("♟", 0), (1, 6): ("♟", 0), (1, 7): ("♟", 0), (2, 3): ("♛", 0),
              (7, 1): ("♚", 1), (6, 0): ("♟", 1), (6, 1): ("♟", 1)}
    # the engine's move: the white queen e3 -> g5, highlighted the way the live site does
    for (r, c) in ((5, 4), (3, 6)):
        v.append(f'<rect class="hl" x="{bx + c * s}" y="{by + r * s}" width="{s}" height="{s}" fill="#e2b33c"/>')
    for (r, c), (g, white) in pieces.items():
        col = "#fff7e6" if white else "#1d140e"
        stroke = 'stroke="#1d140e" stroke-width=".9" paint-order="stroke"' if white else ""
        v.append(f'<text x="{bx + c * s + s / 2}" y="{by + r * s + s * .8}" font-size="19" text-anchor="middle" '
                 f'font-family="\'Segoe UI Symbol\',\'Noto Sans Symbols 2\',\'DejaVu Sans\',serif" fill="{col}" {stroke}>{g}</text>')

    v.append(f'<g class="q"><text x="{bx + 4 * s + s / 2}" y="{by + 5 * s + s * .8}" font-size="19" text-anchor="middle" '
             f'font-family="\'Segoe UI Symbol\',\'Noto Sans Symbols 2\',\'DejaVu Sans\',serif" fill="#fff7e6" '
             f'stroke="#1d140e" stroke-width=".9" paint-order="stroke">♛</text></g>')
    v.append(t(bx + s * 4, by + s * 8 + 26, "plays in your browser, on-device", 11.5, p["muted"], MONO, anchor="middle"))
    defs = ""
    css = f"""
  @keyframes qmove {{ 0%, 30% {{ transform: translate(0, 0); }} 45%, 80% {{ transform: translate({2 * s}px, {-2 * s}px); }}
                      95%, 100% {{ transform: translate(0, 0); }} }}
  .q {{ animation: qmove 5s cubic-bezier(.5,0,.3,1) 1s infinite; }}
  @keyframes hl {{ 0%, 25% {{ opacity: 0; }} 35%, 85% {{ opacity: .55; }} 95%, 100% {{ opacity: 0; }} }}
  .hl {{ animation: hl 5s ease-in-out 1s infinite; opacity: 0; }}
"""
    card(slug="05-chess", palette=p,
         eyebrow="05 · PLAY IT YOURSELF · REINFORCEMENT LEARNING",
         title="AlphaZero-style Chess Engine",
         desc=["Neural network, tree search and self-play written from scratch,",
               "learning with no opening books and no human games."],
         stats=[("1,000", "self-play games", 170), ("4,672", "move logits", 170),
                ("59", "tests in CI", 120)],
         visual="".join(v), defs=defs, css=css)


# --------------------------------------------------------------------------- 05
def tradeski():
    p = dict(bg="#0a0b0d", edge="#22252a", ink="#eef1f5", muted="#9aa3af", accent="#5b9bff")
    v = []
    rng = random.Random(11)
    price, x = 112.0, 640
    for i in range(24):
        o = price
        c = o + rng.uniform(-11, 9.5)
        hi_, lo_ = max(o, c) + rng.uniform(2, 8), min(o, c) - rng.uniform(2, 8)
        up = c < o  # svg y grows down
        col = "#16a34a" if up else "#ef4444"
        cx = x + i * 13.5
        d = .5 + i * .03
        live = ' class="live"' if i == 23 else ""
        v.append(f'<g class="f" style="animation-delay:{d:.2f}s"><g{live}><line x1="{cx + 3.5}" y1="{lo_:.1f}" x2="{cx + 3.5}" y2="{hi_:.1f}" '
                 f'stroke="{col}" stroke-width="1.2"/><rect x="{cx}" y="{min(o, c):.1f}" width="7" '
                 f'height="{max(abs(c - o), 1.2):.1f}" fill="{col}"/></g></g>')
        price = c
    # assistant reply card
    v.append(f'<g class="r" style="animation-delay:1.3s"><rect x="660" y="146" width="300" height="76" rx="10" fill="#16181b" stroke="#2a2e34"/>'
             f'{t(676, 170, "Ski", 12, p["accent"], MONO, 700)}'
             f'{t(706, 170, "portfolio_what_if · get_quote", 11, p["muted"], MONO)}'
             f'{t(676, 192, "Bottom line: trimming TSLA lowers your", 13, p["ink"])}'
             f'{t(676, 210, "beta. Every figure checked against the data.", 13, p["ink"])}'
             f'<g clip-path="url(#reply)"><rect class="cover c1" x="672" y="179" width="284" height="18" fill="#16181b"/>'
             f'<rect class="cover c2" x="672" y="197" width="284" height="18" fill="#16181b"/></g></g>')
    v.append(f'<g class="f" style="animation-delay:.8s"><circle class="blink" cx="921" cy="36" r="3.5" fill="#16a34a"/>'
             f'{t(964, 40, "LIVE", 11.5, p["muted"], MONO, 700, anchor="end")}</g>')
    css = """
  @keyframes live { 0%, 100% { transform: scaleY(1); } 30% { transform: scaleY(1.7); } 60% { transform: scaleY(.6); } }
  .live { transform-box: fill-box; transform-origin: 50% 50%; animation: live 2.4s ease-in-out infinite; }
  @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: .25; } }
  .blink { animation: blink 1.6s ease-in-out infinite; }
  @keyframes type1 { 0%, 8% { transform: translateX(0); } 38%, 100% { transform: translateX(284px); } }
  @keyframes type2 { 0%, 38% { transform: translateX(0); } 70%, 100% { transform: translateX(284px); } }
  .c1 { animation: type1 7s steps(38) 1.6s infinite; }
  .c2 { animation: type2 7s steps(44) 1.6s infinite; }
  @media (prefers-reduced-motion: reduce) { .cover { display: none; } }
"""
    card(slug="03-tradeski", palette=p,
         eyebrow="03 · REAL-TIME INFRASTRUCTURE · LLM TOOLS",
         title="Tradeski",
         desc=["A streaming market dashboard with an assistant that reasons",
               "about your actual holdings, and checks every figure it quotes."],
         stats=[("79%", "assistant eval, held-out", 220), ("0", "TA libraries used", 160),
                ("343", "tests in CI", 120)],
         visual="".join(v), css=css,
         defs='<clipPath id="reply"><rect x="661" y="147" width="298" height="74" rx="9"/></clipPath>')


# --------------------------------------------------------------------------- 06
def neural_canvas():
    p = dict(bg="#0a0810", edge="#241f33", ink="#ece8f6", muted="#a9a1c4", accent="#bab1f6")
    cx, cy = 802, 125
    rng = random.Random(5)
    pts = [(0, -10)]
    for i in range(1, 9):
        a = i * .55 + rng.uniform(-.2, .2)
        r = 14 + i * 10.5
        pts.append((r * math.cos(a) * .5, -r * math.sin(a + .9)))
    d = "M" + " ".join(f"{a:.1f} {b:.1f}" for a, b in pts[:1])
    for a, b in pts[1:]:
        d += f" T{a:.1f} {b:.1f}"
    v = [f'<g class="spin" filter="url(#glow)" transform="translate({cx} {cy})">']
    colors = ["#ff5fd2", "#8f7bff", "#4fd6ff", "#ff5fd2", "#8f7bff", "#4fd6ff"]
    for k in range(6):
        v.append(f'<path d="{d}" transform="rotate({k * 60})" fill="none" stroke="{colors[k]}" stroke-width="3" '
                 f'stroke-linecap="round" class="d" style="--len:240;animation-delay:{.4 + k * .12:.2f}s" stroke-dasharray="240"/>')
    # the fingertip, painting the first stroke (the other five are its mirror images)
    v.append(f'<circle r="5" fill="#fff" fill-opacity=".9"><animateMotion dur="7s" begin=".4s" repeatCount="indefinite" '
             f'keyPoints="0;1;1" keyTimes="0;.4;1" calcMode="linear" path="{d}"/></circle>')
    v.append("</g>")
    defs = ('<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3.2" result="b"/>'
            '<feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    css = f"""
  @keyframes paint {{ 0% {{ stroke-dashoffset: var(--len); opacity: 1; }} 40% {{ stroke-dashoffset: 0; opacity: 1; }}
                     82% {{ stroke-dashoffset: 0; opacity: 1; }} 100% {{ stroke-dashoffset: 0; opacity: 0; }} }}
  .d {{ animation: paint 7s cubic-bezier(.4,0,.2,1) infinite backwards; }}
  @keyframes spin {{ to {{ transform: translate({cx}px, {cy}px) rotate(360deg); }} }}
  .spin {{ transform: translate({cx}px, {cy}px); animation: spin 90s linear infinite; }}
"""
    card(slug="06-neural-canvas", palette=p,
         eyebrow="06 · HACK THE ARTS 2026 · INTERACTIVE ART",
         title="Neural Canvas",
         desc=["Paint glowing light in mid-air with your bare hands: a webcam,",
               "a hand-tracking network and a pinch. Nothing leaves the device."],
         stats=[("21", "landmarks per hand", 190), ("~60/s", "frames, on-device", 150),
                ("1", "HTML file, no server", 200)],
         visual="".join(v), css=css, defs=defs)


# --------------------------------------------------------------------------- banner
# (name, hook, colour on dark, colour on light), in README order
# what the rotating line under the name says, and which tiles it lights up
PHRASES = [
    ("machine learning.", (1, 4), "#d4ff3f", "#5f7a00"),
    ("post-quantum security.", (0,), "#8ea0f2", "#4f63c9"),
    ("quantitative finance.", (2, 3), "#3fb950", "#1a7f37"),
    ("interactive art.", (5,), "#bab1f6", "#6e5fd6"),
]
CYCLE = 12  # seconds for all four phrases

PROJECTS = [
    ("QuantumSafe Scan", "on PyPI · 11 languages", "#8ea0f2", "#4f63c9"),
    ("RL Trader", "paper with a DOI", "#d4ff3f", "#5f7a00"),
    ("Tradeski", "live AI assistant", "#5b9bff", "#2f6fdb"),
    ("AlphaGlyph", "overfitting detector", "#3fb950", "#1a7f37"),
    ("Chess engine", "learns by self-play", "#c9a368", "#946b2d"),
    ("Neural Canvas", "hand-tracked art", "#bab1f6", "#6e5fd6"),
]


BANNER_CSS = f"""
  @keyframes ph {{ 0% {{ opacity: 0; transform: translateY(10px); }} 4% {{ opacity: 1; transform: none; }}
                  22% {{ opacity: 1; transform: none; }} 25% {{ opacity: 0; transform: translateY(-10px); }}
                  100% {{ opacity: 0; transform: translateY(-10px); }} }}
  .ph {{ opacity: 0; animation: ph {CYCLE}s cubic-bezier(.2,.7,.2,1) infinite backwards; }}
  @keyframes lit {{ 0% {{ opacity: 0; }} 4% {{ opacity: 1; }} 22% {{ opacity: 1; }} 25% {{ opacity: 0; }} 100% {{ opacity: 0; }} }}
  .lit {{ opacity: 0; animation: lit {CYCLE}s ease-in-out infinite backwards; }}
  @media (prefers-reduced-motion: reduce) {{ .ph0 {{ opacity: 1; }} }}
"""


def banner(theme, tall=False):
    dark = theme == "dark"
    bg, edge = ("#0d1117", "#30363d") if dark else ("#ffffff", "#d0d7de")
    ink, muted = ("#e6edf3", "#9198a1") if dark else ("#1f2328", "#59636e")
    accent = "#7ee787" if dark else "#1a7f37"
    tile = "#161b22" if dark else "#f6f8fa"
    bw, bh = (600, 672) if tall else (1000, 300)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{bw}" height="{bh}" viewBox="0 0 {bw} {bh}" role="img" '
           f'aria-labelledby="bt"><title id="bt">Dan Lichtenberger: I build and ship, from scratch, machine learning, post-quantum security, quantitative finance and interactive art</title>',
           f"<style>{BASE_CSS}{BANNER_CSS}</style>",
           f'<rect x=".5" y=".5" width="{bw - 1}" height="{bh - 1}" rx="18" fill="{bg}" stroke="{edge}"/>']
    # right-hand motif: the six projects, each in its own card's colour
    tiles_at = len(out)
    gx, gy, tw, th, gap = 592, 34, 179, 70, 10
    for i, (name, hook, dark_c, light_c) in enumerate(PROJECTS):
        col, row = i % 2, i // 2
        x, y = gx + col * (tw + gap), gy + row * (th + gap)
        c = dark_c if dark else light_c
        out.append(f'<g class="r" style="animation-delay:{.3 + i * .07:.2f}s">'
                   f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="10" fill="{tile}" stroke="{edge}"/>'
                   f'<rect x="{x}" y="{y + 14}" width="3" height="{th - 28}" rx="1.5" fill="{c}"/>'
                   f'{t(x + 16, y + 22, f"{i + 1:02d}", 11, c, MONO, 700)}'
                   f'{t(x + 16, y + 43, name, 16, ink, SERIF, 600)}'
                   f'{t(x + 16, y + 60, hook, 11.5, muted, MONO)}'
                   + "".join(f'<rect class="lit" style="animation-delay:{.8 + k * CYCLE / 4:.1f}s" x="{x}" y="{y}" width="{tw}" '
                             f'height="{th}" rx="10" fill="{c}" fill-opacity=".07" stroke="{c}" stroke-width="1.5"/>'
                             for k, (_, idx, _, _) in enumerate(PHRASES) if i in idx)
                   + '</g>')

    def phrases(x, y, size):
        return "".join(f'<text class="ph{" ph0" if k == 0 else ""}" style="animation-delay:{.8 + k * CYCLE / 4:.1f}s" '
                       f'x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" font-style="italic" font-weight="600" '
                       f'fill="{dc if dark else lc}">{escape(ph)}</text>'
                       for k, (ph, _, dc, lc) in enumerate(PHRASES))
    if tall:  # the motif goes under the text, scaled up a little
        motif = out[tiles_at:]
        del out[tiles_at:]
        out.append(f'<g transform="translate(32 318) scale(1.4) translate(-592 -34)">{"".join(motif)}</g>')
        out.append(f'<g class="r" style="animation-delay:.05s">{t(32, 58, "NEW YORK", 14, accent, MONO, 600, extra="letter-spacing=\"1.6\"")}</g>')
        out.append(f'<g class="r" style="animation-delay:.12s">{t(30, 118, "Dan Lichtenberger", 56, ink, SERIF, 600)}</g>')
        out.append(f'<g class="r" style="animation-delay:.2s">{t(32, 162, "I build and ship, from scratch,", 22, ink)}</g>')
        out.append(phrases(32, 198, 30))
        x = 32
        for i, (val, lab, w) in enumerate((("6 / 6", "deployed", 150), ("1,865", "tests in CI", 175),
                                            ("2", "releases with DOIs", 230))):
            out.append(f'<g class="r" style="animation-delay:{.4 + i * .08:.2f}s">{t(x, 254, val, 30, ink, SANS, 700)}'
                       f'{t(x, 280, lab, 15, muted, MONO)}</g>')
            x += w
        out.append("</svg>")
        (OUT / f"banner-{theme}-tall.svg").write_text("\n".join(out), encoding="utf-8")
        return
    out.append(f'<g class="r" style="animation-delay:.05s">{t(48, 64, "NEW YORK", 12.5, accent, MONO, 600, extra="letter-spacing=\"1.8\"")}</g>')
    out.append(f'<g class="r" style="animation-delay:.12s">{t(46, 122, "Dan Lichtenberger", 54, ink, SERIF, 600)}</g>')
    out.append(f'<g class="r" style="animation-delay:.2s">{t(48, 160, "I build and ship, from scratch,", 20, ink)}</g>')
    out.append(phrases(48, 194, 28))
    x = 48
    for i, (val, lab, w) in enumerate((("6 / 6", "projects deployed", 160), ("1,865", "tests in CI", 140),
                                        ("2", "releases with DOIs", 230))):
        out.append(f'<g class="r" style="animation-delay:{.4 + i * .08:.2f}s">{t(x, 244, val, 26, ink, SANS, 700)}'
                   f'{t(x, 266, lab, 12.5, muted, MONO)}</g>')
        x += w
    out.append("</svg>")
    (OUT / f"banner-{theme}.svg").write_text("\n".join(out), encoding="utf-8")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for build in (quantumsafe, rl_trader, tradeski, alphaglyph, chess, neural_canvas):
        build()
    for theme in ("dark", "light"):
        banner(theme)
        banner(theme, tall=True)
    print("wrote", ", ".join(sorted(f.name for f in OUT.glob("*.svg"))))
