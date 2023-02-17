# Generated by Django 1.10 on 2016-09-01 14:27

from django.db import migrations
from markdown import markdown


def forwards(apps, schema_editor):
    for post in apps.get_model("blog", "Post").objects.filter(content_type="markdown"):
        post.html = markdown(
            post.content, extensions=["smarty", "footnotes", "admonition"]
        )
        post.save()


class Migration(migrations.Migration):
    dependencies = [("blog", "0002_auto_20160831_1431")]

    operations = [migrations.RunPython(forwards)]
