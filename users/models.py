from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.translation import ugettext as _

from articles.models import Article


class Follower(models.Model):

    user = models.ForeignKey(User, related_name='follower_origin')
    followed = models.ForeignKey(User, related_name='follower_target')
    create_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user


class Email(models.Model):

    user = models.ForeignKey(User, related_name='user_email')
    email_address = models.CharField(max_length=150)
    subject = models.TextField()
    sent_date = models.DateTimeField(default=timezone.now)
    create_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.email_address


class Profile(models.Model):
    user = models.OneToOneField(User)
    hash = models.TextField()   # To access this property user.profile.hash

    def __unicode__(self):
        return self.user


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user')
    photo = models.ImageField(verbose_name=_("Profile Picture"),
                        upload_to="profile", max_length=255, null=True, blank=True)
    bio = models.TextField(default='', blank=True)

    def create_profile(sender, **kwargs):
        user = kwargs["instance"]
        if kwargs["created"]:
            user_profile = UserProfile(user=user)
            user_profile.save()
    post_save.connect(create_profile, sender=User)