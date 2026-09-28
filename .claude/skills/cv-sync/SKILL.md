---
name: cv-sync
description: >-
  Use when a new CV lands and the website has to catch up, in phrasings like
  "pull from github and download the newest CV, and update my site", "i have
  an updated CV (see Downloads folder of my mac)", "sync my CV to the site",
  "update the website from my new CV", "I added a presentation, put it on the
  site", "the SILICON paper got a major revision, update my site", "update
  everywhere (Research and Teaching and Impact)", "did I miss anything from
  the CV on the website", or "check the site against my CV". Builds the CV
  from its GitHub source (XCharlieCHENG/CV, which Overleaf pushes to), diffs
  it against static/files/CV.pdf, which is the last-synced baseline,
  classifies every hunk as an expected change to apply directly or an
  unexpected one to confirm first, applies the expected ones across
  content/research.md, content/teaching.md, content/impact.md and
  content/cv.md, runs a full CV-against-site reconciliation sweep so nothing
  drifts, replaces the deployed PDF, and builds. Do NOT use for site design,
  layout, or CSS work, for writing a /misc post, or for the deploy itself
  (README.md owns the git and GitHub Pages steps). Do NOT hand the CV pull to
  git-sync, which syncs manuscript repositories; this skill clones the CV
  repository and never pushes to it. Do NOT use to draft the CV PDF; this
  skill reads the CV and never writes it.
---

# CV Sync

The CV is the source of record. The site is a rendering of it under editorial
rules that the CV does not carry, so a sync is a translation and not a copy.
This skill owns the translation.

## Where things are

| Object | Path |
| --- | --- |
| Site root | `~/Library/CloudStorage/GoogleDrive-xccheng@umd.edu/My Drive/Personal Website` |
| CV source | `main.tex` in the GitHub repository `XCharlieCHENG/CV`, which Overleaf pushes to |
| TeX Live 2023 shim for the local build | `.claude/skills/cv-sync/tl23compat.tex` |
| Deployed CV, and the sync baseline | `static/files/CV.pdf` |
| Research page | `content/research.md` |
| Teaching page | `content/teaching.md` |
| Impact page | `content/impact.md` |
| CV page, holding the education table and the PDF embed | `content/cv.md` |
| Homepage strings | `hugo.yaml`, under `params.profileMode` |

`static/files/CV.pdf` is the baseline. It is a byte copy of the CV that
produced the pages as they stand, so a diff against it returns exactly the
changes the site has not absorbed. No separate state file exists and none is
needed. The baseline moves only after every edit it implies has landed.

The site root sits in Google Drive, so its path contains spaces and every shell
reference needs quoting.

The numbered `CV (N).pdf` series in `~/Downloads` ends at `CV (16).pdf`, saved
on Sep 27, 2026, before the first push to GitHub. The GitHub source of that day
already revises its Teaching section. Use a Downloads PDF only when the user
points to one.

## Building the PDF

The repository holds `main.tex` and no PDF, so the sync builds one. Overleaf
compiles this CV with TeX Live 2023, and this machine runs TeX Live 2025. A
plain local build differs from Overleaf's in two places. Longtable 4.19 moves
the strut that opens every table cell into `\everypar`, so a cell that opens
with `\color`, as `\headingfont` and `\subheadingfont` do, gains a blank line.
The 2024 kernel also places the block after a table that crosses a page break
4pt lower. Together they push the CV to four pages and separate two headings
from the entries below them.

The build rolls the kernel back to 2023-11-01 and restores the old cell macro
from `tl23compat.tex`. It leaves `main.tex` untouched:

```bash
git clone --depth 1 https://github.com/XCharlieCHENG/CV.git "$SCRATCH/cv-repo"
cd "$SCRATCH/cv-repo"
cp "<site root>/.claude/skills/cv-sync/tl23compat.tex" .
export SOURCE_DATE_EPOCH=$(git log -1 --format=%ct) FORCE_SOURCE_DATE=1
for i in 1 2; do
  pdflatex -interaction=nonstopmode -jobname=main \
    '\RequirePackage[2023-11-01]{latexrelease}\input{tl23compat}\input{main}'
done
```

