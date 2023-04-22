#!/usr/bin/env python3

import datetime as dt
import re
import sys
from pathlib import Path


def slugify(value):
    return re.sub(r"[^-a-z0-9]+", "-", value.lower()).strip("-")


while True:
    type = input("Create a draft? [Y/n] ").lower()
    if type in {"", "y", "n"}:
        type = "published" if type == "n" else "draft"
        break
while True:
    title = input("Title: ")
    if title:
        break

pubdate = dt.date.today().isoformat()
filename = f"{pubdate}-{slugify(title)}.md"
text = f"""\
Title: {title}
Date: {pubdate}
Categories:

# {title}
"""

path = Path.cwd() / type / filename
if path.exists():
    print(f"Not overwriting {type}/{filename}", file=sys.stderr)
else:
    path.write_text(text)
    print(f"Created {type}/{filename}")
