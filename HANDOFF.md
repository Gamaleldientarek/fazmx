# Session hand-off

Last session: **2026-10-01** (Cairo time, UTC+2). To pick up from here, read `CLAUDE.md` first, then this file. The build and publish commands are in `README.md`.

## Where things stand

- **Live:** https://fazmx.gamaleldien.com, served by GitHub Pages from `main` → `/docs`.
  - Enforce HTTPS is on, and plain `http://` redirects to `https://`.
  - The certificate is from Let's Encrypt and expires on 2026-12-29. GitHub renews it automatically.
  - The origin section went live on 2026-10-01. It was pushed through the GitHub API, so this folder must be synced before the next edit (see "Next up").
- **Repo:** https://github.com/Gamaleldientarek/fazmx (public).
- **DNS:** gamaleldien.com is on **Cloudflare**. The record is a CNAME, `fazmx` → `gamaleldientarek.github.io`, set to **DNS only (grey cloud)**.
  - Keep it grey. If Cloudflare proxies the record, GitHub can't check the domain or renew the certificate.
- **Main site:** gamaleldien.com is still on Framer, untouched.

## Done on 2026-10-01

1. **Added the origin section `#origin` («الأصل»)** between the hero and `#build`. It replaces the placeholder `#story`.
   - Source: the owner's deck «عرض خط السعودية الرقمي V5.0» (`.key` and `.pdf`, in ~/Downloads on 2026-10-01).
   - Copy: Azm X is a modern Naskh, inspired by Saudi manuscripts of the 13th century AH. It closes on the owner's line «خطٌّ سعودي يشبهنا، بأسلوب رقمي حديث.»
   - A manuscript page and six letter pairs, as in the deck. Each word inks in from thin to bold.
   - Images in `assets/heritage/`. The crops were cut from the deck's Keynote originals and converted from CMYK to sRGB. The illuminated-page crops come from the deck's sharper detail scans, not from the full page.
2. Added «الأصل» to the nav. `build.py` now copies `assets/heritage/` to `docs/heritage/` and inlines the images in the preview.
3. Checked a full build in a scratch copy at 1440, 1240, 1110, 1000, 900, 390 and 360 px, light and dark:
   - no console errors and no sideways scroll; every word fits its cell; the nav fits at 1110 px
   - copying «السعوديين» gives clean text
   - reduced motion and the motion switch both leave the words bold
   - the preview's inlined images load
4. **Deployed.** Shell commands could not write anywhere under ~/Documents in this session, so local git was not possible. The build was made in a scratch copy, and one commit went straight to `main` through the GitHub API. It holds `src/`, `assets/heritage/`, `docs/index.html`, `docs/heritage/`, `CLAUDE.md` and this file.

## Next up

1. **Sync this folder with GitHub before editing anything.**
   - This clone is one commit behind `main`, and it shows that commit's changes as uncommitted edits. Run `git fetch && git reset --hard origin/main`. Nothing is lost, because the files here already match that commit.
   - Then delete the stray `assets/heritage/.probe`.
2. **Redesign the `#stats` band** (٨٠٣ / ٥٥٢ / ٢٤ / ٨). The owner asked for this on 2026-10-01. In dark mode it shows as a plain white strip.
3. **Download form: ask for name and email.** The owner asked for this on 2026-10-01. It reverses the "no email capture" decision in `CLAUDE.md`. Waiting on one decision: where the submissions are stored.
4. **Confirm the letter in حفظ.** The deck's caption names حـ, but its red highlight and its manuscript crop (from «لظنهم») both show ظ. The page shows ظ.
5. **Confirm where the manuscripts come from, and that we may publish the scans.** The deck gives no collection or credit. If there is one, add it to the plate's caption.
6. **Copying the hero headline copies the kashidas.**
   - The copied text includes however many stretched kashidas the animation was showing at that moment. For example, the live site gave «نكتـــب بعزم، بحــرفٍ يشبهنــــا.».
   - The ZWJs are already stripped. The fix goes in the copy handler in `src/index.src.html`.
   - Decide first what "clean" should mean. The recommendation is plain text with no tatweel: «نكتب بعزم، بحرفٍ يشبهنا.». The other choice is the source spelling, «نكتـب بعـزم، بحـرفٍ يشبهنـا.».
7. **Verify `gamaleldien.com` in GitHub** (profile Settings → Pages → Verified domains). Then no other GitHub account can put a Pages site on its subdomains.
8. **Get the licence reviewed** by the owner and a lawyer. It's still a draft.

## Where the deck and the page disagree

The page was left as it is on these. Raise them with the owner before the deck goes out again.

- **Weights.** The deck lists 7, with no Medium. The font has 8 named instances, and the page says 8.
- **Languages.** The deck says 5, including Kurdish. The page lists Arabic, Latin, Persian and Urdu.

## Lessons

- **Shell commands may be unable to write under ~/Documents.** In some sessions they get "Operation not permitted" there, even with the sandbox off, while the Edit and Write tools still work.
  - Work around it: edit source with the file tools, then build and test in a scratch copy.
  - To ship without local git, push through the GitHub API with `gh api`: blobs, then a tree on top of `main`, then a commit, then move `refs/heads/main`. Then sync the clone with `git fetch && git reset --hard origin/main`.
- **Keynote files are zip archives.** The original images sit in `Data/`, often sharper than the PDF export.
  - They can be CMYK. Convert them with the profile embedded in the file (here "U.S. Web Coated (SWOP) v2") through Pillow's ImageCms. This matches macOS ColorSync; `pdftoppm` renders them noticeably warmer.
- **Restart the test server after every build.** `build.py` deletes and recreates `docs/`, so an `http.server` started before the build keeps serving the deleted folder and returns 404s.
- **Certificate stuck after the DNS check passed.** Remove the custom domain in Settings → Pages, then add it again; this time that got the certificate approved at once.
  - On a branch source, GitHub records this as two commits ("Delete CNAME", "Create CNAME"). Run `git pull` afterwards.
- **Cloudflare from the command line.** The `wrangler` login can only read zones, so it can't change DNS. Edit records in the Cloudflare dashboard, or make an API token with Zone → DNS → Edit for this zone.
- **Python environment.** This folder syncs through Google Drive, so keep the virtual environment somewhere outside it (for example `~/.venvs/fazmx`), not in `.venv/` here.
- **Fresh DNS records.** Right after a new record is added, a computer that looked the name up earlier may still fail to find it for a few minutes. This clears by itself.

## Shipping a change

Edit `src/`, then run `python src/build.py`. Commit `src/` and `docs/` together and push to `main`. Pages redeploys in about a minute. If the hero changed, run `python src/build.py --og` as well.
