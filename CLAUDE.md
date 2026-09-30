# fazmx: the Azm X Variable font site

This is the download page for **Azm X Variable**, the typeface of AZM X (Azm Experience Company for Information Technology, Riyadh). It will be hosted at https://fazmx.gamaleldien.com on GitHub Pages. The owner's main site, gamaleldien.com, stays on Framer.

The owner is AZM X's Creative & Communications Director and works in Arabic and English. The page is Arabic-first and right-to-left, so any new copy is written in Arabic first, in the page's plain and confident voice.

## Commands

```bash
pip install -r requirements.txt           # Python 3.10+
python src/build.py                       # builds docs/ and build/azmx-font-preview.html
python src/build.py --og                  # also retakes docs/og.png (needs: python -m playwright install chromium)
python -m http.server -d docs 8000        # view at http://localhost:8000
```

- Rebuild after any change to `src/`, `fonts/` or `assets/`.
- Commit `docs/` together with the source. GitHub Pages serves `docs/` as it is, with no build step.
- Retake `og.png` with `--og` whenever the hero changes. A plain build keeps the existing one.

## Layout

- **`src/index.src.html`**: the whole page (about 1,400 lines): HTML, CSS, and one script wrapped in an IIFE.
  - Never edit `docs/index.html`, because every build overwrites it.
  - `build.py` fills these placeholders:
    - `/*@FONTSRC@*/…/*@END@*/`: the font URLs. The preview inlines the WOFF2 as base64 instead.
    - `<!--@LOGO@-->` (used twice), `<!--@CONSTRUCTION@-->` and `/*@GLYPHS@*/{}`.
    - `/*@PREVIEW@*/false`, `/*@ZIPSIZE@*/` and `/*@SIZE:<font file>@*/`.
    - `<!--@META@-->…<!--@END_META@-->`: the canonical, Open Graph and Twitter tags, which the preview drops.
    - `/*@DL@*/…/*@END_DL@*/`: the download links. The preview swaps in disabled spans, because the claude.ai viewer blocks downloads.
- **`src/make_glyphdata.py`** writes `build/glyphdata.json` for the glyph map.
  - The letter sets come from the font's character map. The symbols tab is a hand-picked list.
  - The `init`, `medi` and `fina` flags record whether HarfBuzz gives a letter its own glyph in that position.
- **`src/make_construction.py`** writes `build/construction.svg`, the «تجربة» figure in `#build`. It uses the real outlines at wght 700: letter bodies, rhombus dots, Bézier points on ج and ة, and a column of dots that measures the alef.
- **`src/license.html` and `src/LICENSE.txt`**: the licence as a web page, and as the text file inside the download ZIP.
- **`fonts/`**: the only copy of the font files. The build copies them into `docs/fonts/` and the ZIP.
- **`assets/`**: the navy logo SVG, which the build recolours to `currentColor`, and the favicon.
- **`docs/`**: the built site. It holds `index.html`, `license.html`, `fonts/`, `downloads/AzmX-Variable.zip`, `og.png`, `favicon.png`, `CNAME` and `.nojekyll`. The ZIP is deterministic, stamped with the font's own date, so an unchanged font gives an unchanged ZIP.
- **`build/`**: generated files, not committed.

## Page map, top to bottom

1. Header. Nav links: البناء، التشريح، الأوزان، الحركة، جرّب الخط، رموز مدمجة، الحروف، أسئلة. Also the motion toggle `#motionBtn`.
2. Hero `#top`.
3. Construction `#build`.
4. `#story`, which still has placeholder copy.
5. `#stats`.
6. `#anatomy`.
7. `#weights`.
8. `#motion`: 12 tiles and a marquee band. The tiles are نَفَس، موجة، مغناطيس، مَدّ، كتابة حيّة، الرقم وزنه، سُلَّم، الأوزان الثمانية، أثر، مُرسَل، هبوط، تمرير.
9. `#tester`: presets, weight and size, alignment, and swsh and dlig toggles.
10. `#marks`: `#KSA`, `#RIAL` and the logotypes.
11. `#glyphs`.
12. `#inuse`.
13. `#faq`. The first question is «هل الخط مجاني؟».
14. `#download`.
15. Footer, with the theme toggle `#themeBtn`.

## Design rules (AZMX design system)

- **Colours.** Navy #040038 for headings and inverse surfaces. Electric #001AFF for accents, #5D8FFF in dark mode.
  - The tokens are CSS variables at the top of the stylesheet.
  - Dark mode follows the system unless `html[data-theme]` is set.
