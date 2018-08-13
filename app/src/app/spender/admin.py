from django.contrib import admin

from .models import Transaction, Category, ExchangeRate


class TransactionAdmin(admin.ModelAdmin):

    list_display = (
        'id', 'amount_int', 'amount_decimal', 'currency',
        'direction', 'category',  'owner', 'timestamp', 'category_confirmed', 'record')
    ordering = ('-timestamp',)


class ExchangeRateAdmin(admin.ModelAdmin):

    list_display = ('base', 'symbol', 'date', 'rate')
    ordering = ('-date',)


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Category)
admin.site.register(ExchangeRate, ExchangeRateAdmin)
