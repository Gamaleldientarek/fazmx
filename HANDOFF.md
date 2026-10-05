# Session hand-off

Last session: **2026-10-05** (Cairo time). To pick up from here, read `CLAUDE.md` first, then this file. The build and publish commands are in `README.md`.

## Before you touch anything: sync this folder

The shell still cannot write here (checked again on 2026-10-05), so changes reach GitHub from a scratch clone (see Lessons). This folder is therefore behind `main`: its text files match, but the images in `assets/heritage/` and `assets/gradients/` and the built `docs/` are only on GitHub. Nothing is lost by syncing:

```bash
git fetch && git reset --hard origin/main
rm assets/heritage/.probe        # a stray test file; it is not tracked
```

## Where things stand

- **Live:** https://fazmx.gamaleldien.com, served by GitHub Pages from `main` → `/docs`. Checked on the live site at nine widths (360 to 1440 px), light and dark, with no errors.
  - Enforce HTTPS is on. The Let's Encrypt certificate expires on 2026-12-29, and GitHub renews it automatically.
- **Repo:** https://github.com/Gamaleldientarek/fazmx (public). The latest site change is `3e2c847` (2026-10-05). The 2026-10-01 changes are in `253eea9`, `e87fd4d` and `c02becb`.
- **DNS:** gamaleldien.com is on **Cloudflare**: CNAME `fazmx` → `gamaleldientarek.github.io`, **DNS only (grey cloud)**. Keep it grey, or GitHub can't check the domain or renew the certificate.
- **Download form data:** the Sheet "Azm X: downloads", tab "Downloads", in gibrahim@azmx.sa:
  https://docs.google.com/spreadsheets/d/1xHmYLdz3GHs31Daunwp03ppSBwhQdRRVXO_HcxvwbZg/edit
  - It is fed by the Apps Script project "Azm X downloads form", deployed as a web app. How it works and how to change it are in `CLAUDE.md` under Downloads.
  - It held only its header row at the end of the session. All test rows were deleted.
- **Main site:** gamaleldien.com is still on Framer, untouched.

## Done on 2026-10-05

One commit, `3e2c847`, pushed with the owner's approval and checked on the live site:

1. **Light by default.** The page ignores the system's dark setting. Dark mode comes only from the footer toggle. The licence page is light only.
2. **Black sections.** The class `dark` on a section makes it pure black (the owner asked for "more black" than Neutral 950). Used on «بالأرقام» (navy before), «الحركة» and «رموز مدمجة».
3. **Gradients from the AZMX image library.** The download section uses `gradient-004.jpg` and the cover poster in `#inuse` uses `gradient-026.jpg`, self-hosted in `assets/gradients/`. Alternatives shown to the owner: 011 or 032 for the download, 015 or 006 for the poster.
4. **Brand check.** `brand-check.py` from the azmx-brand skill flags `#000000` as off-palette; that is the owner's call. Its chevron blockers are the ‹ › characters in the character wall and glyph map, not decoration.

## Done on 2026-10-01

Three commits, each pushed with the owner's approval:

1. **`253eea9`: the origin section «الأصل».** It sits between the hero and «البناء», and replaces the placeholder `#story`.
   - Source: the owner's deck «عرض خط السعودية الرقمي V5.0» (`.key` and `.pdf` in ~/Downloads). Azm X is a modern Naskh, inspired by Saudi manuscripts of the 13th century AH. The section closes on the owner's line «خطٌّ سعودي يشبهنا، بأسلوب رقمي حديث.»
   - It shows a manuscript page and the deck's six letter pairs, each word inking in from thin to bold. The images are in `assets/heritage/`, cut from the Keynote originals and converted from CMYK to sRGB.
   - «الأصل» is the first nav link. `build.py` copies the images to `docs/heritage/` and inlines them in the preview.
2. **`e87fd4d`: the numbers band «بالأرقام», redesigned.** It is a dark band in both themes; before, it showed as a white strip in dark mode. Each number sits on its proof, read from the font at build time:
   - ع in its five shapes
   - the character wall
   - the 24 feature tags
   - ع at the eight weights
3. **`c02becb`: the download form.** It asks for name and email before the files, and saves them to the Sheet above.
   - The owner chose a Google Sheet and approved the privacy line as written.
   - The Sheet and script were set up in the owner's Chrome. The owner clicked Allow on Google's permission screen.
   - Tested: bad email rejected, honeypot ignored, a real entry saved from the page, and the reply readable from the live domain.

## Next up

