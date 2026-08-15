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

## Where this lives

```
~/Library/CloudStorage/GoogleDrive-xccheng@umd.edu/My Drive/Personal Website
```

The folder sits inside Google Drive, so its path contains spaces and needs
quoting in the shell. A shortcut in `~/.zshrc` saves the typing:

```bash
alias website='cd "$HOME/Library/CloudStorage/GoogleDrive-xccheng@umd.edu/My Drive/Personal Website"'
```

Google Drive on this machine intermittently refuses file operations and has
corrupted git refs before. If git reports a detached HEAD, a missing object, or
an `EPERM`, delete the folder and clone it again:

```bash
git clone --recurse-submodules https://github.com/XCharlieCHENG/XCharlieCHENG.github.io.git
```

Anything already pushed is safe on GitHub, so nothing is lost.

## Preview locally

```bash
hugo server -D
```

Then open <http://localhost:1313>. The page reloads as you save.

## Publish

Stage the files you changed by name:

```bash
git add content/research.md
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
- Old Google Sites URLs under `/blog/` redirect to `/misc/` via the `aliases`
  field in each post's front matter.

## Switching the domain over to this site

Until the DNS cutover, the site is served from
<https://XCharlieCHENG.github.io> and `charliecheng.cc` still points at the old
Google Sites page. There is deliberately no `static/CNAME` file, because its
presence makes GitHub Pages redirect the `github.io` address to the custom
domain, which would leave nothing to check against before the switch.

At cutover, create the file and push:

```bash
printf 'charliecheng.cc\n' > static/CNAME
git add static/CNAME && git commit -m "Point Pages at the custom domain" && git push
```

Then, at Namecheap under Domain List, Manage, Advanced DNS, add four A records
on host `@` pointing at `185.199.108.153`, `185.199.109.153`, `185.199.110.153`
and `185.199.111.153`, and change the `www` CNAME from `ghs.googlehosted.com`
to `XCharlieCHENG.github.io.`.

Leave the five `eforward*.registrar-servers.com` MX records and both TXT
records alone. They run email forwarding for the domain.
