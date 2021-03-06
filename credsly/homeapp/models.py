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

class PriorityScores(models.Model):
    priority_one_weight = models.IntegerField(default=100, blank=False)
    priority_two_weight = models.IntegerField(default=80, blank=False)  
    priority_three_weight = models.IntegerField(default=50, blank=False)     

    def save(self):
        # count will have all of the objects from the PriorityScores model
        count = PriorityScores.objects.all().count()
        # this will check if the variable exist so we can update the existing ones
        save_permission = PriorityScores.has_add_permission(self)

        # if there's more than two objects it will not save them in the database
        if count < 1:
            super(PriorityScores, self).save()
        elif save_permission:
            super(PriorityScores, self).save()

    def has_add_permission(self):
        return PriorityScores.objects.filter(id=self.id).exists()
