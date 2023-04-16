import datetime as dt
import hashlib
import io
import re
import shutil
from dataclasses import dataclass, field
from functools import total_ordering
from itertools import chain
from pathlib import Path
from typing import Literal

import feedgenerator
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown import markdown
from rcssmin import cssmin


BASE_DIR = Path(__file__).resolve(strict=True).parent


def markdown_to_html(md):
    return markdown(md, extensions=["smarty", "footnotes", "admonition"])


@dataclass(kw_only=True)
class Post:
    title: str
    slug: str
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
    def url(self):
        return f"/writing/{self.slug}/"


@total_ordering
@dataclass(kw_only=True)
class Category:
    title: str
    slug: str

    def __hash__(self):
        return hash(self.title)

    def __lt__(self, other):
        return self.title < other.title

    @property
    def url(self):
        return f"/writing/category-{self.slug}/"

    @property
    def feed_url(self):
        return f"/writing/category-{self.slug}/atom.xml"


def slugify(value):
    return re.sub(r"[^-a-z0-9]+", "-", value.lower())


def parse_date(value):
    try:
        return dt.datetime.strptime(value, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def parse_categories(value):
    return sorted(
        Category(slug=slugify(category), title=category)
        for category in (v.strip() for v in value.split(","))
        if category
    )


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
                    date=parse_date(properties.get("date", "")),
                    categories=parse_categories(properties.get("categories") or ""),
                    type=properties.get("type") or "markdown",
                    content=content,
                )
            )
        except Exception as exc:
            raise Exception(f"Unable to load {md}") from exc

    return sorted(posts, key=lambda post: post.date or dt.date.min, reverse=True)


def write_file(path, content):
    file = BASE_DIR / "out" / path
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(content)


if __name__ == "__main__":
    shutil.rmtree(BASE_DIR / "out", ignore_errors=True)
    posts = load_posts(BASE_DIR / "posts" / "published")
    categories = sorted(set(chain.from_iterable(post.categories for post in posts)))

    styles = cssmin(
        "".join(file.read_text() for file in (BASE_DIR / "styles").glob("*.css"))
    )
    style_file = f"styles.{hashlib.md5(styles.encode('utf-8')).hexdigest()}.css"
    write_file(style_file, styles)

    # from pprint import pprint
    # pprint(posts)
    # print(posts[-1].html)

    write_file(
        "writing/index.html",
        '<meta http-equiv="refresh" content="0; url=https://406.ch/" />',
    )

    env = Environment(
        loader=FileSystemLoader([BASE_DIR / "templates"]),
        autoescape=select_autoescape(
            disabled_extensions=("txt",),
            default_for_string=True,
            default=True,
        ),
    )
    env.globals["year"] = dt.date.today().year
    env.globals["categories"] = categories
    env.globals["style_url"] = f"/{style_file}"

    template = env.get_template("post_archive.html")
    write_file(
        "index.html",
        template.render(object_list=posts),
    )
    feed = feedgenerator.Atom1Feed(
        title="Matthias Kestenholz",
        link="https://406.ch/writing/feed/",
        description="",
        language="en",
    )
    for post in posts[:20]:
        link = f"https://406.ch/writing/{post.slug}/"
        feed.add_item(
            title=post.title,
            description=post.html,
            link=link,
            unique_id=link,
            unique_id_is_permalink=True,
        )
        with io.StringIO() as f:
            feed.write(f, "utf-8")
            write_file("writing/atom.xml", f.getvalue())
            write_file("writing/feed/index.html", f.getvalue())

    for category in categories:
        category_posts = [post for post in posts if category in post.categories]
        write_file(
            f"writing/category-{category.slug}/index.html",
            template.render(
                object_list=category_posts,
                current=category,
            ),
        )
        feed = feedgenerator.Atom1Feed(
            title=f"Matthias Kestenholz: Posts about {category.title}",
            link=f"https://406.ch{category.url}",
            description="",
            language="en",
        )
        for post in category_posts[:20]:
            link = f"https://406.ch/writing/{post.slug}/"
            feed.add_item(
                title=post.title,
                description=post.html,
                link=link,
                unique_id=link,
                unique_id_is_permalink=True,
            )
            with io.StringIO() as f:
                feed.write(f, "utf-8")
                write_file(f"writing/category-{category.slug}/atom.xml", f.getvalue())
                write_file(
                    f"writing/category-{category.slug}/feed/index.html", f.getvalue()
                )

    template = env.get_template("post_detail.html")
    for post in posts:
        write_file(
            f"writing/{post.slug}/index.html",
            template.render(
                post=posts[0],
            ),
        )
