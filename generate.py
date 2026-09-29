# Licensed under the MIT License -- do whatever you want with it but don't complain to me.

import datetime as dt
import html
import re
import shutil
import sys
import unicodedata
from collections import Counter
from dataclasses import dataclass
from hashlib import md5
from itertools import chain
from pathlib import Path
from urllib.parse import urljoin, urlparse
from xml.etree.ElementTree import Element, SubElement as SE, tostring as _ts

import pyromark
from jinja2 import Environment, FileSystemLoader
from minify_html import minify
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import TextLexer, get_lexer_by_name
from rcssmin import cssmin


DIR = Path(__file__).parent
URL = "https://406.ch"
TITLE = "Matthias Kestenholz"
today = dt.date.today()
opts = pyromark.Options
md_options = opts.ENABLE_FOOTNOTES | opts.ENABLE_SMART_PUNCTUATION | opts.ENABLE_GFM
formatter = HtmlFormatter(cssclass="chl", wrapcode=True)
strip_tags = lambda v: html.unescape(re.sub(r"<[^>]+>", "", v))
CODE_RE = r'<pre><code(?: class="language-([^"]+)")?>(.*?)</code></pre>'
HEADING_RE = r"<h([1-6])>(.*?)</h\1>"
FNREF_RE = r'<sup class="footnote-reference"><a href="#([^"]+)">(\d+)</a></sup>'
FNDEF_RE = (
    r'<div class="footnote-definition" id="([^"]+)"><sup[^>]*>(\d+)</sup>(.*?)</div>\n?'
)


def hilite(m):
    lexer = get_lexer_by_name(m[1]) if m[1] else TextLexer()
    return highlight(html.unescape(m[2]), lexer, formatter).rstrip("\n")


def heading(m, seen):
    text = strip_tags(re.sub(FNREF_RE, "", m[2]))
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    slug = re.sub(r"[-\s]+", "-", re.sub(r"[^\w\s-]", "", text).strip().lower())
    seen[slug] += 1
    slug = f"{slug}_{seen[slug] - 1}" if seen[slug] > 1 else slug
    return (
        f'<h{m[1]} id="{slug}"><a class="toclink" href="#{slug}">{m[2]}</a></h{m[1]}>'
    )


def md(content):
    refs, notes, seen = Counter(), [], Counter()
    fnref = lambda name, i: f"fnref{i if i > 1 else ''}:{name}"

    def reference(m):
        refs[m[1]] += 1
        return f'<sup id="{fnref(m[1], refs[m[1]])}"><a class="footnote-ref" href="#fn:{m[1]}">{m[2]}</a></sup>'

    def note(m):
        back = "".join(
            f'<a class="footnote-backref" href="#{fnref(m[1], i)}" title="Jump back to footnote {m[2]} in the text">&#8617;</a>'
            for i in range(1, refs[m[1]] + 1)
        )
        notes.append(
            f'<li id="fn:{m[1]}">{re.sub("</p>$", f"&#160;{back}</p>", m[3].strip())}</li>'
        )
        return ""

    body = pyromark.html(content, options=md_options)
    for pattern, repl in [
        (CODE_RE, hilite),
        (HEADING_RE, lambda m: heading(m, seen)),
        (FNREF_RE, reference),
        (FNDEF_RE, note),
    ]:
        body = re.sub(pattern, repl, body, flags=re.DOTALL)
    return body + (
        f'<div class="footnote"><hr><ol>{"".join(notes)}</ol></div>' if notes else ""
    )


tostring = lambda el: _ts(el, encoding="utf-8", xml_declaration=True).decode("utf-8")


def absolufy(html_content, base_url=URL):
    def repl(m):
        url = m[3]
        if url and not urlparse(url).scheme and not url.startswith("#"):
            url = urljoin(base_url, url)
        return f'{m[1]}{m[2]}="{url}"'

    return re.sub(r'(<(?:a|img)\s[^>]*?)\b(href|src)="([^"]*)"', repl, html_content)


@dataclass(kw_only=True, frozen=True, order=True)
class Category:
    slug: str
    title: str
    url = lambda self: f"/writing/category-{self.slug}/"


@dataclass(kw_only=True, frozen=True, order=True)
class Post:
    date: dt.date
    slug: str
    title: str
    updated: str
    categories: list[Category]
    body: str
    excerpt: str
    draft: str
    url = lambda self: f"/writing/{self.slug}/"

    @classmethod
    def from_path(cls, path, *, only_published):
        try:
            slugify = lambda v: re.sub(r"[^a-z0-9]+", "-", v.lower()).strip("-")
            props, content = path.read_text().replace("\r", "").split("\n\n", 1)
            props = [re.split(r":\s*", prop, maxsplit=1) for prop in props.split("\n")]
            props = {"categories": ""} | {name.lower(): value for name, value in props}
            if "date" in props:
                props["date"] = dt.datetime.strptime(props["date"], "%Y-%m-%d").date()
            else:
                props["date"] = dt.datetime.strptime(path.name[:8], "%Y%m%d").date()
            if only_published and (props["date"] > today or props.get("draft")):
                return None
            props["slug"] = props.get("slug") or slugify(props["title"])
            props["updated"] = f"{props['date'].isoformat()}T12:00:00Z"
            prose = re.sub(r"^```.*?^```", "", content, flags=re.MULTILINE | re.DOTALL)
            if not re.search(r"^# ", prose, re.MULTILINE):
                content = f"# {props['title']}\n\n{content}"
            body = md(content)
            text = re.sub(
                r'<(h1|pre)\b.*?</\1>|<div class="footnote">.*',
                "",
                body,
                flags=re.DOTALL,
            )
            props["excerpt"] = " ".join(strip_tags(text).split())
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
    env.globals.update({"year": today.year, "styles": style_file} | context)
    r = lambda template: (
        lambda **ctx: minify(absolufy(template.render(**ctx), base_url))
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
    paths = DIR.glob("posts/*.md")
    posts = (Post.from_path(p, only_published=only_published) for p in paths)
    posts = sorted(filter(None, posts), reverse=True)
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
