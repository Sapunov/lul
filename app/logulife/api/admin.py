from django.contrib import admin

from logulife.api import models


admin.site.register(models.Customer)
admin.site.register(models.Source)
admin.site.register(models.Record)
