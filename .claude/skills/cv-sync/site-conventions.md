# Site Conventions

The rules the CV does not carry. Read this before editing any content file, and
extend it whenever the user corrects a rendering decision.

## Research page, `content/research.md`

Two streams, each an `<h2>`, each followed by a prose blurb and then one
`<ol class="paper-list">`. Every paper is one `<li>` holding a `<details>`:

```html
<li><details><summary><strong>TITLE</strong><br>AUTHORS<br><em>STATUS</em> · <a href="URL">Paper</a></summary><p class="paper-abstract">ABSTRACT</p></details></li>
```

The whole entry is one physical line. The CSS in
`assets/css/extended/custom.css` suppresses the disclosure triangle, so the
title itself is the affordance.

Stream assignment follows the method, not the topic. The first stream,
"Economics of Generative AI and Agents", holds the game-theoretic modeling
papers. The second, "LLMs for Research and Decision-Making", holds the papers
that build or study LLMs as instruments. A paper that fits neither is a
question for the user.

Within a stream, papers under review come first and work in progress comes
last. Beyond that the order follows the stream's blurb, which describes the
grouping in prose. The second blurb currently pairs the two research
infrastructure papers and then the two decision papers, in that order, so an
insertion has to keep the blurb true.

Authors are printed in full, in CV order, with "and" before the last one.
"Xiang Cheng and Manmohan Aseri"; "Xiang Cheng, Manmohan Aseri, Siva
Viswanathan, and Esther Gal-Or".

Status strings capitalize Review even where the CV writes it lowercase.

| CV wording | Site wording |
| --- | --- |
| Under review at Management Science | Under Review at Management Science |
| Under 3rd Round Review at Information Systems Research | Under 3rd Round Review at Information Systems Research |
| Major Revision at Management Science | Major Revision at Management Science |
| Modeling in progress, Drafting in progress | Work in progress |
| Large-scale experiment in progress | Work in progress, large-scale experiment underway |

Link labels sit after the status, separated by ` · `. An SSRN or arXiv URL is
labelled `Paper`, a YouTube URL is `Presentation`, and an AIS Electronic
Library URL is `ICIS 2025 Proceedings` or the equivalent proceedings name.

A work-in-progress entry carries a one-sentence description in place of an
abstract, because no abstract exists yet. It is the user's sentence, not a
generated one.

## Teaching page, `content/teaching.md`

One `<h2>` per institution, then one `<h3>` per course carrying the course code
in parentheses. Under each heading comes a `Role, Term` line and then a prose
paragraph of one or two sentences. Entries are separated by `---`.

The CV writes teaching as bullets. The site writes prose, so a CV bullet is
rewritten into a sentence and never pasted in as a fragment.

## Impact page, `content/impact.md`

Honors and Grants lists the UMD era only. The two Renmin University awards on
the CV are deliberately absent, and finding them absent is not a discrepancy to
fix. The format expands the CV's abbreviation:

```
- Smith Internal Research Grant, University of Maryland, $17,000 · 2026
```

Newest first, and a range for a multi-year award.

Conference Presentations groups by the year in the CV's parenthetical date, one
line per year, newest year first, venue short names separated by ` · ` and
sorted alphabetically inside the line:

```
**2026** · ACM Collective Intelligence · CIST · Fisher AI in Business · WAICI
```

A venue appears once per year no matter how many papers it hosted.

Three inclusion rules decide what reaches a year line:

1. A talk marked `†` on the CV is presented by a coauthor and does not appear.
   This is the rule commit `ca3c4b6` established, "list only self-presented
   talks".
2. A talk marked `‡` is an invited talk the user gave himself, and it does
   appear. INFORMS Annual Meeting and AI Lightning Talks are both `‡` and both
   listed.
3. A departmental or program research presentation does not appear, because the
   heading says Conference Presentations. "UMD Smith IS PhD Research
   Presentation" is excluded on this rule while "AI Lightning Talks at UMD
   Smith School", a school-wide event, is included.

Venue short names, extended as new venues arrive:

| CV venue | Site short name |
| --- | --- |
| The 14th ACM Collective Intelligence Conference (CI 2026) | ACM Collective Intelligence |
| AI Lightning Talks at UMD Smith School | AI Lightning Talks at UMD Smith |
| Conference on AI, ML, and Business Analytics (AI/ML) | AI/ML |
| Biz AI Conference at The University of Texas at Dallas (BizAI) | BizAI |
| Conference on Information Systems and Technology (CIST) | CIST |
| Fisher AI in Business Conference | Fisher AI in Business |
| International Conference on Information Systems (ICIS) | ICIS |
| INFORMS Annual Meeting | INFORMS Annual Meeting |
| INFORMS Workshop on Data Science 2025 | INFORMS Workshop on Data Science |
| Workshop on AI and the Future of Collaborative Innovation (WAICI) | WAICI |
| Workshop on Information Systems and Economics (WISE) | WISE |
| Workshop on Information Technologies and Systems (WITS) | WITS |

Academic Service prints one bullet per role, with the journal or conference
name italicized where it is a journal, the acronym in parentheses where the CV
uses one, and the years after ` · `.

The Elsewhere section is hand-written and no CV field feeds it. Leave it alone.

## CV page, `content/cv.md`

The education table is a `<div class="education">` of three-column rows, in the
order Maryland, New York University, Renmin. Note that this order is not the
CV's, which sorts by start date. The page then links and embeds
`/files/CV.pdf`.

Contact details are deliberately absent from this page. Commit `ca3c4b6`
removed them, so a CV contact block change does not come back here.

## Homepage, `hugo.yaml`

Every homepage string lives under `params.profileMode`, because PaperMod's
profile mode ignores the body of `content/_index.md`. The subtitle names the
program, the school, and the two research areas. A CV change reaches this file
only when the Research Interests block or the affiliation changes.

## Decisions carried forward

Each row is a rendering question the user has already answered. Applying the
row is the whole job; asking it again is the failure this section prevents.

| Question | Answer | Settled |
| --- | --- | --- |
| Does the Teaching page print enrollment counts? | No. The CV dropped "(22 students)" from BMGT 302 and the site dropped the sentence with it. Do not reintroduce a headcount for any course. | Aug 2026 |
| The CV dropped "incoming" from the AI Bootcamp audience. Does the site follow? | No. The Teaching page keeps "incoming Smith MBA students". The CV edit is a space trim and not a change of audience. | Aug 2026 |
| Does a work-in-progress paper show its CV sub-status? | Only where the CV names a running data collection. "Large-scale experiment in progress" becomes "Work in progress, large-scale experiment underway"; "Modeling in progress" and "Drafting in progress" both become plain "Work in progress". | Aug 2026 |
