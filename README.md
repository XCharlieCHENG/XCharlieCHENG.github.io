# charliecheng.cc

Personal academic site for Xiang (Charlie) Cheng. Hugo + PaperMod, deployed to
GitHub Pages. Design adapted from [raveeshmayya.com](https://raveeshmayya.com).

## Editing

Everything you edit lives in `content/`, as plain Markdown:

| File | Page |
| --- | --- |
| `content/_index.md` | Homepage |
| `content/research.md` | Research |
| `content/teaching.md` | Teaching |
| `content/cv.md` | CV |
| `content/misc/_index.md` | Miscellaneous, the intro text |
| `content/misc/*.md` | One file per post |

Images go in `static/images/`, files (the CV PDF) in `static/files/`. Site-wide
settings (title, nav menu, social links, footer) are in `hugo.yaml`.

## Preview locally

```bash
cd ~/Sites/charliecheng.cc
hugo server -D
```

Then open <http://localhost:1313>. The page reloads as you save.

## Publish

```bash
git add -A
git commit -m "Update research page"
git push
```

GitHub Actions builds and deploys. The site is live about a minute later.

## Adding a post

Create `content/misc/some-slug.md`:

```markdown
---
title: "Post Title"
date: 2026-08-14
---

Body text.
```

## Notes

- `themes/PaperMod` is a git submodule. Clone with
  `git clone --recurse-submodules`. Update it with
  `git submodule update --remote --merge`.
- `static/CNAME` holds the custom domain. Do not delete it; GitHub Pages reads
  it on every deploy.
- Old Google Sites URLs under `/blog/` redirect to `/misc/` via the `aliases`
  field in each post's front matter.