`SOURCE_DATE_EPOCH` takes the "Last Updated" month from the last commit, which
is when the user last edited the CV, and makes the build byte-reproducible. The
log carries two expected warnings from the rollback: tabularx requests the
2024-06-01 kernel, and xcolor loads its 2022-06-12 release. `gh` is not
authenticated on this machine, and plain `git` over HTTPS works through the
keychain.

The shim is verified against Overleaf's own PDF of Sep 27, 2026. With that
day's Teaching block restored, the local build puts all 125 text lines on all
three pages where Overleaf puts them. If the Overleaf project moves to a newer
TeX Live (Menu, then Settings), compare one local build against an Overleaf
download before dropping the shim.

## Procedure

### 1. Pull the source, build it, and confirm it is new

Clone and build as in "Building the PDF", then compare:

```bash
git -C "$SCRATCH/cv-repo" log -1 --format='%h %ad %s' --date=iso
md5 "$SCRATCH/cv-repo/main.pdf" static/files/CV.pdf
```

Equal hashes mean the site is already current; report that and stop. A TeX
Live update also changes the bytes. The text diff in step 2 then comes back
empty, and the sync reduces to step 7.

### 2. Extract both to text and diff

```bash
pdftotext -layout static/files/CV.pdf "$SCRATCH/cv_old.txt"
pdftotext -layout "$SCRATCH/cv-repo/main.pdf" "$SCRATCH/cv_new.txt"
diff -u "$SCRATCH/cv_old.txt" "$SCRATCH/cv_new.txt"
```

`pdftotext` is at `/opt/homebrew/bin/pdftotext`. Then read `cv_new.txt` end to
end. The diff alone is not enough for two reasons. A line whose text is
unchanged can appear in the diff because a page break moved it across the "Last
Updated" footer, and that is not a change. And the site can carry drift that
predates this CV, which only the reconciliation sweep in step 6 finds.

A second diff drops the layout, collapses whitespace, and removes the page
furniture. A moved page break then returns nothing, and only content changes
remain:

```bash
norm() { pdftotext "$1" - | sed -E 's/[[:space:]]+/ /g; s/^ //; s/ $//' | grep -vE '^([0-9]+|Last Updated.*)?$'; }
diff <(norm static/files/CV.pdf) <(norm "$SCRATCH/cv-repo/main.pdf")
```

`main.tex` carries the `†` and `‡` markers as source. Its commented-out lines
are not part of the CV and never reach the site.

### 3. Classify every hunk

Sort each hunk into one of the two tables below. A hunk that fits neither goes
to step 5 for confirmation. Guessing is the failure this split exists to
prevent.

### 4. Apply the expected changes

Edit the content files under the conventions in `site-conventions.md`, which
holds the CV-field to site-location map, the venue short names, and the
inclusion rules. Keep each edit surgical and leave the surrounding prose alone.

### 5. Ask about the rest

Batch every uncertain hunk into a single `AskUserQuestion` call, one question
per hunk, each quoting the CV's old and new wording and naming the site line it
would change. Do not send them one at a time and do not apply any of them on a
default.

### 6. Reconciliation sweep

The diff catches what changed since the last sync. This step catches what never
made it. Walk the whole CV against all four pages:

- Every paper in the CV's `W` list appears once on the Research page, in the
  right stream, with the right status string and a working link.
- Each Research section blurb still counts correctly. The second blurb says
  "Two papers develop and validate LLMs as research infrastructure. Two others
  study how AI shapes the decisions that people reach." Inserting a fifth paper
  into that stream makes the sentence false, so the blurb is rewritten with the
  paper, not after it.
- Every talk the user presented himself appears on its year line on the Impact
  page, and every venue on a year line traces back to a CV entry.
