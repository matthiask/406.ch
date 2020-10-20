from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from markdown2 import markdown


def markdown_to_soup(md):
    html = markdown(
        md,
        extras=("smarty-pants", "nofollow", "target-blank-links", "footnotes"),
    )
    # Remove entities etc.
    return BeautifulSoup(html)


class Category(models.Model):
    title = models.CharField(_("title"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=200, unique=True)
    content = models.TextField(_("content"), blank=True)
    html = models.TextField(_("HTML"), editable=False)

    class Meta:
        ordering = ["title"]
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog_category_detail", kwargs={"slug": self.slug})

    def clean(self):
        self.html = str(markdown_to_soup(self.content))


class PostQuerySet(models.QuerySet):
    def search(self, query):
        q = Q()
        for term in query.split():
            q &= Q(title__icontains=term) | Q(content__icontains=term)

        return self.filter(q)

    def published(self):
        return self.filter(
            published_on__isnull=False,
            published_on__lte=timezone.now(),
            is_active=True,
        )

    def current(self):
        return self.published().filter(published_on__year__gte=2014)

    def archive(self):
        return self.published().filter(published_on__year__lt=2014)


class Post(models.Model):
    CONTENT_TYPE_CHOICES = (("markdown", _("Markdown")), ("html", _("HTML")))

    is_active = models.BooleanField(_("is active"), default=False)
    is_microblog = models.BooleanField(_("is microblog"), default=False)
    created_on = models.DateTimeField(_("created on"), default=timezone.now)
    published_on = models.DateTimeField(_("published on"), blank=True, null=True)

    title = models.CharField(_("title"), max_length=200, blank=True)
    slug = models.SlugField(_("slug"), max_length=200, unique=True, default="new")
    content = models.TextField(_("content"), blank=True)
    content_type = models.CharField(
        _("content type"),
        max_length=20,
        choices=CONTENT_TYPE_CHOICES,
        default=CONTENT_TYPE_CHOICES[0][0],
    )
    html = models.TextField(_("HTML"), editable=False)
    author = models.CharField(_("author"), max_length=200, blank=True)
    categories = models.ManyToManyField(
        Category, related_name="posts", verbose_name=_("categories"), blank=True
    )

    objects = PostQuerySet.as_manager()

    class Meta:
        get_latest_by = "published_on"
        ordering = ["-published_on"]
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog_post_detail", kwargs={"slug": self.slug})

    def clean(self):
        if self.content_type == "markdown":
            soup = markdown_to_soup(self.content)
            self.html = str(soup)
        else:
            self.html = self.content
            soup = BeautifulSoup(self.html)

        if self.is_microblog:
            self.title = self.html[:200]
        else:
            try:
                self.title = soup.find("h1").text
            except Exception:
                raise ValidationError("Please provide at least one H1 tag.")

        if self.slug in {"", "new"} or not self.is_active:
            self.slug = slugify(self.title)
        if self.is_active and not self.published_on:
            self.published_on = timezone.now()
