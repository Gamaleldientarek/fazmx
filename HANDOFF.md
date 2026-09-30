# Session hand-off

Last session: **2026-09-30** (Cairo time, UTC+2). To pick up from here, read `CLAUDE.md` first, then this file. The build and publish commands are in `README.md`.

## Where things stand

- **Live:** https://fazmx.gamaleldien.com, served by GitHub Pages from `main` → `/docs`.
  - Enforce HTTPS is on, and plain `http://` redirects to `https://`.
  - The certificate is from Let's Encrypt and expires on 2026-12-29. GitHub renews it automatically.
- **Repo:** https://github.com/Gamaleldientarek/fazmx (public).
- **DNS:** gamaleldien.com is on **Cloudflare**. The record is a CNAME, `fazmx` → `gamaleldientarek.github.io`, set to **DNS only (grey cloud)**.
  - Keep it grey. If Cloudflare proxies the record, GitHub can't check the domain or renew the certificate.
- **Main site:** gamaleldien.com is still on Framer, untouched.

## Done this session

1. Built `docs/`. The build was clean, and the numbers in `#stats` match the font.
2. Checked the site locally and then live:
   - desktop 1440×900 and phone 390×844, in light and dark
   - no console errors, no sideways scroll, and the font loads
   - the download links point to `downloads/AzmX-Variable.zip` and `fonts/…`
   - the page, licence, ZIP, font files, `og.png` and favicon all return 200
   - the canonical and Open Graph URLs use `https://`
3. Started the git repo, made the first commit, created the GitHub repo and pushed.
4. Turned on Pages with the custom domain, added the DNS record, got the certificate and turned on Enforce HTTPS.

## Next up

1. **Copying the hero headline copies the kashidas.**
   - The copied text includes however many stretched kashidas the animation was showing at that moment. For example, the live site gave «نكتـــب بعزم، بحــرفٍ يشبهنــــا.».
   - The ZWJs are already stripped. The fix goes in the copy handler in `src/index.src.html`.
   - Decide first what "clean" should mean. The recommendation is plain text with no tatweel: «نكتب بعزم، بحرفٍ يشبهنا.». The other choice is the source spelling, «نكتـب بعـزم، بحـرفٍ يشبهنـا.».
2. **Verify `gamaleldien.com` in GitHub** (profile Settings → Pages → Verified domains). Then no other GitHub account can put a Pages site on its subdomains.
3. **Replace the placeholder copy in `#story`.**
4. **Get the licence reviewed** by the owner and a lawyer. It's still a draft.

## Lessons from this session

- **Certificate stuck after the DNS check passed.** Remove the custom domain in Settings → Pages, then add it again; this time that got the certificate approved at once.
  - On a branch source, GitHub records this as two commits ("Delete CNAME", "Create CNAME"). Run `git pull` afterwards.
- **Cloudflare from the command line.** The `wrangler` login can only read zones, so it can't change DNS. Edit records in the Cloudflare dashboard, or make an API token with Zone → DNS → Edit for this zone.
- **Python environment.** This folder syncs through Google Drive, so keep the virtual environment somewhere outside it (for example `~/.venvs/fazmx`), not in `.venv/` here.
- **Fresh DNS records.** Right after a new record is added, a computer that looked the name up earlier may still fail to find it for a few minutes. This clears by itself.

## Shipping a change

Edit `src/`, then run `python src/build.py`. Commit `src/` and `docs/` together and push to `main`. Pages redeploys in about a minute. If the hero changed, run `python src/build.py --og` as well.
