#!/usr/bin/env python3

import datetime as dt
import re
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve(strict=True).parent


def slugify(value):
    return re.sub(r"[^-a-z0-9]+", "-", value.lower()).strip("-")


type = "published" if len(sys.argv) < 2 else sys.argv[1]
assert type in {"draft", "published"}, "First argument must be 'draft' or 'published'"

if title := input("Title: "):
    pubdate = dt.date.today().isoformat()
    filename = f"{pubdate}-{slugify(title)}.md"
    (BASE_DIR / type / filename).write_text(
        f"""\
Title: {title}
Date: {pubdate}
Categories:

# {title}
"""
    )
    print(f"Created {type}/{filename}")
