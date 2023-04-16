import datetime as dt
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown import markdown


BASE_DIR = Path(__file__).resolve(strict=True).parent

env = Environment(
    loader=FileSystemLoader([BASE_DIR / "templates"]),
    autoescape=select_autoescape(
        disabled_extensions=("txt",),
        default_for_string=True,
        default=True,
    ),
)


def markdown_to_html(md):
    return markdown(md, extensions=["smarty", "footnotes", "admonition"])


@dataclass(kw_only=True)
class Post:
    title: str
    slug: str
    is_published: bool
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

    @property
    def get_absolute_url(self):
        return f"/writing/{self.slug}/"


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
        try:
            props, content = md.read_text().split("\n\n", 1)

            properties = {}
            for prop in props.split("\n"):
                name, value = prop.split(":", 1)
                properties[name.lower()] = value.strip()

            posts.append(
                Post(
                    title=properties["title"],
                    slug=properties.get("slug") or slugify(properties["title"]),
                    is_published=properties.get("status") == "published",
                    date=parse_date(properties.get("date", "")),
                    categories=parse_categories(properties.get("categories") or ""),
                    type=properties.get("type") or "markdown",
                    content=content,
                )
            )
        except Exception as exc:
            raise Exception(f"Unable to load {md}") from exc

    return sorted(posts, key=lambda post: post.date or dt.date.min, reverse=True)


if __name__ == "__main__":
    posts = load_posts(BASE_DIR / "posts")

    # from pprint import pprint
    # pprint(posts)
    # print(posts[-1].html)

    template = env.get_template("post_archive.html")
    print(
        template.render(
            object_list=[post for post in posts if post.is_published],
            year=dt.date.today().year,
            blog={},
            request={},
            view={},
        )
    )

    template = env.get_template("post_detail.html")
    print(
        template.render(
            post=posts[0],
            year=dt.date.today().year,
            blog={},
            request={},
            view={},
        )
    )
