Title: Embedding videos in feincms3
Slug: embedding-videos-in-feincms3
Date: 2020-09-21
Categories: Django, feincms, Programming
Type: markdown

# Embedding videos in feincms3

I have been using [oEmbed](https://oembed.com/) services for about 10 years now to embed content from YouTube and Vimeo on other sites, first using [feincms-oembed](https://github.com/feincms/feincms-oembed/) and later using [feincms3.plugins.external](https://feincms3.readthedocs.io/en/latest/ref/plugins.html#module-feincms3.plugins.external). This worked well enough despite some problems such as [Embed.ly](https://embed.ly/) introducing API keys and [Noembed](https://noembed.com/) being more or less unmaintained since 2017.

However, the requirement to fetch data from a different service always bothered me, especially since all I wanted (most of the time) was to generate a bare `<iframe>` containing the embed, nothing more.

[django-embed-video](https://github.com/jazzband/django-embed-video/) was almost what I needed but it had some worrysome thumbnail fetching code in there; also I didn't understand the reason for defining backends, dynamically importing them etc. when all I wanted was a function where I would get back some HTML when passing a supported URL, or nothing if the URL wasn't supported.

Since I really like writing code[^nih] here's my solution to embedding YouTube and Vimeo videos as a part of feincms3, [feincms3.embedding](https://github.com/matthiask/feincms3/blob/main/feincms3/embedding.py). Since it doesn't depend on an external service (except the obvious ones) it is [never gonna give you up](https://www.youtube.com/watch?v=dQw4w9WgXcQ) if you just call:

    from feincms3.embedding import embed
    html = embed("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

[^nih]: Maybe it's just a really strong [NIH syndrome](https://en.wikipedia.org/wiki/Not_invented_here). Either way, since most other content providers are sadly/luckily irrelevant for the sites I help create and maintain it should be fine.
