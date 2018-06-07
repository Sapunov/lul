from django.contrib import admin

from logulife.api import models


class SourceAdmin(admin.ModelAdmin):

    list_display = ('name', 'owner')
    ordering = ('-name',)


class RecordAdmin(admin.ModelAdmin):

    list_display = (
        'text', 'timestamp', 'owner',
        'source', 'id', 'label',
        'label_confirmed', 'prediction_confidence')
    ordering = ('-id',)
    readonly_fields = ('id', 'timestamp')
    exclude = ('label_prediction_results',)


class EntityAdmin(admin.ModelAdmin):

    list_display = ('raw', 'id', 'record', 'name')
    ordering = ('-id',)


admin.site.register(models.Source, SourceAdmin)
admin.site.register(models.Record, RecordAdmin)
admin.site.register(models.Entity, EntityAdmin)
