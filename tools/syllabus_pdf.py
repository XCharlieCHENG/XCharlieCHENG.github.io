"""Build the public BMGT 302 syllabus-and-schedule PDF for the website.

Reads the course's Markdown sources, never writes to the course folder, and
renders each document the way the course PDFs were rendered: headless Chrome,
A4, the macOS system font. The web copy differs from the course copy in two
ways the instructor chose on 2026-09-27: the teaching assistant rows are
removed, and the bracketed numbers in the extended-absence paragraph lose
their brackets.

Usage, from the site root:
    python3 tools/syllabus_pdf.py \\
        ~/Library/CloudStorage/GoogleDrive-xccheng@umd.edu/My\\ Drive/Teach/BMGT302\\ Fall26 \\
        static/files/BMGT302_Fall2026_Syllabus_and_Schedule.pdf
"""
import os
import re
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import markdown
from pypdf import PdfReader, PdfWriter

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TITLE = "BMGT 302 Essential Programming and AI Skills for Business Analytics"

# Calibrated against the Aug 24 course PDFs: text widths and horizontal
# positions match, and vertical positions agree within 2pt.
CSS = """
@page { size: A4; margin: 50.4pt 97.5pt 50pt 97.5pt; }
html { font-size: 14px; }
body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif;
       line-height: 22px; color: #1f2328; }
h1, h2, h3 { font-weight: 600; line-height: 1.25; margin: 24px 0 16px; }
h1, h2 { padding-bottom: 0.3em; border-bottom: 1px solid #d8dee4; }
h1 { font-size: 2em; }
h2 { font-size: 1.5em; }
h3 { font-size: 1.25em; }
p, ul, ol, table { margin: 0 0 16px; }
ul, ol { padding-left: 40px; }
table { border-collapse: collapse; width: 100%; }
th, td { padding: 5px 10px; text-align: left; vertical-align: middle; border-bottom: 1px solid #d8dee4; }
th { font-weight: 600; border-bottom: 2px solid #1f2328; }
a { color: #0969da; text-decoration: none; }
tr { break-inside: avoid; }
"""


def web_copy(name, text):
    """Apply the web-only edits to one source document."""
    if name.startswith("Syllabus"):
        rows = text.split("\n")
        start = next(i for i, r in enumerate(rows) if r.startswith("| **Teaching Assistant**"))
        end = start + 1
        while end < len(rows) and rows[end].startswith("| **Office Hour"):
            end += 1
        if rows[start - 1].strip() == "| | |":
            start -= 1
        del rows[start:end]
        text = "\n".join(rows)
        text = re.sub(r"\[(\d+)\] (days|sessions)", r"\1 \2", text)
    # Link bare URLs and addresses, as the course PDFs do.
    text = re.sub(r"(?<![<(])(https?://[^\s)|,]+[^\s)|,.])", r"<\1>", text)
    text = re.sub(r"(?<![<\w.])([\w.+-]+@[\w-]+\.[\w.]*\w)", r"<\1>", text)
    return text


def render(md_text, html_path, pdf_path, profile):
    body = markdown.markdown(md_text, extensions=["tables", "sane_lists"])
    html_path.write_text(
        f"<!doctype html><html><head><meta charset='utf-8'><title>{TITLE}</title>"
        f"<style>{CSS}</style></head><body>{body}</body></html>",
        encoding="utf-8",
    )
    # Headless Chrome on this Mac writes the PDF and then does not exit. The
    # script waits for a complete file and closes that Chrome instance itself.
    pdf_path.unlink(missing_ok=True)
    proc = subprocess.Popen(
        [CHROME, "--headless", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
         "--use-mock-keychain", "--disable-sync", "--disable-extensions",
         "--disable-background-networking", "--disable-component-update",
         f"--user-data-dir={profile}", "--no-pdf-header-footer",
         f"--print-to-pdf={pdf_path}", html_path.as_uri()],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True,
    )
    last_size, deadline = -1, time.time() + 90
    while time.time() < deadline:
        size = pdf_path.stat().st_size if pdf_path.exists() else -1
        if size > 0 and size == last_size and pdf_path.read_bytes().rstrip().endswith(b"%%EOF"):
            break
        if proc.poll() is not None and size > 0:
            break
        last_size = size
        time.sleep(1)
    else:
        raise RuntimeError(f"Chrome did not produce {pdf_path}")
    if proc.poll() is None:
        os.killpg(proc.pid, signal.SIGTERM)
        proc.wait(timeout=15)


def main(course_dir, out_pdf):
    course_dir, out_pdf = Path(course_dir), Path(out_pdf)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        parts = []
        for name in ["Syllabus_BMGT302_Fall2026", "Schedule_BMGT302_Fall2026"]:
            text = web_copy(name, (course_dir / f"{name}.md").read_text(encoding="utf-8"))
            pdf = tmp / f"{name}.pdf"
            render(text, tmp / f"{name}.html", pdf, tmp / "chrome-profile")
            parts.append((name.split("_")[0], PdfReader(pdf)))
        writer = PdfWriter()
        for label, reader in parts:
            first = len(writer.pages)
            for page in reader.pages:
                writer.add_page(page)
            writer.add_outline_item(label, first)
        writer.add_metadata({"/Title": "BMGT 302 Fall 2026: Syllabus and Schedule",
                             "/Author": "Xiang (Charlie) Cheng"})
        with open(out_pdf, "wb") as fh:
            writer.write(fh)
    print(f"wrote {out_pdf} ({sum(len(r.pages) for _, r in parts)} pages)")


if __name__ == "__main__":
    main(*sys.argv[1:3])
