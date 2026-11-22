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
                ("506", "tests in CI", 120)],
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
                ("587", "tests in CI", 120)],
         visual="".join(v), css=css)


# --------------------------------------------------------------------------- 03
def _mulberry32(seed):
    """The site's seeded generator (frontend/backtest-preview.js), bit for bit."""
    state = [seed & 0xFFFFFFFF]

    def imul(a, b):
        return (a * b) & 0xFFFFFFFF

    def r():
        state[0] = (state[0] + 0x6D2B79F5) & 0xFFFFFFFF
        s_ = state[0]
        t_ = imul(s_ ^ (s_ >> 15), 1 | s_)
        t_ = ((t_ + imul(t_ ^ (t_ >> 7), 61 | t_)) & 0xFFFFFFFF) ^ t_
        return ((t_ ^ (t_ >> 14)) & 0xFFFFFFFF) / 4294967296
    return r


def _backtest_example():
    """The example backtest AlphaGlyph plays before a first run: same seed, same series."""
    r = _mulberry32(20261637)

    def gauss():
        a = r()
        return math.sqrt(-2 * math.log(a + 1e-12)) * math.cos(2 * math.pi * r())
    n, cap = 252, 100000.0
    spy, strat = [cap], [cap]
    for i in range(1, n):
        mkt = 0.00035 + 0.0095 * gauss()
        spy.append(spy[-1] * (1 + mkt))
        strat.append(strat[-1] * (1 + 0.00025 + 0.8 * mkt + 0.0062 * gauss()))
    trades = []
    for b in range(0, n - 29, 32):
        lo = hi = b
        for k in range(b, b + 30):
            if strat[k] < strat[lo]:
                lo = k
            if strat[k] > strat[hi]:
                hi = k
        if hi > lo + 3:
            trades += [(lo, True), (hi, False)]
    peak, dd, rets = cap, 0.0, []
    for k in range(1, n):
        peak = max(peak, strat[k])
        dd = max(dd, 1 - strat[k] / peak)
        rets.append(strat[k] / strat[k - 1] - 1)
    m = sum(rets) / len(rets)
    sd = math.sqrt(sum((x - m) ** 2 for x in rets) / (len(rets) - 1))
    return spy, strat, trades, dict(ret=strat[-1] / cap - 1, sharpe=m / sd * math.sqrt(252), dd=dd)


def _path(pts):
    d = "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts)
    length = sum(math.dist(pts[k - 1], pts[k]) for k in range(1, len(pts)))
    return d, length


