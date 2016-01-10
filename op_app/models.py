from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class LecturerProfile(models.Model):
    name = models.CharField(max_length=100, verbose_name='Imię:')
    surname = models.CharField(max_length=100, verbose_name='Nazwisko:')
    info = models.CharField(max_length=2000, blank=True, verbose_name='Dodatkowe informacje:')
    user_id = models.ForeignKey(User, null=False)
    work_places = models.ManyToManyField("WorkPlace", db_table="LecturerWorkPlace", blank=True)
    tags = models.ManyToManyField("Tags", db_table="LecturerTags", blank=True)

    class Meta:
        db_table = 'LecturerProfile'


class WorkPlace(models.Model):
    name = models.CharField(max_length=200)
    town = models.CharField(max_length=200)

    class Meta:
        db_table = 'WorkPlace'


class Tags(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'Tags'


class Comment(models.Model):
    text = models.CharField(max_length=200)
    knowledge = models.IntegerField()
    teaching = models.IntegerField()
    friendliness = models.IntegerField()
    #profile is an object, not an integer!
    profile = models.ForeignKey("LecturerProfile", null=False)

    class Meta:
        db_table = 'Comment'