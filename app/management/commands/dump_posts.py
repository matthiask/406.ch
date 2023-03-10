import datetime as dt
from pathlib import Path

from django.core.management.base import BaseCommand

from blog.models import Post


class Command(BaseCommand):
    help = ""

    def add_arguments(self, parser):
        parser.add_argument("target", type=str)

    def handle(self, **options):
        base = Path(options["target"])

        for post in Post.objects.all():
            metadata = [
                ("Title", post.title),
                (
                    "Status",
                    "published" if post.is_active and post.published_on else "draft",
                ),
                (
                    "Date",
                    post.published_on.date().isoformat()
                    if post.published_on
                    else dt.date.today().isoformat(),
                ),
                ("Categories", ", ".join(c.title for c in post.categories.all())),
                ("Slug", post.slug),
            ]

            date = post.published_on or post.created_on
            f = base / f"{date.date().isoformat()}-{post.slug}.md"
            f.write_text(
                "\n\n".join(
                    (
                        "\n".join(f"{key}: {value}" for key, value in metadata),
                        post.content.replace("\r", ""),
                    )
                )
            )
