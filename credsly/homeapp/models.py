from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    total_posts = models.IntegerField(null=True, blank=True)
    total_friends = models.IntegerField(null=True, blank=True)
    total_likes = models.IntegerField(null=True, blank=True)
    total_comments = models.IntegerField(null=True, blank=True)
    total_credit = models.IntegerField(null=True, blank=True)
    total_followers = models.IntegerField(null=True, blank=True)
    linkedin_zipname = models.CharField(max_length=100, null=True, blank=True)
    facebook_zipname = models.CharField(max_length=100, null=True, blank=True)
    twitter_username = models.CharField(max_length=100, null=True, blank=True)
    credit_score = models.IntegerField(null=True, blank=True)

