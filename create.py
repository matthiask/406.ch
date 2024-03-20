#!/usr/bin/env python3

import datetime as dt
import re
import sys
from pathlib import Path


def slugify(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


while True:
    title = input("Title: ")
    if title:
        break

pubdate = dt.date.today().isoformat()
filename = f"{pubdate.replace('-', '')}-{slugify(title)}.md"
text = f"""\
Title: {title}
Date: {pubdate}
Categories:
Draft: remove-this-to-publish

# {title}
"""

path = Path.cwd() / "posts" / filename
if path.exists():
    print(f"Not overwriting posts/{filename}", file=sys.stderr)
else:
    path.write_text(text)
    print(f"Created posts/{filename}")
