"""Build the Azm X font site into docs/ (served by GitHub Pages) and a one-file preview.

    python src/build.py         rebuild everything, keeping the existing docs/og.png
    python src/build.py --og    also retake docs/og.png (needs Playwright with Chromium)

Outputs:
  docs/                          the site. Commit it: GitHub Pages serves main /docs.
  build/azmx-font-preview.html   one file with the font inlined, for the claude.ai preview
  build/glyphdata.json, build/construction.svg
                                 inputs measured from the font, regenerated on every run
"""
import base64
import re
import shutil
import subprocess
import sys
import unicodedata
import zipfile
from datetime import datetime, timedelta
from html import escape
from pathlib import Path

from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SITE = ROOT / "docs"
BUILD = ROOT / "build"
ASSETS = ROOT / "assets"
DOMAIN = "fazmx.gamaleldien.com"
FONTS = ("AzmXVariable.woff2", "AzmXVariable.woff", "AzmXVariable.ttf")
AR = "٠١٢٣٤٥٦٧٨٩"
RETAKE_OG = "--og" in sys.argv[1:]

# Inputs measured from the font: the glyph map data and the construction figure.
for script in ("make_glyphdata.py", "make_construction.py"):
    subprocess.run([sys.executable, str(HERE / script)], check=True, stdout=subprocess.DEVNULL)
glyph_json = (BUILD / "glyphdata.json").read_text(encoding="utf-8")
construction = (BUILD / "construction.svg").read_text(encoding="utf-8")
src = (HERE / "index.src.html").read_text(encoding="utf-8")

# Logo: recolour to currentColor, drop the clip group and fixed size.
logo = (ASSETS / "azmx-logo-navy.svg").read_text(encoding="utf-8")
logo = re.sub(r'\s(width|height)="[^"]*"', "", logo, count=2)
logo = re.sub(r"<defs>.*?</defs>", "", logo, flags=re.S)
logo = re.sub(r'<g clip-path="[^"]*">', "", logo).replace("</g>", "")
logo = logo.replace('fill="#040038"', 'fill="currentColor"')
logo = logo.replace("<svg ", '<svg aria-hidden="true" focusable="false" ', 1)
logo = re.sub(r">\s+<", "><", logo).strip()

font = TTFont(ROOT / "fonts" / "AzmXVariable.ttf")
# Zip entries carry the font's own build date, so an unchanged font gives an unchanged zip.
FONT_DATE = (datetime(1904, 1, 1) + timedelta(seconds=font["head"].modified)).timetuple()[:6]

# The stats row states these numbers in the copy. After a font update, warn if they drifted.
stated = [int(v) for v in re.findall(r'class="n num" data-v="(\d+)"', src)]
features = {r.FeatureTag for t in ("GSUB", "GPOS") if t in font for r in font[t].table.FeatureList.FeatureRecord}
actual = [len(font.getGlyphOrder()), len(font.getBestCmap()), len(features), len(font["fvar"].instances)]
for label, s, a in zip(("glyphs", "characters", "feature tags", "named weights"), stated, actual):
    if s != a:
        print(f"WARNING: the page says {s} {label}, the font has {a}. Update #stats and any copy that repeats it.")

# The proofs under the numbers in #stats: every visible character the font maps (no marks, spaces,
# controls, presentation forms, tatweel or dotted circle), Arabic first, and the feature tags.
HIDDEN = {"Mn", "Me", "Cf", "Cc", "Co", "Zs", "Zl", "Zp"}
shown = [chr(c) for c in sorted(font.getBestCmap())
         if unicodedata.category(chr(c)) not in HIDDEN and c not in (0x0640, 0x25CC) and not 0xFB50 <= c <= 0xFEFF]
is_ar = lambda ch: 0x0600 <= ord(ch) <= 0x06FF or 0x0750 <= ord(ch) <= 0x077F
chars_ar = escape(" ".join(ch for ch in shown if is_ar(ch)))
chars_la = escape(" ".join(ch for ch in shown if not is_ar(ch)))
feature_tags = "".join(f'<li><code class="on">{t}</code></li>' if t == "swsh" else f"<li><code>{t}</code></li>"
                       for t in sorted(features))


def kb(n):
    return "".join(AR[int(c)] for c in str(round(n / 1024))) + " ك.ب"


def fill(html, fontsrc, preview, zipsize):
    html = re.sub(r"/\*@FONTSRC@\*/.*?/\*@END@\*/", lambda m: fontsrc, html, flags=re.S)
    html = re.sub(r"/\*@SIZE:([\w.]+)@\*/", lambda m: kb((ROOT / "fonts" / m[1]).stat().st_size), html)
    html = html.replace("<!--@LOGO@-->", logo)
    html = html.replace("<!--@CONSTRUCTION@-->", construction)
    html = html.replace("/*@GLYPHS@*/{}", glyph_json)
    html = html.replace("<!--@CHARS:ar@-->", chars_ar).replace("<!--@CHARS:la@-->", chars_la)
    html = html.replace("<!--@FEATURES@-->", feature_tags)
    html = html.replace("/*@PREVIEW@*/false", "true" if preview else "false")
    html = html.replace("/*@ZIPSIZE@*/", zipsize)
    return html


