import datetime as dt
import hashlib
import io
import re
import shutil
import time
from dataclasses import dataclass, field
from functools import total_ordering
from itertools import chain
from pathlib import Path
from typing import Literal
from xml.etree.ElementTree import Element, SubElement, tostring

from jinja2 import Environment, FileSystemLoader
from markdown import markdown
from minify_html import minify

import feedgenerator


_files_written = 0
BASE_DIR = Path(__file__).resolve(strict=True).parent


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
            return markdown(
                self.content, extensions=["smarty", "footnotes", "admonition"]
            )
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
    if value:
        return dt.datetime.strptime(value, "%Y-%m-%d").date()


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
    global _files_written
    _files_written += 1
    file = BASE_DIR / "htdocs" / path.lstrip("/")
    file.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        file.write_bytes(content)
    else:
        file.write_text(content)


def write_minified_file(path, content):
    write_file(path, minify(content))


def styles_url():
    styles = minify(
        "".join(file.read_text() for file in (BASE_DIR / "styles").glob("*.css"))
    )
    style_file = f"styles.{hashlib.md5(styles.encode('utf-8')).hexdigest()}.css"
    write_file(style_file, styles)
    return f"/{style_file}"


def jinja_env(**kwargs):
    env = Environment(
        loader=FileSystemLoader([BASE_DIR / "templates"]),
        autoescape=True,
    )
    env.globals["year"] = dt.date.today().year
    env.globals["styles_url"] = styles_url()
    env.globals.update(kwargs)
    return env


def render_minified(template, **kwargs):
    return minify(template.render(**kwargs))


def feed_with_posts(posts, **kwargs):
    feed = feedgenerator.Atom1Feed(**kwargs)
    for post in posts:
        link = f"https://406.ch{post.url}"
        feed.add_item(
            title=post.title,
            description=post.html,
            link=link,
            pubdate=dt.datetime.combine(post.date, dt.time(12, 0)),
            unique_id=link,
            unique_id_is_permalink=True,
        )
    with io.StringIO() as f:
        feed.write(f, "utf-8")
        return f.getvalue()


if __name__ == "__main__":
    start = time.perf_counter()
    shutil.rmtree(BASE_DIR / "htdocs", ignore_errors=True)
    posts = load_posts(BASE_DIR / "published")
    categories = sorted(set(chain.from_iterable(post.categories for post in posts)))

    env = jinja_env(categories=categories)
    write_file(
        "writing/index.html",
        '<meta http-equiv="refresh" content="0; url=https://406.ch/" />',
    )
    write_file(
        "robots.txt",
        "User-agent: *\nSitemap: https://406.ch/sitemap.xml\n",
    )
    write_file("404.html", env.get_template("404.html").render())

    archive_template = env.get_template("post_archive.html")
    post_template = env.get_template("post_detail.html")

    write_file("index.html", render_minified(archive_template, posts=posts))
    feed = feed_with_posts(
        posts[:20],
        title="Matthias Kestenholz",
        link="https://406.ch/",
        description="",
        language="en",
    )
    write_file("writing/atom.xml", feed)
    write_file("writing/feed/index.html", feed)

    for category in categories:
        category_posts = [post for post in posts if category in post.categories]
        write_file(
            f"{category.url}index.html",
            render_minified(archive_template, posts=category_posts, current=category),
        )
        feed = feed_with_posts(
            category_posts[:20],
            title=f"Matthias Kestenholz: Posts about {category.title}",
            link=f"https://406.ch{category.url}",
            description="",
            language="en",
        )
        write_file(f"{category.url}atom.xml", feed)
        write_file(f"{category.url}feed/index.html", feed)

    root = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for post in posts:
        write_file(f"{post.url}index.html", render_minified(post_template, post=post))
        loc = SubElement(SubElement(root, "url"), "loc")
        loc.text = f"https://406.ch{post.url}"

    write_file("sitemap.xml", tostring(root, encoding="utf-8", xml_declaration=True))
    elapsed = time.perf_counter() - start
    print(f"Wrote {_files_written} files in {elapsed:.2f} seconds.")
