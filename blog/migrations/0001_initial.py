# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="title")),
                ("slug", models.SlugField(max_length=200, verbose_name="slug")),
            ],
            options={
                "ordering": [b"title"],
                "verbose_name": "category",
                "verbose_name_plural": "categories",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="created on"
                    ),
                ),
                (
                    "published_on",
                    models.DateTimeField(
                        null=True, verbose_name="published on", blank=True
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="title")),
                (
                    "slug",
                    models.SlugField(unique=True, max_length=200, verbose_name="slug"),
                ),
                ("content", models.TextField(verbose_name="content", blank=True)),
                (
                    "content_type",
                    models.CharField(
                        default=b"markdown",
                        max_length=20,
                        verbose_name="content type",
                        choices=[(b"markdown", "Markdown"), (b"html", "HTML")],
                    ),
                ),
                ("html", models.TextField(verbose_name="HTML", editable=False)),
                (
                    "author",
                    models.CharField(max_length=200, verbose_name="author", blank=True),
                ),
                (
                    "categories",
                    models.ManyToManyField(
                        to="blog.Category", verbose_name="categories", blank=True
                    ),
                ),
            ],
            options={
                "ordering": [b"-published_on"],
                "get_latest_by": b"published_on",
                "verbose_name": "post",
                "verbose_name_plural": "posts",
            },
            bases=(models.Model,),
        ),
    ]
