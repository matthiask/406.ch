Title: Static site generation
Date: 2023-04-16
Categories: Django, Programming
Type: markdown

# Static site generation

[I did what I threatened (myself) to do:](https://406.ch/writing/weeknotes-2023-week-10/) I replaced the Django code base for this weblog with a static site generator.

My main goal was to preserve as much as possible of the existing structure, including the Atom feeds and the IDs of posts so that the rewrite wouldn't flood any aggregators.

The end result is a hacky ~200 LOC script which uses Markdown, Jinja2 and rcssmin. Markdown is great for blogging and I have been using it for a long time, basically since I started this website in 2005. I don't like it that much for documentation, but that's a story for another day.

For now I still deploy the blog to a VPS but there's nothing stopping me from uploading it somewhere else. I'm thinking about using GitHub actions for the deployment, but I can do that another day.
