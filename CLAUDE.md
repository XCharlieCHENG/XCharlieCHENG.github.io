# Personal Website

The Hugo source for charliecheng.cc. GitHub Actions builds and deploys the
site on every push to `main`.

## Commit and push after every change

Commit and push to `main` as soon as a change is complete and verified. Do not
ask first. This is the user's standing instruction for this repository
(2026-09-27), and it overrides the global rule to push only when asked.

Stage files by name and never use `git add -A`. End each commit message with
the `Co-Authored-By` line from the global git conventions. After the push,
confirm that the deploy run succeeds and that the live page shows the change.
