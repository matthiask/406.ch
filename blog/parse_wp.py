import codecs
from datetime import datetime
from lxml import etree

from django.template.defaultfilters import slugify

from .models import Category, Post


def import_from_xml(filename):
    ns_wp = etree.FunctionNamespace('http://wordpress.org/export/1.2/')
    ns_wp.prefix = 'wp'

    xml = etree.fromstring(codecs.open(filename).read())

    authors = {}
    for author in xml.xpath('//wp:author'):
        key = value = ''
        for child in author:
            if child.tag == '{http://wordpress.org/export/1.2/}author_login':
                key = child.text
            elif child.tag == '{http://wordpress.org/export/1.2/}author_display_name':
                value = child.text

            if key and value:
                authors[key] = value

    categories = {}

    Post.objects.all().delete()
    Category.objects.all().delete()

    for item in xml.xpath('//item'):
        post = Post()
        _categories = []

        for child in item:
            if child.tag == 'title':
                post.title = child.text
            elif child.tag == '{http://purl.org/dc/elements/1.1/}creator':
                post.author = authors.get(child.text, child.text)
            elif child.tag == '{http://purl.org/rss/1.0/modules/content/}encoded':
                post.content = child.text
            elif child.tag == '{http://wordpress.org/export/1.2/}post_date':
                post.published_on = post.created_on = datetime.strptime(
                    child.text, '%Y-%m-%d %H:%M:%S')
            elif child.tag == '{http://wordpress.org/export/1.2/}post_name':
                post.slug = child.text
            elif child.tag == '{http://wordpress.org/export/1.2/}status':
                if child.text != 'publish':
                    post.published_on = None
            elif child.tag == 'category':
                slug = child.attrib['nicename']
                title = child.text

                _categories.append(slug)

                if slug not in categories:
                    categories[slug] = Category.objects.create(
                        title=title,
                        slug=slug,
                        )

            else:
                print child.tag

        if not post.slug:
            post.slug = slugify(post.title)
        post.save()
        post.categories.add(*[categories[c] for c in _categories])
