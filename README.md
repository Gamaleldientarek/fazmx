# Azm X Variable · fazmx.gamaleldien.com

The download page for **Azm X Variable**, the AZM X typeface. It's Arabic-first and right-to-left, with live type animations, a construction figure drawn from the font's own outlines, a type tester, a glyph map and direct downloads.

## What's here

| Path | What it is |
| --- | --- |
| `src/index.src.html` | The page source. Edit this, never `docs/index.html`. |
| `src/build.py` | Builds `docs/` and a one-file preview |
| `src/make_glyphdata.py` | Reads the glyph map data from the font |
| `src/make_construction.py` | Draws the «تجربة» construction figure from the font's outlines |
| `src/license.html`, `src/LICENSE.txt` | The font licence, as a web page and as the copy inside the download ZIP |
| `fonts/` | AzmXVariable in WOFF2, WOFF and TTF. The build copies them from here. |
| `assets/` | Logo and favicon |
| `docs/` | The built site, which GitHub Pages serves. Commit it after every build. |
| `build/` | Generated files and the preview. Not committed. |

## Build

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python src/build.py                     # rebuild docs/ and build/azmx-font-preview.html
python src/build.py --og                # also retake the link-preview image, docs/og.png
python -m http.server -d docs 8000      # then open http://localhost:8000
```

`--og` needs Chromium for Playwright: `python -m playwright install chromium`.

## Publish on GitHub Pages

1. Push this folder to the `main` branch of a public repo, `Gamaleldientarek/fazmx`.
2. In the repo, open **Settings → Pages**. Set the source to **Deploy from a branch**, the branch to **main** and the folder to **/docs**.
3. Where the DNS for gamaleldien.com is managed, add a CNAME record: name `fazmx`, value `gamaleldientarek.github.io`.
4. Once GitHub's DNS check passes, tick **Enforce HTTPS** on the same page.

`docs/CNAME` already holds `fazmx.gamaleldien.com`, so the custom domain survives every build.

## Updating the font

Replace the three files in `fonts/`, keeping their names, and run `python src/build.py`. The build refreshes the glyph map, the construction figure, the file sizes and the ZIP. It also warns if the glyph, character, feature or weight counts in the page's stats row no longer match the font. Update the version number in `src/license.html` and `src/LICENSE.txt`.

## Licence

The font is free for personal and commercial use, but it may not be sold, redistributed on its own, or modified. See `src/LICENSE.txt`. The terms are a draft awaiting review.
