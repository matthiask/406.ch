Title: Migrating from FeinCMS to feincms3
Categories: Django, Programming, feincms

[FeinCMS](https://github.com/feincms/feincms) is still actively maintained, but development, bugfixes and new features mostly land on [feincms3](https://github.com/feincms/feincms3) and [django-content-editor](https://github.com/feincms/django-content-editor) these days, not on FeinCMS itself. That's reason enough to eventually move a project over.

Someone [asked on the feincms3 issue tracker](https://github.com/feincms/feincms3/issues/59) whether there's a guide for making that move. There isn't one yet, so I thought I'd expand on my comment in the issue tracker and post it here too in the hope that it's useful to others. The post is based on a gradual migration [we](https://feinheit.ch/) did in a large, long-lived Django project -- a textbook publishing platform with years of content. Unfortunately I can't show more details since it's a commercial, closed source project. During the migration, the platform stayed in production the whole time, aside from the inevitable bug here and there.

The most important insight is that FeinCMS 1 content types and feincms3 plugins are close enough that we could keep using the same underlying database tables. An export/import step isn't required at all.

## The overall shape of the migration

- FeinCMS keeps managing the plugin tables as usual, for now.
- New feincms3 plugin models get added alongside the old ones, with `managed = False` in their `Meta` and `db_table` pointing at the exact table FeinCMS already created. Django doesn't think these are new or different tables, it just uses the ones that already exist.
- The admin gets migrated from `ItemEditor` to `django-content-editor`'s `ContentEditor`. If your project has more than one independent hierarchy (in our case, one per book series instead of a single global page tree) you can migrate them independently instead of having to do it all in one step.
- Rendering moves over from FeinCMS's rendering machinery to feincms3's, again piece by piece: the HTML generation for the frontend, any full text search indexers, anything else that touches the content.

The examples below use `Chapter` and `ChapterPlugin` because that's the hierarchy in this particular project, one tree per book series rather than one global page tree. Most feincms3 projects center on a single `Page` model instead, so read `Page` wherever you see `Chapter`; the rest still applies.

## Getting the migration state right

Here's a concrete proxy model from that migration, simplified. `RichTextContent` is our own abstract mixin, holding nothing but the actual `text` field, shared between the FeinCMS and feincms3 sides of the code base. The same role is played by [`feincms3.plugins.richtext.RichText`](https://github.com/feincms/feincms3/blob/main/feincms3/plugins/richtext.py) if you use feincms3's bundled plugin instead of your own. `ChapterPlugin` in turn only wires up the boilerplate that's specific to being a plugin content type of our `Chapter` model:

    :::python
    class RichTextContent(models.Model):
        text = RichTextField()

        class Meta:
            abstract = True

    class RichText(ChapterPlugin, RichTextContent):
        class Meta:
            db_table = "textbooks_chapter_richtextcontent"
            managed = False  # Proxy for the real model still owned by FeinCMS

The exact table name depends on how FeinCMS auto-generated it for your project (a mix of the app label, the base model and the content type name), so look it up rather than guessing. `./manage.py sqlmigrate` or just inspecting the database will tell you.

For the very last step, once a plugin has been converted and `managed = False` can go away, use Django's [`migrations.SeparateDatabaseAndState`](https://docs.djangoproject.com/en/stable/ref/migration-operations/#separatedatabaseandstate). It lets you change the migration *state* without touching the database at all. That's exactly what you need here since the table already exists and already has the right shape; only Django's idea of what the schema is needs to catch up.

You don't even have to write these migrations by hand. Remove `managed = False`, run `./manage.py makemigrations` as usual, and Django writes out the normal operations it would generate for any new model. The only manual step is moving that generated list of operations into the `state_operations` argument of a single `SeparateDatabaseAndState` operation, redacted and shortened here:

    :::python
    class Migration(migrations.Migration):
        dependencies = [
            ("textbooks", "0096_remove_richtextcontent_managed"),
        ]

        operations = [
            migrations.SeparateDatabaseAndState(
                state_operations=[
                    migrations.CreateModel(
                        name="RichText",
                        fields=[
                            ("id", models.AutoField(primary_key=True, serialize=False)),
                            ("text", models.TextField()),
                            ("chapter", models.ForeignKey(to="textbooks.Chapter", ...)),
                        ],
                        options={"db_table": "textbooks_chapter_richtextcontent"},
                    ),
                ],
                # No database_operations -- the table is already exactly like this.
            ),
        ]

As always, test this on a copy of the database first and make sure you have backups. Hand-editing migrations isn't generally recommended, but it's safe if you know exactly what you're doing. Treat it with the same care as any other schema change.

## The page tree: mptt vs. tree-queries

FeinCMS 1's bundled `Page` model uses [django-mptt](https://github.com/django-mptt/django-mptt) for the page hierarchy, while feincms3's page comes with [django-tree-queries](https://github.com/feincms/django-tree-queries) instead. If you're using FeinCMS's own `Page` model and migrating to feincms3's, this can be a little bit painful since the database schema is different. There's a [dedicated guide for migrating from django-mptt](https://django-tree-queries.readthedocs.io/en/latest/#migrating-from-django-mptt) in the django-tree-queries documentation.

Once the last plugin has switched over, FeinCMS can be dropped from the project entirely, including from the requirements. The models end up exactly where they would have been if you'd started the project with feincms3 in the first place -- and you never had to export or import a single row to get there.
