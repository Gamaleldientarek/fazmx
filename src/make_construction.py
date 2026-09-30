"""Generate the construction figure for the word «تجربة» from the real Azm X outlines.

Writes build/construction.svg. Everything is measured from the font:
letter bodies, the rhombus dots, the Bezier points of two curves, and a column of
dots that measures the alef height.
"""
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

HERE = Path(__file__).resolve().parent
TTF = HERE.parent / "fonts" / "AzmXVariable.ttf"
OUT = HERE.parent / "build" / "construction.svg"
WORD, WGHT = "تجربة", 700
ALEF = 680          # alef height in font units (same at every weight)
POLY_GLYPHS = ("uni062C", "uni0629")   # show Bezier points for ج and ة


def num(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def pt(p):
    return f"{num(p[0])} {num(p[1])}"


inst = instantiateVariableFont(TTFont(TTF), {"wght": WGHT}, inplace=False)
gs = inst.getGlyphSet()
hbfont = hb.Font(hb.Face(hb.Blob.from_file_path(str(TTF))))
hbfont.set_variations({"wght": WGHT})
buf = hb.Buffer()
buf.add_str(WORD)
buf.guess_segment_properties()
hb.shape(hbfont, buf, {})

glyphs, cursor = [], 0
for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
    name = hbfont.glyph_to_string(info.codepoint)
    ox, oy = cursor + pos.x_offset, pos.y_offset
    pen = DecomposingRecordingPen(gs)
    gs[name].draw(pen)
    contours, cur = [], None
    for op, args in pen.value:
        pts = [(ox + p[0], -(oy + p[1])) for p in args if p is not None]
        if op == "moveTo":
            cur = [("M", pts)]
        elif op == "lineTo":
            cur.append(("L", pts))
        elif op == "qCurveTo":
            cur.append(("Q", pts))
        elif op == "curveTo":
            cur.append(("C", pts))
        elif op in ("closePath", "endPath") and cur:
            contours.append(cur)
            cur = None
    glyphs.append({"name": name, "contours": contours})
    cursor += pos.x_advance
WORD_W = cursor


def bbox(c):
    ps = [p for _, pts in c for p in pts]
    xs, ys = [p[0] for p in ps], [p[1] for p in ps]
    return min(xs), min(ys), max(xs), max(ys)


def is_dot(c):
    x0, y0, x1, y1 = bbox(c)
    ops = [k for k, _ in c[1:]]
    return len(ops) == 3 and all(k == "L" for k in ops) and abs((x1 - x0) - (y1 - y0)) < 3 and (x1 - x0) < 300


def path_d(c):
    out = []
    for k, pts in c:
        if k in ("M", "L"):
            out.append(k + pt(pts[0]))
        elif k == "C":
            out.append("C" + " ".join(pt(p) for p in pts))
        else:  # TrueType quadratic spline with implied on-curve points
            offs, on = pts[:-1], pts[-1]
            if not offs:
                out.append("L" + pt(on))
                continue
            for a, b in zip(offs, offs[1:]):
                out.append(f"Q{pt(a)} {pt(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2))}")
            out.append(f"Q{pt(offs[-1])} {pt(on)}")
    return "".join(out) + "Z"


def control_points(c):
    seq = []
    for k, pts in c:
        if k in ("M", "L"):
            seq.append((pts[0], True))
        else:
            seq += [(p, False) for p in pts[:-1]] + [(pts[-1], True)]
    return seq


dots = [ctr for g in glyphs for ctr in g["contours"] if is_dot(ctr)]
DOT = bbox(dots[0])[2] - bbox(dots[0])[0]
STACK_X = WORD_W + 300

all_boxes = [bbox(c) for g in glyphs for c in g["contours"]]
top = min(min(b[1] for b in all_boxes), -ALEF) - 160
bottom = max(b[3] for b in all_boxes) + 160
left, right = -160, STACK_X + DOT / 2 + 160
parts = [
    f'<svg class="bf" viewBox="{num(left)} {num(top)} {num(right - left)} {num(bottom - top)}" '
    f'role="img" aria-label="كلمة تجربة مبنية من نقاط خط عزم إكس">',
    f'<line class="bf-base" x1="{num(left + 60)}" x2="{num(right - 60)}" y1="0" y2="0"/>',
]

n = len(glyphs)
for i, g in enumerate(glyphs):
    delay = f"{(n - 1 - i) * 0.22:.2f}s"          # reading order: rightmost glyph first
    body = [c for c in g["contours"] if not is_dot(c)]
    gdots = [c for c in g["contours"] if is_dot(c)]
    parts.append(f'<g style="--d:{delay}">')
    parts += [f'<path class="bf-body" pathLength="1" d="{path_d(c)}"/>' for c in body]
    parts += [f'<path class="bf-dot" d="{path_d(c)}"/>' for c in gdots]
    parts.append("</g>")

    con = [f'<g class="bf-con" style="--d:{delay}">']
    for c in gdots:
        x0, y0, x1, y1 = bbox(c)
        cy, cx = (y0 + y1) / 2, (x0 + x1) / 2
        con.append(f'<line class="bf-diag" x1="{num(x0)}" y1="{num(cy)}" x2="{num(x1)}" y2="{num(cy)}"/>')
        con.append(f'<line class="bf-diag" x1="{num(cx)}" y1="{num(y0)}" x2="{num(cx)}" y2="{num(y1)}"/>')
        con += [f'<circle class="bf-pt" cx="{num(x)}" cy="{num(cy)}" r="14"/>' for x in (x0, x1)]
    if g["name"].startswith(POLY_GLYPHS) and body:
        big = max(body, key=lambda c: (bbox(c)[2] - bbox(c)[0]) * (bbox(c)[3] - bbox(c)[1]))
        seq = control_points(big)
        con.append('<polygon class="bf-poly" points="' + " ".join(f"{num(p[0])},{num(p[1])}" for p, _ in seq) + '"/>')
        for p, on in seq:
            if on:
                con.append(f'<rect class="bf-on" x="{num(p[0] - 13)}" y="{num(p[1] - 13)}" width="26" height="26"/>')
            else:
                con.append(f'<circle class="bf-off" cx="{num(p[0])}" cy="{num(p[1])}" r="13"/>')
    con.append("</g>")
    parts += con

# Column of dots measuring the alef: rhombi stacked tip to tip from the baseline.
m = ['<g class="bf-con" style="--d:1.1s">']
for k in range(4):
    cy = -(DOT / 2 + k * DOT)
    h = DOT / 2
    m.append(f'<path class="bf-rh" d="M{num(STACK_X - h)} {num(cy)}L{num(STACK_X)} {num(cy - h)}L{num(STACK_X + h)} {num(cy)}L{num(STACK_X)} {num(cy + h)}Z"/>')
m.append(f'<line class="bf-diag" x1="{num(STACK_X - DOT)}" x2="{num(STACK_X + DOT)}" y1="{-ALEF}" y2="{-ALEF}"/>')
m.append("</g>")
parts += m
parts.append("</svg>")

OUT.parent.mkdir(exist_ok=True)
OUT.write_text("\n".join(parts), encoding="utf-8")
print(f"glyphs {[g['name'] for g in glyphs]}, dots {len(dots)}, dot size {DOT:.1f}, "
      f"alef = {ALEF / DOT:.2f} dots, bytes {len(''.join(parts))}")
