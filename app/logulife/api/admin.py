from django.contrib import admin

from logulife.api import models


class SourceAdmin(admin.ModelAdmin):

    list_display = ('name', 'owner')
    ordering = ('-name',)


class RecordAdmin(admin.ModelAdmin):

    list_display = ('text', 'timestamp', 'owner', 'source', 'id', 'label', 'label_confirmed')
    ordering = ('-id',)
    readonly_fields = ('id', 'timestamp')


admin.site.register(models.Source, SourceAdmin)
admin.site.register(models.Record, RecordAdmin)
