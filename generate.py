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
from xml.etree.ElementTree import Element, SubElement, tostring

from jinja2 import Environment, FileSystemLoader
from markdown import markdown
from minify_html import minify

import feedgenerator


_files_written = 0
BASE_DIR = Path(__file__).resolve(strict=True).parent
BASE = "https://406.ch"


@dataclass(kw_only=True)
class Post:
    title: str
    slug: str
    date: dt.date | None = None
    categories: list[str] = field(default_factory=list)
    content: str

    @property
    def html(self):
        if all(not line.startswith("# ") for line in self.content.splitlines()):
            self.content = f"# {self.title}\n\n{self.content}"
        return markdown(self.content, extensions=["smarty", "footnotes", "admonition"])

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
    file.write_text(content)


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


def write_feed_with_posts(path, posts, **kwargs):
    feed = feedgenerator.Atom1Feed(**kwargs)
    for post in posts:
        link = f"{BASE}{post.url}"
        feed.add_item(
            title=post.title,
            description=post.html,
            link=link,
            pubdate=dt.datetime.combine(post.date, dt.time(12, 0)),
            unique_id=link,
        )
    with io.StringIO() as f:
        feed.write(f, "utf-8")
        write_file(f"{path}atom.xml", f.getvalue())
        write_file(f"{path}feed/index.html", f.getvalue())


def write_sitemap(posts):
    root = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for post in posts:
        loc = SubElement(SubElement(root, "url"), "loc")
        loc.text = f"{BASE}{post.url}"
    sitemap = tostring(root, encoding="utf-8", xml_declaration=True)
    write_file("sitemap.xml", sitemap.decode("utf-8"))


if __name__ == "__main__":
    start = time.perf_counter()
    shutil.rmtree(BASE_DIR / "htdocs", ignore_errors=True)
    posts = load_posts(BASE_DIR / "published")
    categories = sorted(set(chain.from_iterable(post.categories for post in posts)))

    env = jinja_env(categories=categories)
    write_file(
        "writing/index.html",
        f'<meta http-equiv="refresh" content="0; url={BASE}/">',
    )
    write_file("robots.txt", f"User-agent: *\nSitemap: {BASE}/sitemap.xml\n")
    write_sitemap(posts)
    write_file("404.html", render_minified(env.get_template("404.html")))

    archive_template = env.get_template("post_archive.html")
    post_template = env.get_template("post_detail.html")

    write_file("index.html", render_minified(archive_template, posts=posts))
    write_feed_with_posts(
        "writing/",
        posts[:20],
        title="Matthias Kestenholz",
        link=f"{BASE}/",
        description="",
        language="en",
    )

    for category in categories:
        category_posts = [post for post in posts if category in post.categories]
        write_file(
            f"{category.url}index.html",
            render_minified(archive_template, posts=category_posts, current=category),
        )
        write_feed_with_posts(
            category.url,
            category_posts[:20],
            title=f"Matthias Kestenholz: Posts about {category.title}",
            link=f"{BASE}{category.url}",
            description="",
            language="en",
        )

    for post in posts:
        write_file(f"{post.url}index.html", render_minified(post_template, post=post))

    elapsed = time.perf_counter() - start
    print(f"Wrote {_files_written} files in {elapsed:.2f} seconds.")