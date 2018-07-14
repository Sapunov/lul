from django.contrib import admin

from .models import Transaction, Category


class TransactionAdmin(admin.ModelAdmin):

    list_display = (
        'id', 'amount_int', 'amount_decimal', 'currency',
        'direction', 'category',  'owner', 'timestamp', 'category_confirmed', 'record')
    ordering = ('-timestamp',)


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Category)
