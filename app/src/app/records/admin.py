from django.contrib import admin

from .models import Source, Record, Entity


class SourceAdmin(admin.ModelAdmin):

    list_display = ('name', 'owner')
    ordering = ('-name',)


class RecordAdmin(admin.ModelAdmin):

    list_display = (
        'text', 'timestamp', 'owner',
        'source', 'id', 'label',
        'label_confirmed', 'deleted')
    ordering = ('-timestamp',)
    readonly_fields = ('id', 'timestamp')
    exclude = ('label_prediction_results',)


class EntityAdmin(admin.ModelAdmin):

    list_display = ('raw', 'value', 'id', 'record', 'name')
    ordering = ('-id',)


admin.site.register(Source, SourceAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(Entity, EntityAdmin)
