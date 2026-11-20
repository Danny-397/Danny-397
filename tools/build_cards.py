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
        v.append(f'<path class="d" style="--len:420;animation-delay:{.3 + k * .02:.2f}s" d="{path}" fill="none" '
                 f'stroke="#5d636b" stroke-opacity=".55" stroke-width="1.1" stroke-dasharray="420"/>')
    mean = [sum(r[i][1] for r in runs) / 30 for i in range(40)]
    mpath = "M" + " L".join(f"{xs[i]:.1f} {mean[i]:.1f}" for i in range(40))
    v.append(f'<path class="d" style="--len:420;animation-delay:1s" d="{mpath}" fill="none" stroke="{p["accent"]}" '
             f'stroke-width="2.6" stroke-linejoin="round" stroke-dasharray="420"/>')
    v.append(t(x1, 226, "mean across seeds", 12, p["accent"], MONO, anchor="end"))
    card(slug="02-rl-trader", palette=p,
         eyebrow="02 · RESEARCH PAPER · REINFORCEMENT LEARNING",
         title="RL Trader",
         desc=["Deep RL written from scratch, and a published paper on telling",
               "an agent that learned from one that got lucky."],
         stats=[("30", "seeds per experiment", 190), ("19 yrs", "of SPY, option hedging", 230),
                ("505", "tests in CI", 120)],
         visual="".join(v))


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
                 f'{t([640, 764, 814, 872][i] + [118, 44, 52, 92][i] / 2, 212, m, 11, p["accent"], MONO, anchor="middle")}</g>')
    css = """
  .d { animation: draw 1.3s cubic-bezier(.4,0,.2,1) .4s both; }
"""
    card(slug="04-alphaglyph", palette=p,
         eyebrow="04 · STATISTICAL RIGOR · QUANTITATIVE FINANCE",
         title="AlphaGlyph",
         desc=["A backtesting lab with overfitting detection built in: Deflated",
               "Sharpe, PBO and walk-forward tests on every strategy."],
         stats=[("106k", "param transformer", 190), ("512 MB", "served as ONNX", 200),
                ("374", "tests in CI", 120)],
         visual="".join(v), css=css)


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
              (7, 1): ("♚", 1), (6, 0): ("♟", 1), (6, 1): ("♟", 1), (5, 4): ("♛", 1)}
    for (r, c), (g, white) in pieces.items():
        col = "#fff7e6" if white else "#1d140e"
        stroke = 'stroke="#1d140e" stroke-width=".9" paint-order="stroke"' if white else ""
        v.append(f'<text x="{bx + c * s + s / 2}" y="{by + r * s + s * .8}" font-size="19" text-anchor="middle" '
                 f'font-family="\'Segoe UI Symbol\',\'Noto Sans Symbols 2\',\'DejaVu Sans\',serif" fill="{col}" {stroke}>{g}</text>')

    v.append(t(bx + s * 4, by + s * 8 + 26, "plays in your browser, on-device", 11.5, p["muted"], MONO, anchor="middle"))
    defs = ""
    card(slug="05-chess", palette=p,
         eyebrow="05 · PLAY IT YOURSELF · REINFORCEMENT LEARNING",
         title="AlphaZero-style Chess Engine",
         desc=["Neural network, tree search and self-play written from scratch,",
               "learning with no opening books and no human games."],
         stats=[("1,000", "self-play games", 170), ("4,672", "move logits", 170),
                ("59", "tests in CI", 120)],
         visual="".join(v), defs=defs)


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
        v.append(f'<g class="f" style="animation-delay:{d:.2f}s"><line x1="{cx + 3.5}" y1="{lo_:.1f}" x2="{cx + 3.5}" y2="{hi_:.1f}" '
                 f'stroke="{col}" stroke-width="1.2"/><rect x="{cx}" y="{min(o, c):.1f}" width="7" '
                 f'height="{max(abs(c - o), 1.2):.1f}" fill="{col}"/></g>')
        price = c
    # assistant reply card
    v.append(f'<g class="r" style="animation-delay:1.3s"><rect x="660" y="146" width="300" height="76" rx="10" fill="#16181b" stroke="#2a2e34"/>'
             f'{t(676, 170, "Ski", 12, p["accent"], MONO, 700)}'
             f'{t(706, 170, "portfolio_what_if · get_quote", 11, p["muted"], MONO)}'
             f'{t(676, 192, "Bottom line: trimming TSLA lowers your", 13, p["ink"])}'
             f'{t(676, 210, "beta. Every figure checked against the data.", 13, p["ink"])}</g>')
    card(slug="03-tradeski", palette=p,
         eyebrow="03 · REAL-TIME INFRASTRUCTURE · LLM TOOLS",
         title="Tradeski",
         desc=["A streaming market dashboard with an assistant that reasons",
               "about your actual holdings, and checks every figure it quotes."],
         stats=[("79%", "assistant eval, held-out", 220), ("0", "TA libraries used", 160),
                ("343", "tests in CI", 120)],
         visual="".join(v))


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
    v.append("</g>")
    # a hand's 21 landmarks, faint, at the stroke's origin
    v.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="#fff" fill-opacity=".9" filter="url(#glow)"/>')
    defs = ('<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3.2" result="b"/>'
            '<feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    css = f"""
  .d {{ animation: draw 1.6s cubic-bezier(.4,0,.2,1) both; }}
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
def banner(theme, tall=False):
    dark = theme == "dark"
    bg, edge = ("#0d1117", "#30363d") if dark else ("#ffffff", "#d0d7de")
    ink, muted = ("#e6edf3", "#9198a1") if dark else ("#1f2328", "#59636e")
    accent, faint = ("#7ee787", "#3d444d") if dark else ("#1a7f37", "#d8dee4")
    bw, bh = (600, 560) if tall else (1000, 300)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{bw}" height="{bh}" viewBox="0 0 {bw} {bh}" role="img" '
           f'aria-labelledby="bt"><title id="bt">Dan Lichtenberger: machine learning and security software, shipped and measured</title>',
           f"<style>{BASE_CSS}.d {{ animation: draw 2.2s cubic-bezier(.4,0,.2,1) both; }}</style>",
           f'<rect x=".5" y=".5" width="{bw - 1}" height="{bh - 1}" rx="18" fill="{bg}" stroke="{edge}"/>']
    # right-hand motif: thirty faint seed runs and the one that looks like a discovery
    rng = random.Random(42)
    x0, x1, base = 600, 904, 176
    motif_at = len(out)
    out.append(f'<line x1="{x0}" y1="{base}" x2="{x1}" y2="{base}" stroke="{muted}" stroke-dasharray="3 5" stroke-opacity=".7"/>')
    out.append(t(x1 + 10, base + 4, "baseline", 12, muted, MONO))
    for k in range(31):
        y, pts = base, []
        lucky = k == 30
        for i in range(46):
            y += rng.gauss(-2.0 if lucky else .2, 4.4 if lucky else 3.2)
            pts.append((x0 + i * (x1 - x0) / 45, y))
        path = "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts)
        if lucky:
            out.append(f'<path class="d" style="--len:520;animation-delay:.9s" d="{path}" fill="none" stroke="{accent}" '
                       f'stroke-width="2.6" stroke-linejoin="round" stroke-dasharray="520"/>')
            ex, ey = pts[-1]
            out.append(f'<circle class="f" style="animation-delay:2.9s" cx="{ex:.1f}" cy="{ey:.1f}" r="4.5" fill="{accent}"/>')
        else:
            out.append(f'<path class="d" style="--len:520;animation-delay:{.2 + k * .02:.2f}s" d="{path}" fill="none" '
                       f'stroke="{faint}" stroke-width="1.2" stroke-dasharray="520"/>')
    out.append(f'<g class="f" style="animation-delay:1.2s">{t(x0, 46, "every result tested across 30 training runs", 12, muted, MONO)}</g>')
    if tall:  # the motif goes under the text, scaled up a little
        motif = out[motif_at:]
        del out[motif_at:]
        out.append(f'<g transform="translate(32 {bh - 250}) scale(1.25) translate(-600 -30)">{"".join(motif)}</g>')
        out.append(f'<g class="r" style="animation-delay:.05s">{t(32, 58, "NEW YORK", 14, accent, MONO, 600, extra="letter-spacing=\"1.6\"")}</g>')
        out.append(f'<g class="r" style="animation-delay:.12s">{t(30, 118, "Dan Lichtenberger", 56, ink, SERIF, 600)}</g>')
        out.append(f'<g class="r" style="animation-delay:.2s">{t(32, 162, "I build machine learning and security", 22, muted)}</g>')
        out.append(f'<g class="r" style="animation-delay:.25s">{t(32, 192, "software, ship it, and measure that it works.", 22, muted)}</g>')
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
    out.append(f'<g class="r" style="animation-delay:.2s">{t(48, 160, "I build machine learning and security software,", 19, muted)}</g>')
    out.append(f'<g class="r" style="animation-delay:.25s">{t(48, 186, "ship it, and measure that it really works.", 19, muted)}</g>')
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
