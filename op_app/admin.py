from django.contrib import admin
from . import models


@admin.register(models.LecturerProfile)
class Admin(admin.ModelAdmin):
    list_display = ('name', 'surname')


@admin.register(models.Tags)
class Admin1(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(models.WorkPlace)
class Admin2(admin.ModelAdmin):
    list_display = ('name', 'town')


@admin.register(models.Comment)
class Admin3(admin.ModelAdmin):
    list_display = ('text', 'profile')

