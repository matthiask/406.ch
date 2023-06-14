# License: WTFPL (DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE)
# See http://www.wtfpl.net/

import re
import shutil
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from hashlib import md5
from itertools import chain
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring

from jinja2 import Environment, FileSystemLoader
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from minify_html import minify
from rcssmin import cssmin


DIR = Path(__file__).resolve(strict=True).parent
URL = "https://406.ch"
TITLE = "Matthias Kestenholz"
mext = ["smarty", "footnotes", "admonition", CodeHiliteExtension(linenums=False)]


@dataclass(kw_only=True, frozen=True, order=True)
class Post:
    date: date
    slug: str
    title: str
    updated: str
    categories: list[str]
    body: str

    def url(self):
        return f"/writing/{self.slug}/"


@dataclass(kw_only=True, frozen=True, order=True)
class Category:
    slug: str
    title: str

    def url(self):
        return f"/writing/category-{self.slug}/"


def load_posts(dirs):
    slugify = lambda v: re.sub(r"[^-a-z0-9]+", "-", v.lower()).strip("-")
    for md in chain.from_iterable(DIR.glob(f"{dir}/*.md") for dir in dirs):
        try:
            props, content = md.read_text().replace("\r", "").split("\n\n", 1)
            props = [re.split(r":\s*", prop, 1) for prop in props.split("\n")]
            props = {name.lower(): value for name, value in props}
            body = markdown(content, extensions=mext)
            if "<h1>" not in body:
                body = markdown(f"# {props['title']}", extensions=["smarty"]) + body
            date = datetime.strptime(props["date"], "%Y-%m-%d").date()
            yield Post(
                date=date,
                slug=props.get("slug") or slugify(props["title"]),
                title=props["title"],
                updated=f"{date.isoformat()}T12:00:00Z",
                categories=[
                    Category(slug=slugify(category), title=category)
                    for category in re.split(r",\s*", props.get("categories", ""))
                    if category
                ],
                body=body,
            )
        except Exception as exc:
            md = md.relative_to(DIR)
            print(f"Skipping the invalid '{md}' file: {exc!r}", file=sys.stderr)


def write_file(path, content):
    file = DIR / "htdocs" / path.lstrip("/")
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(content)
    write_file.count = getattr(write_file, "count", 0) + 1


def styles():
    styles = cssmin("".join(f.read_text() for f in sorted(DIR.glob("styles/*.css"))))
    style_file = f"/styles.{md5(styles.encode('utf-8')).hexdigest()[:12]}.css"
    write_file(style_file, styles)
    return style_file


def jinja_templates(**kwargs):
    env = Environment(loader=FileSystemLoader([DIR / "templates"]), autoescape=True)
    env.globals.update({"year": date.today().year, "styles": styles()} | kwargs)
    r = lambda template: lambda **ctx: minify(template.render(**ctx))
    return [r(env.get_template(f"{t}.html")) for t in ["archive", "post", "404"]]


def write_feed_with_posts(path, posts, title, link):
    root = Element("feed", {"xml:lang": "en", "xmlns": "http://www.w3.org/2005/Atom"})
    SubElement(root, "title").text = title
    SubElement(root, "link", {"href": f"{URL}/{path}atom.xml", "rel": "self"})
    SubElement(root, "link", {"href": link, "rel": "alternate"})
    SubElement(root, "id").text = link
    SubElement(root, "updated").text = posts[0].updated
    SubElement(SubElement(root, "author"), "name").text = TITLE
    for post in posts:
        entry = SubElement(root, "entry")
        SubElement(entry, "title").text = post.title
        link = f"{URL}{post.url()}"
        SubElement(entry, "link", {"href": link, "rel": "alternate"})
        SubElement(entry, "id").text = link
        SubElement(entry, "published").text = post.updated
        SubElement(entry, "updated").text = post.updated
        SubElement(entry, "summary", {"type": "html"}).text = post.body

    xml = tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")
    write_file(f"{path}atom.xml", xml)
    write_file(f"{path}feed/index.html", xml)


def write_sitemap(posts):
    root = Element("urlset", {"xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"})
    for post in posts:
        SubElement(SubElement(root, "url"), "loc").text = f"{URL}{post.url()}"
    xml = tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")
    write_file("sitemap.xml", xml)


def main(folders, *, future=False):
    posts = sorted(load_posts(folders), reverse=True)
    if not future:
        posts = [post for post in posts if post.date <= date.today()]
    counter = Counter(chain.from_iterable(post.categories for post in posts))
    categories = sorted(counter)
    print(f"{len(posts)} posts in ", end="")
    print(", ".join(f"{c.title} ({count})" for c, count in sorted(counter.items())))

    shutil.rmtree(DIR / "htdocs", ignore_errors=True)
    write_file("writing/index.html", f'<meta content="0;url={URL}"http-equiv=refresh>')
    write_file("robots.txt", f"User-agent: *\nSitemap: {URL}/sitemap.xml\n")
    write_sitemap(posts)

    archive, detail, not_found = jinja_templates(categories=categories)
    write_file("404.html", not_found())
    write_file("index.html", archive(posts=posts))
    write_feed_with_posts("writing/", posts[:20], title=TITLE, link=f"{URL}/")
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
            link=f"{URL}{category.url()}",
        )
    print(f"Wrote {write_file.count} files.")


if __name__ == "__main__":
    main(["posts"])
