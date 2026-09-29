# 406.ch

Static blog generator (single-file, no framework). Posts are Markdown in `posts/`,
output goes to `htdocs/` (gitignored, wiped and rewritten on every build).

## Commands

- Build: `uv run python generate.py` — writes `htdocs/` with production URLs (`https://406.ch`).
- Preview: `./watch.sh` — rebuilds on change (drafts and future posts included) and
  serves on http://localhost:8001. Note it overwrites `htdocs/` with localhost URLs.
- No test suite.

## Post format

Filename: `posts/YYYYMMDD-slug.md`. The date prefix sets the publication date.

The file starts with a metadata block, then a blank line, then the Markdown body:

```
Title: Weeknotes (2026 week 37)
Categories: Climate, Django, Programming, Weeknotes
```

- `Title:` is required; the URL slug is derived from it (`/writing/<slugified-title>/`)
  unless an explicit `Slug:` is given.
- `Categories:` is comma-separated. Reuse existing category names — each distinct
  value creates its own archive page and feed.
- Optional: `Date:` (overrides the filename date), `Slug:`, `Draft:` (any value hides
  the post from production builds).
- Don't add an `# H1` — the title is prepended automatically. Body sections use `##`.
  (Some old posts have an explicit H1 that differs from their `Title:`; leave those.)
- Markdown is CommonMark via pyromark (pulldown-cmark), not Python-Markdown:
  - Code blocks are fenced with a language: ` ```python `. Unlabeled blocks are not
    highlighted (no language guessing). No `:::lang` headers.
  - Notes use GFM alerts: `> [!NOTE]` followed by `> ` lines (styled via `.markdown-alert-note`).
  - Footnotes: `[^name]` and `[^name]: text`.
  - Inch marks after digits need `&rdquo;` (`27&rdquo;`); a plain `"` becomes an opening quote.
- Parse errors are printed and the post is silently skipped, so check the build output.

## Writing conventions

- Write plain ASCII punctuation: smart punctuation turns `"` and `'` into curly
  quotes and `--` into an en dash (`--` is the dash style used throughout the site).
- `30°C` — no space before the degree sign.
- Weeknotes: prose sections first, then a `## Releases` section with one `###` per
  package, each linking to the PyPI project page (not the version-specific URL).
- Internal links are root-relative: `/writing/<slug>/`, optionally with a `#anchor`
  (heading anchors are auto-generated slugs of the heading text).