1. **Owner decisions:**
   - **The letter in حفظ.** The deck's caption names حـ, but its red highlight and its manuscript crop (from «لظنهم») both show ظ. The page shows ظ.
   - **Credit and rights for the manuscript scans.** The deck names no collection. If there is one, add it to the plate's caption.
   - **The deck disagrees with the page.** The deck lists 7 weights (no Medium) and 5 languages including Kurdish. The font has 8 named weights, and the page lists Arabic, Latin, Persian and Urdu. The page was left as it is. Fix the deck before it goes out again.
2. **Optional hardening for the form script.**
   - Add `/** @OnlyCurrentDoc */` at the top of the Apps Script, so it can reach only this Sheet instead of all the account's spreadsheets.
   - Then publish it as a new version of the same deployment (see `CLAUDE.md`), and allow again when asked.
3. **Copying the hero headline copies the kashidas.**
   - The copied text includes however many stretched kashidas the animation was showing, for example «نكتـــب بعزم، بحــرفٍ يشبهنــــا.».
   - The fix goes in the copy handler in `src/index.src.html`.
   - Recommended result: plain text with no tatweel, «نكتب بعزم، بحرفٍ يشبهنا.».
4. **Verify `gamaleldien.com` in GitHub** (profile Settings → Pages → Verified domains), so no other account can put a Pages site on its subdomains.
5. **Get the licence reviewed** by the owner and a lawyer. It's still a draft.

## Lessons

- **Shell commands could not write anywhere under ~/Documents** ("Operation not permitted", even with the sandbox off), while the Edit and Write tools still worked. Local builds and local git failed. The workaround that shipped all three commits:
  - Edit `src/` with the file tools.
  - Copy the repo to a scratch folder, then build and test there with `~/.venvs/fazmx/bin/python`.
  - Commit to `main` through the GitHub API with `gh api`: blobs, then a tree on top of the current `main`, then a commit, then PATCH `refs/heads/main`. Use the author identity from earlier commits.
  - Then sync this folder as above.
- **Simpler than the API route (2026-10-05): a scratch clone with plain git.** Clone `main` into the scratch folder, edit `src/` here with the file tools, `cp` the edited files into the clone, build and test there, then `git commit` and `git push` from the clone. gh's HTTPS login handles the push. Set the clone's author to the noreply identity first.
- **An API commit may not start a Pages build.** If none has started after a minute, run `gh api -X POST repos/Gamaleldientarek/fazmx/pages/builds`. The site was live about 30 s later.
- **Testing the Apps Script with curl:**
  - Use `curl -sL --data-urlencode …`, never `-X POST -L`. With `-X POST`, curl repeats the POST at Google's redirect target and gets an error page.
  - The script has already run on the first hop by then, so that row is still written.
  - The first minutes after a new deployment can fail now and then. Test again before you debug.
- **Reading the Sheet without clicking around:** from a Chrome tab on the Sheet, run `fetch('/spreadsheets/d/<id>/gviz/tq?tqx=out:csv&sheet=Downloads')`.
  - To select cells on another tab, type a range such as `Downloads!A2:D4` into the Name box.
- **Chrome automation on Google pages is flaky.**
  - "Couldn't determine which page" means the tab lost focus: navigate it again.
  - Elements found with `find` click more reliably than coordinates.
  - The Apps Script editor exposes `window.monaco`, so `monaco.editor.getModels()[0].setValue(code)` loads a script exactly. Typed code gets auto-closed brackets.
- **Keynote files are zip archives.** The original images sit in `Data/`, often sharper than the PDF export.
  - They can be CMYK. Convert them with the profile embedded in the file (here "U.S. Web Coated (SWOP) v2") through Pillow's ImageCms. This matches macOS ColorSync; `pdftoppm` renders them too warm.
- **Restart the test server after every build.** `build.py` deletes and recreates `docs/`, so a server started earlier keeps serving the deleted folder.
- **Certificate stuck after the DNS check passed.** Remove the custom domain in Settings → Pages, then add it again.
  - On a branch source, GitHub records that as two commits ("Delete CNAME", "Create CNAME"). Pull afterwards.
- **Cloudflare from the command line.** The `wrangler` login can only read zones. Edit DNS in the dashboard, or make an API token with Zone → DNS → Edit.
- **Python environment.** Keep the virtual environment outside this Google Drive folder (`~/.venvs/fazmx`).

## Shipping a change

Edit `src/`, then run `python src/build.py`. Commit `src/` and `docs/` together and push to `main`; Pages redeploys in about a minute. If the hero changed, also run `python src/build.py --og`. If the shell can't write here, use the API route under Lessons.