def alphaglyph():
    p = dict(bg="#0e1411", edge="#22302a", ink="#e6ece8", muted="#a3b0a8", accent="#30d158")
    red, yellow, grey = "#ff453a", "#ffd60a", "#6f7c75"
    spy, strat, trades, st = _backtest_example()
    n = len(strat)
    lo, hi = min(spy + strat), max(spy + strat)
    pad = (hi - lo) * .08
    lo, hi = lo - pad, hi + pad
    x0, x1, y0, y1 = 640, 964, 100, 170
    X = lambda k: x0 + k / (n - 1) * (x1 - x0)          # noqa: E731
    Y = lambda val: y0 + (1 - (val - lo) / (hi - lo)) * (y1 - y0)  # noqa: E731
    sp_d, sp_len = _path([(X(k), Y(v)) for k, v in enumerate(spy)])
    st_d, st_len = _path([(X(k), Y(v)) for k, v in enumerate(strat)])

    # One 9 s loop, as on the site: the lines draw, trade dots land as the line
    # passes, the figures settle, the verdict and its three tests tick in, hold, fade.
    period, draw_end = 9.0, .36
    v, css = [], []
    v.append(t(x0, 40, "example backtest, made-up numbers", 11, p["muted"], MONO))
    figs = [(f"+{st['ret'] * 100:.1f}%", "total return", p["accent"], x0),
            (f"{st['sharpe']:.2f}", "sharpe", p["ink"], x0 + 104),
            (f"−{st['dd'] * 100:.1f}%", "max drawdown", red, x0 + 176)]
    for val, lab, col, x in figs:
        v.append(f'<g class="ag-fig">{t(x, 72, val, 22, col, SANS, 700)}{t(x, 88, lab, 10.5, p["muted"], MONO)}</g>')
    v.append(f'<path class="ag-spy" d="{sp_d}" fill="none" stroke="{grey}" stroke-width="1.4" '
             f'stroke-linejoin="round" stroke-dasharray="{sp_len:.0f}"/>')
    v.append(f'<path class="ag-st" d="{st_d}" fill="none" stroke="{p["accent"]}" stroke-width="2.2" '
             f'stroke-linejoin="round" stroke-dasharray="{st_len:.0f}"/>')
    for n_, (k, buy) in enumerate(trades):
        at = draw_end * k / (n - 1) * 100     # the line draws at a steady pace, so this is its head
        css.append(f"@keyframes agd{n_} {{ 0%, {at:.1f}% {{ opacity: 0; }} {at + 2:.1f}%, 92% {{ opacity: 1; }} 97%, 100% {{ opacity: 0; }} }}"
                   f" .agd{n_} {{ animation: agd{n_} {period}s linear 1s infinite; }}")
        fill, stroke = (p["accent"], "none") if buy else (p["bg"], p["ink"])
        v.append(f'<circle class="agd{n_}" cx="{X(k):.1f}" cy="{Y(strat[k]):.1f}" r="3.2" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="1.3"/>')
    v.append(f'<g class="ag-v"><rect x="{x0}" y="186" width="9" height="9" rx="1.5" fill="{yellow}"/>'
             f'{t(x0 + 16, 195, "Promising, but needs more data", 13.5, yellow, SANS, 700)}</g>')
    tests = [("✓", "Monte Carlo", p["accent"], x0), ("✓", "Deflated Sharpe", p["accent"], x0 + 104),
             ("✕", "Fama-French", red, x0 + 232)]
    for n_, (mark, name, col, x) in enumerate(tests):
        v.append(f'<g class="ag-t{n_}">{t(x, 216, mark, 12, col, SANS, 700)}{t(x + 14, 216, name, 11, p["muted"], MONO)}</g>')

    def show(name, at):
        return (f"@keyframes {name} {{ 0%, {at:.0f}% {{ opacity: 0; }} {at + 3:.0f}%, 92% {{ opacity: 1; }} 97%, 100% {{ opacity: 0; }} }}"
                f" .{name} {{ animation: {name} {period}s ease-out 1s infinite; }}")
    css += [
        f"@keyframes agdraw {{ 0% {{ stroke-dashoffset: var(--l); opacity: 1; }} {draw_end * 100:.0f}% {{ stroke-dashoffset: 0; }}"
        f" 92% {{ stroke-dashoffset: 0; opacity: 1; }} 97%, 100% {{ stroke-dashoffset: 0; opacity: 0; }} }}",
        f".ag-spy {{ --l: {sp_len:.0f}; animation: agdraw {period}s linear 1s infinite; }}",
        f".ag-st {{ --l: {st_len:.0f}; animation: agdraw {period}s linear 1s infinite; }}",
        show("ag-fig", draw_end * 100 - 6), show("ag-v", 42), show("ag-t0", 47), show("ag-t1", 52), show("ag-t2", 57),
    ]
    card(slug="04-alphaglyph", palette=p,
         eyebrow="04 · STATISTICAL RIGOR · QUANTITATIVE FINANCE",
         title="AlphaGlyph",
         desc=["A backtesting lab with overfitting detection built in: Deflated",
               "Sharpe, PBO and walk-forward tests on every strategy."],
         stats=[("106k", "param transformer", 190), ("512 MB", "served as ONNX", 200),
                ("337", "tests in CI", 120)],
         visual="".join(v), css="\n  ".join([""] + css) + "\n")


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
    # 6k1/5ppp/q7/8/8/4Q3/PP6/1K6 w: the black king is shut in behind its own
    # pawns and its queen on a6 cannot reach the back rank, so Qe3-e8 is mate.
    # python-chess confirms Qe8# is the only mate in one here.
    pieces = {(0, 6): ("♚", 0), (1, 5): ("♟", 0), (1, 6): ("♟", 0), (1, 7): ("♟", 0), (2, 0): ("♛", 0),
              (7, 1): ("♚", 1), (6, 0): ("♟", 1), (6, 1): ("♟", 1)}
    # the move, highlighted the way the live site does, then the mated king
    for (r, c) in ((5, 4), (0, 4)):
        v.append(f'<rect class="hl" x="{bx + c * s}" y="{by + r * s}" width="{s}" height="{s}" fill="#e2b33c"/>')
    v.append(f'<rect class="mate" x="{bx + 6 * s}" y="{by}" width="{s}" height="{s}" fill="#d9472b"/>')
    for (r, c), (g, white) in pieces.items():
        col = "#fff7e6" if white else "#1d140e"
        stroke = 'stroke="#1d140e" stroke-width=".9" paint-order="stroke"' if white else ""
        v.append(f'<text x="{bx + c * s + s / 2}" y="{by + r * s + s * .8}" font-size="19" text-anchor="middle" '
                 f'font-family="\'Segoe UI Symbol\',\'Noto Sans Symbols 2\',\'DejaVu Sans\',serif" fill="{col}" {stroke}>{g}</text>')

    v.append(f'<g class="q"><text x="{bx + 4 * s + s / 2}" y="{by + 5 * s + s * .8}" font-size="19" text-anchor="middle" '
             f'font-family="\'Segoe UI Symbol\',\'Noto Sans Symbols 2\',\'DejaVu Sans\',serif" fill="#fff7e6" '
             f'stroke="#1d140e" stroke-width=".9" paint-order="stroke">♛</text></g>')
    v.append(t(bx + s * 4, by + s * 8 + 26, "plays in your browser, on-device", 11.5, p["muted"], MONO, anchor="middle"))
    v.append(f'<g class="san">{t(bx + s * 8 + 14, by + 16, "Qe8#", 15, p["ink"], SANS, 700)}'
             f'{t(bx + s * 8 + 14, by + 32, "back-rank", 10.5, p["muted"], MONO)}'
             f'{t(bx + s * 8 + 14, by + 45, "mate", 10.5, p["muted"], MONO)}</g>')
    defs = ""
    css = f"""
  @keyframes qmove {{ 0%, 24% {{ transform: translate(0, 0); }} 40%, 82% {{ transform: translate(0, {-5 * s}px); }}
                      94%, 100% {{ transform: translate(0, 0); }} }}
  .q {{ animation: qmove 6s cubic-bezier(.5,0,.3,1) 1s infinite; }}
  @keyframes hl {{ 0%, 20% {{ opacity: 0; }} 30%, 85% {{ opacity: .55; }} 95%, 100% {{ opacity: 0; }} }}
  .hl {{ animation: hl 6s ease-in-out 1s infinite; opacity: 0; }}
  @keyframes mate {{ 0%, 42% {{ opacity: 0; }} 48%, 82% {{ opacity: .7; }} 92%, 100% {{ opacity: 0; }} }}
  .mate {{ animation: mate 6s ease-in-out 1s infinite; opacity: 0; }}
  .san {{ animation: mate 6s ease-in-out 1s infinite; }}
"""
    card(slug="05-chess", palette=p,
         eyebrow="05 · PLAY IT YOURSELF · REINFORCEMENT LEARNING",
         title="AlphaZero-style Chess Engine",
         desc=["Neural network, tree search and self-play written from scratch,",
               "learning with no opening books and no human games."],
         stats=[("1,000", "self-play games", 170), ("4,672", "move logits", 170),
                ("62", "tests in CI", 120)],
         visual="".join(v), defs=defs, css=css)


