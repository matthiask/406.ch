# Licensed under the MIT License -- do whatever you want with it but don't complain to me.

import re
import shutil
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime as dt
from hashlib import md5
from itertools import chain
from pathlib import Path
from urllib.parse import urljoin, urlparse
from xml.etree.ElementTree import Element, SubElement as SE, tostring as _ts

from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
from markdown import markdown
from markdown.extensions import codehilite, toc
from minify_html import minify
from rcssmin import cssmin


DIR = Path(__file__).parent
URL = "https://406.ch"
TITLE = "Matthias Kestenholz"
c = codehilite.CodeHiliteExtension(linenums=False, css_class="chl")
t = toc.TocExtension(anchorlink=True)
md_exts = ["smarty", "footnotes", "admonition", c, t]
tostring = lambda el: _ts(el, encoding="utf-8", xml_declaration=True).decode("utf-8")


def absolufy(html_content, base_url=URL):
    soup = BeautifulSoup(html_content, "html.parser")
    url_attributes = {"a": ["href"], "img": ["src"]}
    for tag_name, attributes in url_attributes.items():
        for tag in soup.find_all(tag_name):
            for attr in attributes:
                if tag.get(attr):
                    url = tag[attr]
                    if url and not urlparse(url).scheme and not url.startswith("#"):
                        absolute_url = urljoin(base_url, url)
                        tag[attr] = absolute_url
    return str(soup)


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

    @classmethod
    def from_path(cls, path):
        try:
            slugify = lambda v: re.sub(r"[^a-z0-9]+", "-", v.lower()).strip("-")
            props, content = path.read_text().replace("\r", "").split("\n\n", 1)
            props = [re.split(r":\s*", prop, maxsplit=1) for prop in props.split("\n")]
            props = {"categories": ""} | {name.lower(): value for name, value in props}
            if "date" in props:
                props["date"] = dt.strptime(props["date"], "%Y-%m-%d").date()
            else:
                props["date"] = dt.strptime(path.name[:8], "%Y%m%d").date()
            props["slug"] = props.get("slug") or slugify(props["title"])
            props["updated"] = f"{props['date'].isoformat()}T12:00:00Z"
            if "\n# " not in content and not content.startswith("# "):
                content = f"# {props['title']}\n\n{content}"
            body = markdown(content, extensions=md_exts)
            soup = BeautifulSoup(body, "html.parser")
            props["excerpt"] = " ".join(
                tag.text for tag in soup.select("h2, h3, p, li")
            )
            c_titles = sorted(c for c in re.split(r",\s*", props["categories"]) if c)
            props["categories"] = [Category(slug=slugify(c), title=c) for c in c_titles]
            return cls(**{"body": body, "draft": ""} | props)
        except Exception as e:
            print(f"{path.relative_to(DIR)} invalid, skipping: {e!r}", file=sys.stderr)


def jinja_templates(context, base_url):
    styles = cssmin("".join(f.read_text() for f in sorted(DIR.glob("resources/*.css"))))
    style_file = f"/styles.{md5(styles.encode('utf-8')).hexdigest()[:12]}.css"
    write_file(style_file, styles)

    env = Environment(loader=FileSystemLoader([DIR / "resources"]), autoescape=True)
    env.globals.update({"year": date.today().year, "styles": style_file} | context)
    r = lambda template: lambda **ctx: minify(
        absolufy(template.render(**ctx), base_url)
    )
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


def main(*, only_published=True, base_url=URL):
    posts = (Post.from_path(p) for p in DIR.glob("posts/*.md"))
    posts = sorted(filter(None, posts), reverse=True)
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
    archive, detail, not_found = jinja_templates(
        {"categories": sorted(counter)}, base_url
    )
    write_file("/writing/index.html", f'<meta content="0;url={URL}"http-equiv=refresh>')
    write_file("/robots.txt", f"User-agent: *\nSitemap: {URL}/sitemap.xml\n")
    write_file("/404.html", not_found())
    write_file("/index.html", archive(posts=posts))
    write_feed_with_posts("/writing/", posts[:20], title=TITLE, link=f"{URL}/")
    urlset = Element("urlset", {"xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"})
    for index, post in enumerate(posts):
        write_file(
            f"{post.url()}index.html", detail(post=post, posts=posts, index=index)
        )
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