- **Shapes.** Square corners, and hairline rules instead of cards, on an asymmetric 12-column grid that anchors top-right.
- **Spacing.** `--s1`…`--s9` = 4, 8, 16, 24, 40, 64, 96, 128 and 160 px.
- **Gradient.** `--grad` (145deg, #040038 → #01006E 55% → #001AFF) is used only on the download section.
- **No chevrons anywhere.** The owner asked for them to be removed.

## Decisions so far

- **No template.** The owner rejected every ready-made Framer and Webflow template, so the page is hand-built. Its reference is font.thmanyah.com.
- **Hero headline.** «نكتـب بعـزم، / بحـرفٍ يشبهنـا.», the owner's pick. Each `ـ` marks a kashida that the hero stretches. The subline rolls through للعناوين، للنصوص، للواجهات، للّافتات، للعروض.
- **Construction section.** It follows Thmanyah's "The Answer" section, but is built on our own rhombus dot. Heading: «كل حرف يبدأ من نقطة.»
- **Hosting.** GitHub Pages, from the public repo `Gamaleldientarek/fazmx`, branch `main`, folder `/docs`.
- **Downloads.** Direct, with no email capture: one ZIP plus the three separate files.
- **Licence.** Free for personal and commercial use. The files may not be sold, redistributed on their own, or modified. This is a draft that still needs review by the owner and a lawyer.

## How the animation works

- **One `requestAnimationFrame` loop.** Register work with `every(el, fn)`. It only runs while motion is on and while the element's nearest `[data-watch]` ancestor is on screen: an IntersectionObserver toggles `data-live` on it.
- **Off-screen CSS pauses.** CSS animations inside an off-screen `[data-watch]` are paused too.
- **Motion switch.** Motion starts off under `prefers-reduced-motion`. `#motionBtn` toggles the `motion-off` class on `<html>`.
- **Hero effects:**
  - Per-letter weight tide: `520 + 240·sin(t/700 − i·0.42)`.
  - Breathing kashida, tracked in `heroKLast`.
  - Ink surge when the hero first appears, letter by letter.
  - Pointer magnet, with radius `max(140, 16% of the title width)`.
  - Scroll exhale.
  - The subline word rolls every 2.6 s.
  - `paintHero` also drives the meter bars and the `#heroLive` readout.
- **Construction figure.** Pure CSS keyframes (`bfDraw`, `bfDot`, `bfCon`) on a 10 s loop, staggered with `--d`.
  - A negative delay makes the first frame the finished word.
  - The point markers are hidden below 600 px.

## Arabic text: what breaks easily

- **Split text.** `split()` wraps each letter in a span and adds a ZWJ (U+200D) on every side that joins, based on `joinType()` (D/R/C/T/U).
  - Lam-alef stays as one cluster, and harakat stay with the letter before them.
  - A hidden `.sr` copy keeps the text readable by screen readers.
- **Copying.** The copy handler strips the ZWJs, the `.sr` copies and the hidden rolling words from whatever the reader copies. After adding split text, test copy and paste.
- **Logotypes.** `rlig` turns خادم الحرمين الشريفين، ولي العهد، المعالي، صلى الله عليه وسلم and الله into logotypes wherever Azm X renders them. To show one as plain text in a label or the FAQ, either:
  - put a ZWNJ (U+200C) before a space inside the phrase, or
  - set `font-feature-settings: "rlig" 0`, but only on text with no lam-alef, because turning off rlig breaks lam-alef.
- **Long logotypes.** A logotype that wraps falls apart. Keep it on one line and size it with container units, as `.mark-out.xl` does.
- **Kashida.** U+0640 can only follow a letter that joins on both sides.
- **Symbols.** `#KSA` and `#RIAL`, in any letter case, become the Saudi emblem and the riyal sign through `calt`.

## Font facts

All of these are verified against the font. `build.py` warns if the numbers in `#stats` stop matching.

- **Version.** Azm X Variable v2.004. Weight axis 100–900, with named instances at 100, 200, 300, 400, 500, 600, 700 and 900. There is no 800.
- **Counts.** 803 glyphs, 552 Unicode characters and 24 OpenType feature tags.
- **Metrics.** 1000 units per em, ascender 950, descender −500, alef and cap height 680, x-height 476.
- **Swashes.** `swsh` works on final ب ت ث د ذ ع غ ف, for example شغف، سعد، ذهب. The optional ligature `dlig` gives في.
- **Dots.** They are rhombi: about 162 units at wght 700, 55 at 100 and 170 at 900. A few dots are 142–145 units. The alef is about four dots tall at 700.

## Checking changes

Serve `docs/` and use Playwright with Chromium:

- Check two sizes, desktop 1440×900 and phone 390×844, in both light and dark.
- Check there are no console errors and no sideways scroll: `document.documentElement.scrollWidth <= innerWidth`.
- Check that the split text joins correctly, and that copying the hero headline gives clean text.
- Check that the download links point to `downloads/AzmX-Variable.zip` and `fonts/…`.

## Deploying

1. Create an empty public repo, `Gamaleldientarek/fazmx`, and push to `main`.
2. In Settings → Pages, choose Deploy from a branch → `main` → `/docs`.
3. At the DNS host for gamaleldien.com, add a CNAME record: `fazmx` → `gamaleldientarek.github.io`.
4. Once the DNS check passes, turn on Enforce HTTPS.

## Open items

The site has been live at https://fazmx.gamaleldien.com since 2026-09-30. The current state, the to-do list and the lessons learned are in `HANDOFF.md`. Update it at the end of each session.
