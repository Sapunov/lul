from django.contrib import admin

from .models import Transaction, Category, ExchangeRate, TransactionsSharing


class TransactionAdmin(admin.ModelAdmin):

    list_display = (
        'id', 'amount_int', 'amount_decimal', 'currency',
        'direction', 'category',  'owner', 'timestamp', 'category_confirmed', 'record')
    ordering = ('-timestamp',)


class ExchangeRateAdmin(admin.ModelAdmin):

    list_display = ('base', 'symbol', 'date', 'rate')
    ordering = ('-date',)


class TransactionsSharingAdmin(admin.ModelAdmin):

    list_display = ('owner', 'other_user', 'mode')


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Category)
admin.site.register(ExchangeRate, ExchangeRateAdmin)
admin.site.register(TransactionsSharing, TransactionsSharingAdmin)
