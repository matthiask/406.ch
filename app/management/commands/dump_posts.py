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
                ("Tags", ", ".join(c.title for c in post.categories.all())),
                ("Slug", post.slug),
            ]

            f = base / f"{post.slug}.md"
            f.write_text(
                "\n\n".join(
                    (
                        "\n".join(f"{key}: {value}" for key, value in metadata),
                        post.content,
                    )
                )
            )
