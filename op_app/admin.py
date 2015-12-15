from django.contrib import admin
from . import models
# To jest tzw. dekorator, mówi on że klasa Admin opisuje interfejs
# admina dla modelu LecturerProfile


@admin.register(models.LecturerProfile)
class Admin(admin.ModelAdmin):
    pass