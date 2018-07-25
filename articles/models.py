from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _


class Category(models.Model):

    name = models.CharField(max_length=30)
    create_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Article(models.Model):

    user = models.ForeignKey(User)
    article_answered = models.ForeignKey("self", blank=True, null=True)
    title = models.CharField(max_length=150)
    media = models.ImageField(verbose_name=_("Imagen"),
                        upload_to="articles", max_length=255, null=True, blank=True)
    introduction = models.CharField(max_length=150)
    text = models.TextField()
    categories = models.ManyToManyField(Category)
    create_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    publication_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


class Favourite(models.Model):

    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)
    create_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.article

    def __str__(self):
        return self.article.title


class Comment(models.Model):

    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)
    text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.text

    def __str__(self):
        return self.text


class Highlight(models.Model):

    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)
    highlight_text = models.TextField()
    start_position = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.underlined_text

    def __str__(self):
        return self.underlined_text


class Mentions(models.Model):

    user = models.ForeignKey(User, related_name='user_metioned')
    article = models.ForeignKey(Article)
    create_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user

    def __str__(self):
        return self.user

