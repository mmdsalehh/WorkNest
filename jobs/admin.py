from django.contrib import admin

from .models import Application, Job

admin.site.register(Job)
admin.site.register(Application)