# 1) The site
old_og = (SITE / "og.png").read_bytes() if (SITE / "og.png").exists() else None
shutil.rmtree(SITE, ignore_errors=True)
(SITE / "fonts").mkdir(parents=True)
(SITE / "downloads").mkdir()
for f in FONTS:
    shutil.copyfile(ROOT / "fonts" / f, SITE / "fonts" / f)
zip_dl = SITE / "downloads" / "AzmX-Variable.zip"
with zipfile.ZipFile(zip_dl, "w", zipfile.ZIP_DEFLATED) as z:
    for path, name in [(ROOT / "fonts" / f, f) for f in FONTS] + [(HERE / "LICENSE.txt", "LICENSE.txt")]:
        info = zipfile.ZipInfo(f"AzmX-Variable/{name}", date_time=FONT_DATE)
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        z.writestr(info, path.read_bytes())
zipsize = kb(zip_dl.stat().st_size)

site_font = ", ".join([
    'url("fonts/AzmXVariable.woff2") format("woff2-variations")', 'url("fonts/AzmXVariable.woff2") format("woff2")',
    'url("fonts/AzmXVariable.woff") format("woff-variations")', 'url("fonts/AzmXVariable.woff") format("woff")',
    'url("fonts/AzmXVariable.ttf") format("truetype-variations")', 'url("fonts/AzmXVariable.ttf") format("truetype")'])
page = fill(src, site_font, False, zipsize)
for marker in ("<!--@META@-->\n", "<!--@END_META@-->", "/*@DL@*/", "/*@END_DL@*/"):
    page = page.replace(marker, "")
(SITE / "index.html").write_text(page, encoding="utf-8")
shutil.copyfile(HERE / "license.html", SITE / "license.html")
shutil.copyfile(ASSETS / "azmx-favicon.png", SITE / "favicon.png")
for folder in ("heritage", "gradients"):
    shutil.copytree(ASSETS / folder, SITE / folder, ignore=shutil.ignore_patterns(".*"))
(SITE / "CNAME").write_text(DOMAIN + "\n", encoding="utf-8")
(SITE / ".nojekyll").write_text("", encoding="utf-8")

# Link-preview image: the top of the page at 1200x630. Retaken only with --og (or when missing),
# because the hero is animated and every retake gives a slightly different picture.
if old_og and not RETAKE_OG:
    (SITE / "og.png").write_bytes(old_og)
else:
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            tab = browser.new_page(viewport={"width": 1200, "height": 630})
            tab.goto((SITE / "index.html").as_uri())
            tab.evaluate("document.fonts.ready")
            tab.wait_for_timeout(3200)
            tab.screenshot(path=str(SITE / "og.png"))
            browser.close()
    except Exception as exc:  # the site still works without it
        if old_og:
            (SITE / "og.png").write_bytes(old_og)
        print("og.png not retaken:", exc)

# 2) Preview: font and images inlined, no social tags, no page wrapper, no file downloads.
b64 = base64.b64encode((ROOT / "fonts" / "AzmXVariable.woff2").read_bytes()).decode()
prev = fill(src, f'url("data:font/woff2;base64,{b64}") format("woff2")', True, zipsize)
prev = re.sub(r'(src="|url\(")((?:heritage|gradients)/[\w-]+\.jpg)"',
              lambda m: m[1] + "data:image/jpeg;base64," + base64.b64encode((ASSETS / m[2]).read_bytes()).decode() + '"',
              prev)
prev = re.sub(r"<!--@META@-->.*?<!--@END_META@-->\n?", "", prev, flags=re.S)
prev = re.sub(r"/\*@DL@\*/.*?/\*@END_DL@\*/",
              lambda m: 'const fileLink = (href, cls, inner) => `<span class="${cls} is-off" aria-disabled="true">${inner}</span>`;',
              prev, flags=re.S)
head = prev[prev.index("<title>"):prev.index("</head>")]
head = re.sub(r"<!--.*?-->", "", head, flags=re.S)
body = prev[prev.index("<body>") + len("<body>"):prev.index("</body>")]
script_at = body.rindex("<script>")
markup, script = body[:script_at], body[script_at:]
out = (head.strip()
       + '\n<script>document.documentElement.lang="ar";document.documentElement.dir="rtl";</script>\n'
       + '<div dir="rtl" lang="ar">' + markup + "</div>\n" + script)
(BUILD / "azmx-font-preview.html").write_text(out, encoding="utf-8")

files = [p for p in SITE.rglob("*") if p.is_file()]
print(f"docs/: {len(files)} files, {sum(p.stat().st_size for p in files):,} bytes | font zip: {zipsize}"
      f" | preview: {(BUILD / 'azmx-font-preview.html').stat().st_size:,} bytes")
