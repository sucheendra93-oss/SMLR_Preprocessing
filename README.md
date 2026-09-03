# SMLR Exam Kit

Static site of SMLR session notes. Plain HTML/CSS/JS, built locally with a
small Python script, deployed on GitHub Pages with no CI build step.

## Layout

```
manifest.json           ordered list of chapters (id, file, title, eyebrow, description)
content/0N-slug.html     chapter body only (hero + <section> blocks)
templates/page.html      chapter document shell (head, sidebar, footer script)
templates/index.html     landing page shell
assets/css/style.css     shared design system
assets/js/theme.js       theme toggle + syntax highlighting init
build.py                 stitches content + templates -> index.html, chapters/*.html
chapters/                generated output (committed)
index.html               generated output (committed)
```

`chapters/` and the root `index.html` are generated files, committed to the
repo so GitHub Pages can serve them directly with no build step.

## Adding a chapter

1. Create `content/0N-slug.html` containing just the page body:
   ```html
   <div class="hero">
     <span class="eyebrow">...</span>
     <h1>...</h1>
     <p class="lede">...</p>
   </div>

   <section class="sec" id="some-id" data-group="Group label" data-badge="1">
     <div class="sec-lead"><span class="num">1</span><h2>Section title</h2></div>
     <p>...</p>
   </section>
   ```
   - `data-group` puts a divider label above this entry in the sidebar; repeat
     the same label on consecutive sections to group them.
   - `data-badge` is the small glyph/number shown next to the section link.
   - The sidebar's in-page nav and headings are generated automatically from
     each `<section id>` + its first `<h2>` — no nav markup to hand-write.

2. Add an entry to `manifest.json`:
   ```json
   { "id": "02", "file": "02-slug.html", "title": "...", "eyebrow": "...", "description": "..." }
   ```

3. Rebuild and commit:
   ```
   python3 build.py
   git add -A && git commit -m "Add chapter 2"
   ```

## Deploying on GitHub Pages

One-time setup:

```
git init                       # if not already a repo
git add -A
git commit -m "Initial site"
gh repo create <your-repo-name> --public --source=. --push
```

Then in the GitHub UI: **Settings → Pages → Build and deployment** →
Source: **Deploy from a branch** → Branch: **main**, folder **/ (root)**.
The site will be live at `https://<username>.github.io/<your-repo-name>/`
within a couple of minutes. Every subsequent `git push` to `main` redeploys
automatically — no GitHub Actions workflow is needed since there's no build
step at deploy time (the generated HTML is already committed).
