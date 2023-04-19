Title: The insides of my static site generator
Date: 2023-04-19
Categories: Django, Programming

# The insides of my static site generator

[Last sunday I wrote that I'm now using a hacky ~200 LOC Python script to
generate this blog.](https://406.ch/writing/static-site-generation/) The ~200
LOC became a challenge to myself immediately and I started refactoring the code
while adding additional features, adding a licensing comment at the top and
further reducing the lines of code in there.

I don't intend to stop working on it, but I'm really happy with the result [as it is currently](https://github.com/matthiask/406.ch/blob/e6402d0927c92c6d426db1dd44de6002940f28b7/generate.py). The script is less than 190 lines long and supports:

- Generating individual HTML files for the front page, the category pages and posts
- Generating `robots.txt` and `sitemap.xml`
- Generating Atom feeds for all posts and posts of each category
- Minifying HTML and CSS using
  [minify-html](https://pypi.org/project/minify-html/) and
  [rcssmin](https://pypi.org/project/rcssmin/); the CSS is outputted as a
  single file and includes the content hash in the filename for better
  cacheability
- Keeping the link structure of the old Django-based website

I used Django's `feedgenerator.py` module at first to generate the Atom feed;
I have since switched to directly working with the [ElementTree
API](https://docs.python.org/3/library/xml.etree.elementtree.html#module-xml.etree.ElementTree).
Yes, it's probably less efficient since it has to keep the whole XML tree in
memory but who cares when the largest file's file size is under 100 KiB at the
time of writing.

I'm using tox to generate the site locally; the local build includes published
and draft posts. The production build uses GitHub actions and automatically
deploys to GitHub pages, while only including published posts. There is no
incremental build right now but rebuilding the whole site using tox (with an
initialized virtualenv) takes less than one second, so that's not really a pain
point for me right now.

A difficulty was that I have used URLs ending in slashes in the past, not just
for the browsable pages but also for the Atom feeds themselves. nginx only
serves `index.html` in folders by default so I couldn't just add a
`index.xml` file in those folders. Luckily enough the internet is made of
lots and lots of duct tape and saving the atom feed as `.../feed/index.html`
actually works. It seems that RSS readers, aggregators and some libraries such
as [feedparser](https://pypi.org/project/feedparser/) do not really need the
correct HTTP headers.

I have licensed the script under the [WTFPL](http://www.wtfpl.net/), so if
you're interested you can do what you want with it, without any obligations. I
would certainly enjoy hearing about it though!
