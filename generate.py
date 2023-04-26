# License: WTFPL (DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE)
# See http://www.wtfpl.net/

import re
import shutil
import sys
from dataclasses import dataclass
from datetime import date, datetime, time, timezone
from hashlib import md5
from itertools import chain
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring

from jinja2 import Environment, FileSystemLoader
from markdown import markdown
from minify_html import minify
from rcssmin import cssmin


BASE_DIR = Path(__file__).resolve(strict=True).parent
BASE = "https://406.ch"
TITLE = "Matthias Kestenholz"


@dataclass(kw_only=True)
class Post:
    title: str
    slug: str
    date: date
    updated: datetime
    categories: list[str]
    body: str

    def __lt__(self, other):
        return (self.date, self.slug) < (other.date, other.slug)

    def url(self):
        return f"/writing/{self.slug}/"


@dataclass(kw_only=True)
class Category:
    title: str
    slug: str

    def __hash__(self):
        return hash(self.slug)

    def __lt__(self, other):
        return self.slug < other.slug

    def url(self):
        return f"/writing/category-{self.slug}/"


def slugify(value):
    return re.sub(r"[^-a-z0-9]+", "-", value.lower()).strip("-")


def parse_categories(value):
    return [
        Category(slug=slugify(category), title=category)
        for category in re.split(r",\s*", value)
        if category
    ]


def load_posts(dirs):
    for md in chain.from_iterable(BASE_DIR.glob(f"{dir}/*.md") for dir in dirs):
        try:
            props, content = md.read_text().replace("\r", "").split("\n\n", 1)
            props = [re.split(r":\s*", prop, 1) for prop in props.split("\n")]
            props = {name.lower(): value for name, value in props}
            body = markdown(content, extensions=["smarty", "footnotes", "admonition"])
            if "<h1>" not in body:
                body = markdown(f"# {props['title']}", extensions=["smarty"]) + body
            date = datetime.strptime(props["date"], "%Y-%m-%d").date()
            yield Post(
                title=props["title"],
                slug=props.get("slug") or slugify(props["title"]),
                date=date,
                updated=datetime.combine(date, time(12, 0), tzinfo=timezone.utc),
                categories=parse_categories(props.get("categories") or ""),
                body=body,
            )
        except Exception as exc:
            md = md.relative_to(BASE_DIR)
            print(f"Skipping the invalid '{md}' file: {exc!r}", file=sys.stderr)


def write_file(path, content):
    file = BASE_DIR / "htdocs" / path.lstrip("/")
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(content)
    write_file.cc = getattr(write_file, "cc", 0) + 1


def styles():
    styles = cssmin("".join(file.read_text() for file in BASE_DIR.glob("styles/*.css")))
    style_file = f"/styles.{md5(styles.encode('utf-8')).hexdigest()[:12]}.css"
    write_file(style_file, styles)
    return style_file


def jinja_templates(**kwargs):
    loader = FileSystemLoader([BASE_DIR / "templates"])
    env = Environment(loader=loader, autoescape=True)
    env.globals.update({"year": date.today().year, "styles": styles()} | kwargs)
    r = lambda template: lambda **ctx: minify(template.render(**ctx))  # noqa: E731
    return [r(env.get_template(f"{t}.html")) for t in ["archive", "post", "404"]]


def write_feed_with_posts(path, posts, title, link):
    root = Element("feed", {"xml:lang": "en", "xmlns": "http://www.w3.org/2005/Atom"})
    SubElement(root, "title").text = title
    SubElement(root, "link", {"href": f"{BASE}/{path}atom.xml", "rel": "self"})
    SubElement(root, "link", {"href": link, "rel": "alternate"})
    SubElement(root, "id").text = link
    SubElement(root, "updated").text = posts[0].updated.isoformat()
    SubElement(SubElement(root, "author"), "name").text = TITLE
    for post in posts:
        entry = SubElement(root, "entry")
        SubElement(entry, "title").text = post.title
        link = f"{BASE}{post.url()}"
        SubElement(entry, "link", {"href": link, "rel": "alternate"})
        SubElement(entry, "id").text = link
        SubElement(entry, "published").text = post.updated.isoformat()
        SubElement(entry, "updated").text = post.updated.isoformat()
        SubElement(entry, "summary", {"type": "html"}).text = post.body

    xml = tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")
    write_file(f"{path}atom.xml", xml)
    write_file(f"{path}feed/index.html", xml)


def write_sitemap(posts):
    root = Element("urlset", {"xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"})
    for post in posts:
        SubElement(SubElement(root, "url"), "loc").text = f"{BASE}{post.url()}"
    sitemap = tostring(root, encoding="utf-8", xml_declaration=True)
    write_file("sitemap.xml", sitemap.decode("utf-8"))


if __name__ == "__main__":
    posts = sorted(load_posts(sys.argv[1:]), reverse=True)
    categories = sorted(set(chain.from_iterable(post.categories for post in posts)))
    print(f"{len(posts)} posts in {', '.join(c.title for c in categories)}.")

    shutil.rmtree(BASE_DIR / "htdocs", ignore_errors=True)
    write_file("writing/index.html", f'<meta content="0;url={BASE}"http-equiv=refresh>')
    write_file("robots.txt", f"User-agent: *\nSitemap: {BASE}/sitemap.xml\n")
    write_sitemap(posts)

    archive, detail, not_found = jinja_templates(categories=categories)
    write_file("404.html", not_found())
    write_file("index.html", archive(posts=posts))
    write_feed_with_posts("writing/", posts[:20], title=TITLE, link=f"{BASE}/")
    for post in posts:
        write_file(f"{post.url()}index.html", detail(post=post))

    for category in categories:
        category_posts = [post for post in posts if category in post.categories]
        write_file(
            f"{category.url()}index.html",
            archive(posts=category_posts, current=category),
        )
        write_feed_with_posts(
            category.url().lstrip("/"),
            category_posts[:20],
            title=f"{TITLE}: Posts about {category.title}",
            link=f"{BASE}{category.url()}",
        )
    print(f"Wrote {write_file.cc} files.")
