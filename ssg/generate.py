import datetime as dt
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from markdown import markdown


BASE_DIR = Path(__file__).resolve(strict=True).parent


def markdown_to_html(md):
    return markdown(md, extensions=["smarty", "footnotes", "admonition"])


@dataclass(kw_only=True)
class Post:
    title: str
    slug: str
    status: Literal["published", "draft"] = "draft"
    date: dt.date | None = None
    categories: list[str] = field(default_factory=list)
    type: Literal["markdown", "html"] = "markdown"
    content: str

    @property
    def html(self):
        if self.type == "html":
            return self.content
        elif self.type == "markdown":
            return markdown_to_html(self.content)
        raise Exception(f"Unknown content type {self.type}")


def slugify(value):
    return re.sub(r"[^-a-z0-9]+", "-", value.lower())


def parse_date(value):
    try:
        return dt.datetime.strptime(value, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def parse_categories(value):
    return {slugify(category): category for category in value.split(", ")}


def load_posts(path):
    posts = []
    for md in path.glob("*.md"):
        props, content = md.read_text().split("\n\n", 1)

        properties = {}
        for prop in props.split("\n"):
            name, value = prop.split(": ", 1)
            properties[name.lower()] = value

        posts.append(
            Post(
                title=properties["title"],
                slug=properties.get("slug") or slugify(properties["title"]),
                status=properties.get("status") or "draft",
                date=parse_date(properties.get("date", "")),
                categories=parse_categories(properties.get("categories") or ""),
                type=properties.get("type") or "markdown",
                content=content,
            )
        )

    return sorted(posts, key=lambda post: post.date or dt.date.min)


if __name__ == "__main__":
    posts = load_posts(BASE_DIR / "posts")
    from pprint import pprint

    pprint(posts)

    print(posts[-1].html)
