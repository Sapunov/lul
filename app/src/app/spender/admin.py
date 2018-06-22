from django.contrib import admin

from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):

    list_display = (
        'id', 'amount_int', 'amount_decimal', 'currency',
        'direction', 'category', 'category_confirmed', 'record')
    ordering = ('-id',)


admin.site.register(Transaction, TransactionAdmin)