- Honors, academic service, teaching, and the education table match.
- The homepage subtitle in `hugo.yaml` still describes the research the
  Research page now lists.

### 7. Replace the deployed PDF

```bash
cp "$SCRATCH/cv-repo/main.pdf" static/files/CV.pdf
```

This is last, because the baseline is only true once the pages match it.

### 8. Verify

```bash
hugo --gc --minify
```

The build must finish with no warnings about the pages touched. Then open the
preview through `preview_start` with the `charliecheng.cc` configuration in
`.claude/launch.json` and check the three pages render, the collapsed abstracts
still open, and the embedded PDF on the CV page shows the new "Last Updated"
month.

### 9. Publish and report

Commit and push to `main` without asking, per the standing instruction in the
project `CLAUDE.md`. Stage the files by name, never `git add -A`, and end the
message with the `Co-Authored-By` line. Then state what changed per file, with
the absolute path and the modification time of each file written.

## Expected changes, applied without asking

| Change in the CV | What it does to the site |
| --- | --- |
| A presentation is added under a paper and carries no `†` | Add the venue's short name to that year's line on the Impact page, alphabetically |
| A paper's review status changes, including a new round, a major revision, an acceptance, or a named journal replacing a bare "Under review" | Rewrite the `<em>` in that paper's `<summary>` on the Research page |
| A paper moves from Work-in-progress to Papers under Review | Rewrite its status and, where the stream orders by status, move it above the remaining work-in-progress entries |
| A `[Paper Link]` or `[Link]` is added or changed | Add or update the `<a>` in that paper's `<summary>` |
| A new honor or grant from the UMD era | Add a line to Honors and Grants, newest first |
| A new journal or conference reviewing line | Add a line to Academic Service, or extend the year range on an existing one |
| A role title, term, or course title changes in Teaching experience | Rewrite the affected line on the Teaching page |
| The "Last Updated" month advances with no other change | Replace `static/files/CV.pdf` and stop |

## Unexpected changes, confirmed first

| Change in the CV | Why it stops |
| --- | --- |
| Anything is deleted: a paper, a presentation, an honor, a service line | A removal from the CV is not always a removal from the site, and it is the one edit that cannot be undone by the next sync |
| A detail the site renders in prose disappears, for example an enrollment count, the word "incoming", or a city | The CV can drop a detail for space while the site still wants it |
| An author list changes | The site prints authors in full and the order carries meaning |
| A paper title changes | The title is the anchor a reader recognizes, and a retitle usually travels with an abstract rewrite |
| A new paper appears | Adding it is expected, but the site needs an abstract and a stream assignment that the CV does not carry. Ask which stream, and take the abstract from the linked SSRN or arXiv page or from the user. Never write one |
| A status change that reads as a withdrawal, a rejection, or a downgrade | Confirm the wording the user wants in public |
| Education, contact details, or affiliation change | These sit on the CV page and in `hugo.yaml`, and a stale one is worse than a missing one |
| A presentation carries `†` or `‡`, or a marker changes | The Impact page lists only self-presented talks, so a marker decides whether the entry appears at all |
| A section blurb on the Research page stops being true | The blurb is the user's prose and a rewrite is a prose decision |
| Anything the expected table does not cover | The tables are the contract; an unlisted change is by definition unexpected |

## Two rules that override everything above

Never invent content the CV does not carry. That covers abstracts, venue full
names, dollar amounts, dates, and stream assignments. Ask instead.

Never edit the CV PDF or `main.tex`. This skill builds the PDF from the GitHub
source and copies it. The LaTeX source lives outside this repository, and the
build adds only `tl23compat.tex`, loaded ahead of `main.tex`.

## Prose on the pages

The site's prose is the user's, so any sentence this skill writes follows the
`writing-voice` skill and its `banned-terms.md`. Present tense, no em dashes,
one claim per sentence, and a subtraction budget on every pass.
