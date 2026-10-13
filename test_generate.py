import contextlib
import io
import os
import re
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path
from xml.etree.ElementTree import fromstring

import generate as g


ATOM = "{http://www.w3.org/2005/Atom}"
FEED = [
    ("title", ()),
    ("link", ("href", "rel")),
    ("link", ("href", "rel")),
    ("id", ()),
    ("updated", ()),
    ("author", ()),
]
ENTRY = [
    ("title", ()),
    ("link", ("href", "rel")),
    ("id", ()),
    ("published", ()),
    ("updated", ()),
    ("summary", ("type",)),
]


DEPLOYED = "origin/gh-pages"


def git(*args):
    return subprocess.run(
        ["git", *args], cwd=g.DIR, capture_output=True, check=True
    ).stdout


def published_posts(paths):
    return {
        path.name: post
        for path in paths
        if (post := g.Post.from_path(path, only_published=True))
    }


def current_entries(posts):
    # Posts pushed out of the feeds by newer posts still keep their identity
    current = {
        url: (url, url, post.updated, post.updated)
        for post in posts.values()
        if (url := f"{g.URL}{post.url()}")
    }
    for path in (g.DIR / "htdocs" / "writing").glob("**/atom.xml"):
        for entry in fromstring(path.read_bytes()).iter(f"{ATOM}entry"):
            current[identity(entry)[0]] = identity(entry)
    return current


def deployed_source_posts():
    # Posts as they were in the source commit of the deployment, to tell
    # explicit deletions and unpublishing apart from accidental changes
    subject = git("log", "-1", "--format=%s", DEPLOYED).decode()
    if not (source := re.match(r"deploy: ([0-9a-f]{40})", subject)):
        return {}
    try:
        archive = git("archive", source[1], "posts")
    except subprocess.CalledProcessError:
        return {}
    with tempfile.TemporaryDirectory(dir=g.DIR / "htdocs") as tmp:
        with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
            tar.extractall(tmp, filter="data")
        return published_posts(Path(tmp).glob("posts/*.md"))


def identity(entry):
    # Changing any of these makes feed readers show the entry as new again
    return (
        entry.find(f"{ATOM}id").text,
        entry.find(f"{ATOM}link").attrib["href"],
        entry.find(f"{ATOM}published").text,
        entry.find(f"{ATOM}updated").text,
    )


def skeleton(element):
    return [
        (child.tag.removeprefix(ATOM), tuple(sorted(child.attrib))) for child in element
    ]


class GenerateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        stderr = io.StringIO()
        with (
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(stderr),
        ):
            g.main()
        cls.stderr = stderr.getvalue()

    def test_build(self):
        # Invalid posts and duplicated slugs are only reported on stderr
        self.assertEqual(self.stderr, "")
        for path in ["index.html", "404.html", "robots.txt", "sitemap.xml"]:
            self.assertTrue((g.DIR / "htdocs" / path).is_file(), path)

    def test_feeds(self):
        feeds = sorted((g.DIR / "htdocs" / "writing").glob("**/atom.xml"))
        self.assertGreater(len(feeds), 1)
        for path in feeds:
            with self.subTest(feed=str(path.relative_to(g.DIR))):
                content = path.read_text()
                self.assertEqual(
                    content, (path.parent / "feed" / "index.html").read_text()
                )
                feed = fromstring(content.encode())
                self.assertEqual(feed.tag, f"{ATOM}feed")
                self.assertEqual(
                    feed.attrib, {"{http://www.w3.org/XML/1998/namespace}lang": "en"}
                )

                children = skeleton(feed)
                self.assertEqual(children[: len(FEED)], FEED)
                self.assertEqual(
                    [link.attrib["rel"] for link in feed.findall(f"{ATOM}link")],
                    ["self", "alternate"],
                )
                self.assertEqual(
                    feed.find(f"{ATOM}link[@rel='self']").attrib["href"],
                    f"{g.URL}/{path.relative_to(g.DIR / 'htdocs')}",
                )
                self.assertEqual(skeleton(feed.find(f"{ATOM}author")), [("name", ())])

                entries = feed.findall(f"{ATOM}entry")
                self.assertTrue(1 <= len(entries) <= 20)
                self.assertEqual(children[len(FEED) :], [("entry", ())] * len(entries))
                for entry in entries:
                    self.assertEqual(skeleton(entry), ENTRY)
                    self.assertEqual(
                        entry.find(f"{ATOM}summary").attrib["type"], "html"
                    )
                    self.assertTrue(
                        entry.find(f"{ATOM}id").text.startswith(f"{g.URL}/writing/")
                    )

    def test_entry_identities_unchanged(self):
        if os.environ.get("ALLOW_GUID_CHANGES", "false") != "false":
            self.skipTest("ALLOW_GUID_CHANGES is set")
        try:
            paths = git("ls-tree", "-r", "--name-only", DEPLOYED, "writing/").decode()
        except subprocess.CalledProcessError:
            self.skipTest(f"{DEPLOYED} not available")

        posts = published_posts(g.DIR.glob("posts/*.md"))
        current = current_entries(posts)

        deployed_posts = deployed_source_posts()
        sources = {
            f"{g.URL}{post.url()}": name for name, post in deployed_posts.items()
        }
        files = {path.name for path in g.DIR.glob("posts/*.md")}
        added_dates = {
            post.date for name, post in posts.items() if name not in deployed_posts
        }

        def removed_on_purpose(url):
            if not (name := sources.get(url)):
                return False
            if name in files:
                return name not in posts  # Draft or future date again
            # Deleted, and not renamed to a new file with the same date
            return deployed_posts[name].date not in added_dates

        for path in filter(lambda path: path.endswith("/atom.xml"), paths.split()):
            feed = fromstring(git("show", f"{DEPLOYED}:{path}"))
            for deployed in map(identity, feed.iter(f"{ATOM}entry")):
                if current.get(deployed[0]) == deployed or removed_on_purpose(
                    deployed[0]
                ):
                    continue
                with self.subTest(feed=path, entry=deployed[0]):
                    self.fail(
                        f"Deployed feed entry changed or vanished: {deployed} !="
                        f" {current.get(deployed[0])}. Keep the old URL with a `Slug:`"
                        " header (and the date with `Date:`), or set"
                        " ALLOW_GUID_CHANGES=true if this is intentional."
                    )


if __name__ == "__main__":
    unittest.main()
