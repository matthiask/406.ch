Title: django-tree-queries
Slug: django-tree-queries
Date: 2020-09-15
Categories: Django, Programming
Type: markdown

# django-tree-queries

The reason for this blog post is the recent release of [django-tree-queries 0.4](https://django-tree-queries.readthedocs.io/). django-tree-queries allows using an SQL database to retrieve tree nodes in [depth-first search (DFS)](https://en.wikipedia.org/wiki/Depth-first_search) order.

## Other libraries

Many Django libraries exist already for managing and retrieving tree-shaped data. A list of them follows along with reasons why none of them are being used in [feincms3](https://feincms3.readthedocs.io/).

### [django-mptt](https://django-mptt.readthedocs.io/)

I still am a heavy user of django-mptt. FeinCMS 1.x uses it and we therefore use django-mptt as well for many sites which are actively maintained. I also am a co-maintainer of django-mptt so the following critique should be understood with this fact in mind.

django-mptt uses the [nested set model](https://en.wikipedia.org/wiki/Nested_set_model) with an additional `level` and `tree_id` field; the latter partitions nodes into individual, unconnected trees. This is a useful performance optimization. In principle, the nested set model doesn't even require a parent foreign key for nodes; however, django-mptt always adds this field as well.

django-mptt is very dependent on having up-to-date values of the `left`, `right` and `parent_id` values. Fetching ancestors or descendants does not work when those values are outdated. Calling `.save()` with outdated values _absolutely will_ cause corrupted trees -- that is, the MPTT attributes get out of sync. A band-aid fix may be to call `.refresh_from_db()` before each write; but even then I suspect there is a potential for corruption with concurrent writes which are probably only completely avoidable by using a database isolation level of `SERIALIZABLE`.

We had recurring problems with django-mptt even on medium sites without many editors so these problems aren't just theoretical[^djcms].

[^djcms]: [django CMS](https://www.django-cms.org/) was a heavy user of django-mptt until 2015, when they switched to django-treebeard because of the problems mentioned.

### [django-treebeard](https://django-treebeard.readthedocs.io/)

django-treebeard offers three implementations: Nested sets, materialized paths and adjacency lists.

I didn't really want to use more nested sets. The materialized path implementation would probably have been worth a try. The adjacency list implementation does not use recursive CTEs and therefore has to recursively execute one query per parent. This is obviously inefficient and therefore not viable.

I'm not 100% sure anymore but I think I had some doubts regarding the maintainability of django-treebeard. I do like to help out generally, but treebeard still seems to suffer from scope creep a bit.

### ltree, closure trees, oh my...

I also looked at libraries using the [ltree PostgreSQL extension](https://www.postgresql.org/docs/current/ltree.html), and at closure trees and so on. Those solutions didn't seem obviously better to me, at the time.

### [django-cte-trees](https://django-cte-trees.readthedocs.io/) / [django-cte-forest](https://django-cte-forest.readthedocs.io/)

Researching alternative solutions lead me to the [django-cte-trees](https://django-cte-trees.readthedocs.io/) project which uses the adjacency list model and therefore avoids redundant data in the database -- a thing which elegantly avoids even the possibility of data getting out of sync. Databases are able to build the tree structure with hundreds of nodes themselves and still execute SQL queries within milliseconds.

django-cte-forest was my attempt to modernize the codebase of the unmaintained project. This worked well enough. However, for some use cases I really wanted to avoid the common table expression. A better way to achieve this would have been an opt-in instead of an opt-out API for the CTE part. This proofed hard to implement. Also, django-cte-trees supported many many features that I didn't even begin to use.

## The constraints of django-tree-queries

This research lead me to write my own solution. The goals were as follows[^goals]:

[^goals]: That's probably colored by hindsight and wasn't completely worked out at the time.

- Depth-first search only.
- No customizations of deletions etc, let Django's `on_delete` mechanism handle everything.
- It's fine if primary keys must be integers (and not UUIDs etc.)
- As little customization as possible.
- No redundant data in the database. A nullable parent foreign key and optionally a position field to give ordering to siblings.
- PostgreSQL-only is fine.
- Tree querying shouldn't be active by default.

Recursive common table expressions (CTE) might just be fast enough. As long as you guarantee that the database only contains trees things will never get out of sync or break. The only data corruption which is possible is when a node contains itself in its ancestry. Right now, django-tree-queries doesn't handle this case because it may come with an (additional) performance penalty and because I think model validation is sufficient for avoiding these types of accidents.

## The value of small API surfaces

The initial version of django-tree-queries only supported PostgreSQL, but because of its small API surface it didn't take a lot of work to add support for other databases. In the end only two changes were necessary:

- MySQL/MariaDB and sqlite3 do not have a native array type. I therefore decided on concatenating padded strings in the database and splitting the string back into its parts in Python again.
- I had to write slightly different SQL for each database.

This worked out quite well and immediately made [feincms3](https://feincms3.readthedocs.io/) compatible with a broader range of databases.

## The state of things now

[SLOCCount](https://dwheeler.com/sloccount/) counts 280 lines of code (only the `tree_queries` folder containing the library itself, without tests or `setup.py` files) for a library supporting Django 1.8 or better, Python 2.7 or better, and recursive CTEs on PostgreSQL, sqlite3, MariaDB and MySQL.

The first few months of development from summer to the fall of 2018 almost no changes were necessary to the core implementation. The code stayed basically unchanged since before the release of Django 2.2 LTS until last week[^change], following my aim of writing [low maintenance software](https://406.ch/writing/low-maintenance-software/).

[^change]: The only recent change improves performance on PostgreSQL by going back to using integers directly instead of casting them to `::text` if it isn't necessary.
