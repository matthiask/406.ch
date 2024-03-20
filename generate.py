# License: WTFPL (DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE), http://www.wtfpl.net/

import re
import shutil
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime as dt
from hashlib import md5
from itertools import chain
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement as SE, tostring as _ts

from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from minify_html import minify
from rcssmin import cssmin


DIR = Path(__file__).parent
URL = "https://406.ch"
TITLE = "Matthias Kestenholz"
c = CodeHiliteExtension(linenums=False, css_class="chl")
md_exts = ["smarty", "footnotes", "admonition", c]
tostring = lambda el: _ts(el, encoding="utf-8", xml_declaration=True).decode("utf-8")


@dataclass(kw_only=True, frozen=True, order=True)
class Category:
    slug: str
    title: str
    url = lambda self: f"/writing/category-{self.slug}/"


@dataclass(kw_only=True, frozen=True, order=True)
class Post:
    date: date
    slug: str
    title: str
    updated: str
    categories: list[Category]
    body: str
    excerpt: str
    draft: str
    url = lambda self: f"/writing/{self.slug}/"


def create_excerpt(body):
    soup = BeautifulSoup(body, "html.parser")
    return " ".join(tag.text for tag in soup.select("h2, h3, p, li"))


def load_posts(dirs):
    slugify = lambda v: re.sub(r"[^a-z0-9]+", "-", v.lower()).strip("-")
    for md in chain.from_iterable(DIR.glob(f"{dir}/*.md") for dir in dirs):
        try:
            props, content = md.read_text().replace("\r", "").split("\n\n", 1)
            props = [re.split(r":\s*", prop, maxsplit=1) for prop in props.split("\n")]
            props = {"categories": ""} | {name.lower(): value for name, value in props}
            props["date"] = dt.strptime(props["date"], "%Y-%m-%d").date()
            props["slug"] = props.get("slug") or slugify(props["title"])
            props["updated"] = f"{props['date'].isoformat()}T12:00:00Z"
            body = markdown(content, extensions=md_exts)
            if "<h1>" not in body:
                body = markdown(f"# {props['title']}", extensions=["smarty"]) + body
            props["excerpt"] = create_excerpt(body)
            c_titles = sorted(c for c in re.split(r",\s*", props["categories"]) if c)
            props["categories"] = [Category(slug=slugify(c), title=c) for c in c_titles]
            yield Post(**{"body": body, "draft": ""} | props)
        except Exception as exc:
            print(f"{md.relative_to(DIR)} invalid, skipping: {exc!r}", file=sys.stderr)


def jinja_templates(context):
    styles = cssmin("".join(f.read_text() for f in sorted(DIR.glob("resources/*.css"))))
    style_file = f"/styles.{md5(styles.encode('utf-8')).hexdigest()[:12]}.css"
    write_file(style_file, styles)

    env = Environment(loader=FileSystemLoader([DIR / "resources"]), autoescape=True)
    env.globals.update({"year": date.today().year, "styles": style_file} | context)
    r = lambda template: lambda **ctx: minify(template.render(**ctx))
    return [r(env.get_template(f"{t}.html")) for t in ["archive", "post", "404"]]


def write_feed_with_posts(path, posts, title, link):
    feed = Element("feed", {"xml:lang": "en", "xmlns": "http://www.w3.org/2005/Atom"})
    SE(feed, "title").text = title
    SE(feed, "link", {"href": f"{URL}{path}atom.xml", "rel": "self"})
    SE(feed, "link", {"href": link, "rel": "alternate"})
    SE(feed, "id").text = link
    SE(feed, "updated").text = posts[0].updated
    SE(SE(feed, "author"), "name").text = TITLE
    for post in posts:
        entry = SE(feed, "entry")
        SE(entry, "title").text = post.title
        link = f"{URL}{post.url()}"
        SE(entry, "link", {"href": link, "rel": "alternate"})
        SE(entry, "id").text = link
        SE(entry, "published").text = SE(entry, "updated").text = post.updated
        SE(entry, "summary", {"type": "html"}).text = post.body
    write_file(f"{path}atom.xml", tostring(feed))
    write_file(f"{path}feed/index.html", tostring(feed))


def write_file(path, content):
    file = DIR / "htdocs" / path[1:]
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(content)
    write_file.count = getattr(write_file, "count", 0) + 1


def main(*, only_published=True):
    posts = sorted(load_posts(["posts"]), reverse=True)
    if only_published:
        posts = [post for post in posts if post.date <= date.today() and not post.draft]
    slugs = Counter(post.slug for post in posts).items()
    if dup := [slug for slug, count in slugs if count > 1]:
        print(f"Duplicated slugs: {', '.join(map(repr, dup))}", file=sys.stderr)
    counter = Counter(chain.from_iterable(post.categories for post in posts))
    print(f"{len(posts)} posts in ", end="")
    print(", ".join(f"{c.title} ({count})" for c, count in sorted(counter.items())))

    shutil.rmtree(DIR / "htdocs", ignore_errors=True)
    shutil.copytree(DIR / "assets", DIR / "htdocs" / "assets", dirs_exist_ok=True)
    archive, detail, not_found = jinja_templates({"categories": sorted(counter)})
    write_file("/writing/index.html", f'<meta content="0;url={URL}"http-equiv=refresh>')
    write_file("/robots.txt", f"User-agent: *\nSitemap: {URL}/sitemap.xml\n")
    write_file("/404.html", not_found())
    write_file("/index.html", archive(posts=posts))
    write_feed_with_posts("/writing/", posts[:20], title=TITLE, link=f"{URL}/")
    urlset = Element("urlset", {"xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"})
    for post in posts:
        write_file(f"{post.url()}index.html", detail(post=post))
        SE(SE(urlset, "url"), "loc").text = f"{URL}{post.url()}"
    for category in sorted(counter):
        category_posts = [post for post in posts if category in post.categories]
        write_file(
            f"{category.url()}index.html",
            archive(posts=category_posts, current=category),
        )
        write_feed_with_posts(
            category.url(),
            category_posts[:20],
            title=f"{TITLE}: Posts about {category.title}",
            link=f"{URL}{category.url()}",
        )
        SE(SE(urlset, "url"), "loc").text = f"{URL}{category.url()}"
    write_file("/sitemap.xml", tostring(urlset))
    shutil.copy("resources/favicon.ico", "htdocs/favicon.ico")
    print(f"Wrote {write_file.count} files.")


if __name__ == "__main__":
    main()