# --------------------------------------------------------------------------- 05
def tradeski():
    p = dict(bg="#0a0b0d", edge="#22252a", ink="#eef1f5", muted="#9aa3af", accent="#5b9bff")
    amber = "#f5a524"
    v = []
    # a price series with the dashboard's own indicators, all computed here the
    # way Tradeski computes them (no TA library): SMA 20, SMA 50, Bollinger 20/2
    rng = random.Random(7)
    px, price = [], 100.0
    for _ in range(130):
        price *= 1 + rng.gauss(.0012, .013)
        px.append(price)

    def sma(k, w):
        return sum(px[k - w + 1:k + 1]) / w

    def sd(k, w):
        m = sma(k, w)
        return math.sqrt(sum((x - m) ** 2 for x in px[k - w + 1:k + 1]) / w)
    ks = range(50, 130)
    s20 = [sma(k, 20) for k in ks]
    s50 = [sma(k, 50) for k in ks]
    up = [sma(k, 20) + 2 * sd(k, 20) for k in ks]
    dn = [sma(k, 20) - 2 * sd(k, 20) for k in ks]
    pr = [px[k] for k in ks]
    lo, hi = min(dn + pr + s50), max(up + pr + s50)
    x0, x1, y0, y1 = 640, 964, 54, 134
    X = lambda q: x0 + q / (len(pr) - 1) * (x1 - x0)          # noqa: E731
    Y = lambda val: y0 + (1 - (val - lo) / (hi - lo)) * (y1 - y0)  # noqa: E731
    pts = lambda arr: [(X(q), Y(val)) for q, val in enumerate(arr)]  # noqa: E731
    band = "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts(up)) + " L" + \
        " L".join(f"{a:.1f} {b:.1f}" for a, b in reversed(pts(dn))) + " Z"

    legend = [("Price", p["ink"]), ("SMA 20", p["accent"]), ("SMA 50", amber), ("Bollinger 20,2", "#6b7380")]
    x = x0
    for name, col in legend:
        v.append(f'<g class="f" style="animation-delay:.6s"><rect x="{x}" y="35" width="12" height="2.4" rx="1" fill="{col}"/>'
                 f'{t(x + 17, 40, name, 10.5, p["muted"], MONO)}</g>')
        x += 17 + len(name) * 6.6 + 14
    v.append(f'<path class="f" style="animation-delay:.7s" d="{band}" fill="#8b95a5" fill-opacity=".08" stroke="#6b7380" '
             f'stroke-opacity=".55" stroke-width=".8"/>')
    for arr, col, w, cls, dl in ((s50, amber, 1.5, "d50", .9), (s20, p["accent"], 1.5, "d20", .8), (pr, p["ink"], 1.7, "dpx", .6)):
        d, length = _path(pts(arr))
        v.append(f'<path class="tdraw" style="--len:{length:.0f};animation-delay:{dl}s" d="{d}" fill="none" stroke="{col}" '
                 f'stroke-width="{w}" stroke-linejoin="round" stroke-dasharray="{length:.0f}"/>')

    # crosshair: a guide line and a dot that rides the price line, in step
    price_pts = pts(pr)
    d_price, total = _path(price_pts)
    cum, acc = [0.0], 0.0
    for q in range(1, len(price_pts)):
        acc += math.dist(price_pts[q - 1], price_pts[q])
        cum.append(acc)
    key_t = ";".join(f"{(a - x0) / (x1 - x0):.4f}" for a, _ in price_pts)
    key_p = ";".join(f"{c / total:.4f}" for c in cum)
    v.append(f'<g opacity=".9"><line x1="{x0}" y1="{y0 - 4}" x2="{x0}" y2="{y1 + 4}" stroke="{p["muted"]}" stroke-opacity=".5" '
             f'stroke-dasharray="2 3"><animateTransform attributeName="transform" type="translate" from="0 0" to="{x1 - x0} 0" '
             f'dur="7s" begin="2.2s" repeatCount="indefinite"/></line>'
             f'<circle r="3.4" fill="{p["accent"]}" stroke="{p["bg"]}" stroke-width="1.5" cx="0" cy="0" opacity="0">'
             f'<set attributeName="opacity" to="1" begin="2.2s"/>'
             f'<animateMotion path="{d_price}" dur="7s" begin="2.2s" repeatCount="indefinite" calcMode="linear" '
             f'keyTimes="{key_t}" keyPoints="{key_p}"/></circle></g>')

    # assistant reply card
    v.append(f'<g class="r" style="animation-delay:1.3s"><rect x="660" y="146" width="300" height="76" rx="10" fill="#16181b" stroke="#2a2e34"/>'
             f'{t(676, 170, "Ski", 12, p["accent"], MONO, 700)}'
             f'{t(706, 170, "portfolio_what_if · get_quote", 11, p["muted"], MONO)}'
             f'{t(676, 192, "Bottom line: trimming TSLA lowers your", 13, p["ink"])}'
             f'{t(676, 210, "beta. Every figure checked against the data.", 13, p["ink"])}'
             f'<g clip-path="url(#reply)"><rect class="cover c1" x="672" y="179" width="284" height="18" fill="#16181b"/>'
             f'<rect class="cover c2" x="672" y="197" width="284" height="18" fill="#16181b"/></g></g>')
    css = """
  .tdraw { animation: draw 1.6s cubic-bezier(.4,0,.2,1) both; }
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
                ("336", "tests in CI", 120)],
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
    bw, bh = (600, 642) if tall else (1000, 300)
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
        out.append(f'<g transform="translate(32 288) scale(1.4) translate(-592 -34)">{"".join(motif)}</g>')
        out.append(f'<g class="r" style="animation-delay:.12s">{t(30, 88, "Dan Lichtenberger", 56, ink, SERIF, 600)}</g>')
        out.append(f'<g class="r" style="animation-delay:.2s">{t(32, 132, "I build and ship, from scratch,", 22, ink)}</g>')
        out.append(phrases(32, 168, 30))
        x = 32
        for i, (val, lab, w) in enumerate((("6 / 6", "deployed", 150), ("1,828", "tests in CI", 175),
                                            ("2", "releases with DOIs", 230))):
            out.append(f'<g class="r" style="animation-delay:{.4 + i * .08:.2f}s">{t(x, 224, val, 30, ink, SANS, 700)}'
                       f'{t(x, 250, lab, 15, muted, MONO)}</g>')
            x += w
        out.append("</svg>")
        (OUT / f"banner-{theme}-tall.svg").write_text("\n".join(out), encoding="utf-8")
        return
    out.append(f'<g class="r" style="animation-delay:.12s">{t(46, 96, "Dan Lichtenberger", 54, ink, SERIF, 600)}</g>')
    out.append(f'<g class="r" style="animation-delay:.2s">{t(48, 134, "I build and ship, from scratch,", 20, ink)}</g>')
    out.append(phrases(48, 168, 28))
    x = 48
    for i, (val, lab, w) in enumerate((("6 / 6", "projects deployed", 160), ("1,828", "tests in CI", 140),
                                        ("2", "releases with DOIs", 230))):
        out.append(f'<g class="r" style="animation-delay:{.4 + i * .08:.2f}s">{t(x, 218, val, 26, ink, SANS, 700)}'
                   f'{t(x, 240, lab, 12.5, muted, MONO)}</g>')
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
