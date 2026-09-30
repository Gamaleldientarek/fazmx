"""Write build/glyphdata.json, the data behind the page's glyph map, from the font itself.

Letter sets come from the font's character map. The flags init, medi and fina say
whether HarfBuzz gives a letter its own glyph in that position (tested with ZWJ
on either side), so the map only offers the forms the font really has.
"""
import json
import unicodedata as ud
from pathlib import Path

import uharfbuzz as hb
from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
TTF = HERE.parent / "fonts" / "AzmXVariable.ttf"
OUT = HERE.parent / "build" / "glyphdata.json"
ZWJ = "‍"
# The symbols tab is a chosen set, in code point order. Each one must exist in the font.
SYMBOLS = "#$%&*@£©«®°»،؛؟٪٫٬٭۔–—“”•‹›€™←→﷼"

cmap = TTFont(TTF).getBestCmap()
font = hb.Font(hb.Face(hb.Blob.from_file_path(str(TTF))))


def glyph_at(text, index):
    """Glyph id HarfBuzz uses for the character at `index` of `text`."""
    buf = hb.Buffer()
    buf.add_codepoints([ord(ch) for ch in text])
    buf.guess_segment_properties()
    buf.cluster_level = hb.BufferClusterLevel.CHARACTERS  # keep ZWJ out of the letter's cluster
    hb.shape(font, buf, {})
    return next(info.codepoint for info in buf.glyph_infos if info.cluster == index)


def entry(cp, forms=False):
    ch = chr(cp)
    e = {"c": ch, "u": f"U+{cp:04X}", "n": ud.name(ch).title()}
    if forms:
        isol, init = glyph_at(ch, 0), glyph_at(ch + ZWJ, 0)
        medi, fina = glyph_at(ZWJ + ch + ZWJ, 1), glyph_at(ZWJ + ch, 1)
        # A right-joining letter (ا د ر و …) shows its final form mid-word: that is not a medial form.
        e["f"] = {"init": init != isol, "medi": medi not in (isol, fina), "fina": fina != isol}
    return e


def letters(lo, hi):
    return [cp for cp in sorted(cmap) if lo <= cp <= hi and ud.category(chr(cp)) == "Lo"]


missing = [s for s in SYMBOLS if ord(s) not in cmap]
if missing:
    raise SystemExit(f"Symbols missing from the font: {' '.join(missing)}")

digits = [*range(0x0660, 0x066A), *range(0x06F0, 0x06FA), *range(0x30, 0x3A)]
latin = [*range(0x41, 0x5B), *range(0x61, 0x7B)]
data = {
    "arabic": [entry(cp, True) for cp in letters(0x0621, 0x064A)],
    "extended": [entry(cp, True) for cp in letters(0x0671, 0x06FF)],
    "digits": [entry(cp) for cp in digits if cp in cmap],
    "latin": [entry(cp) for cp in latin if cp in cmap],
    "symbols": [entry(ord(s)) for s in SYMBOLS],
}
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print("glyphdata:", {k: len(v) for k, v in data.items()})
