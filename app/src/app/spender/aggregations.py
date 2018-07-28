from collections import defaultdict
from django.conf import settings

from app.spender.models import ExchangeRate


class Amount:

    def __init__(self, integer=0, decimal=0):

        self.integer = integer
        self.decimal = decimal

    def add(self, integer, decimal):

        self.integer += integer
        self.decimal += decimal

    def to_representation(self):

        return self.integer + self.decimal / 10000.0

    def __add__(self, other):

        return Amount(self.integer + other.integer, self.decimal + other.decimal)


def sum_amounts(amounts):

    integers = 0
    decimals = 0

    for amount in amounts:
        integers += amount.integer
        decimals += amount.decimal

    return Amount(integers, decimals).to_representation()


def convert_amount(dict_obj):

    for key in dict_obj.keys():
        if isinstance(dict_obj[key], dict):
            convert_amount(dict_obj[key])
        elif isinstance(dict_obj[key], list):
            for i, _ in enumerate(dict_obj[key]):
                convert_amount(dict_obj[key][i])
        elif isinstance(dict_obj[key], Amount):
            dict_obj[key] = dict_obj[key].to_representation()


def convert_currency(code_from, code_to, amount):

    return amount


def default_currency_dict(currencies, default_currency):

    amounts = []
    approx = False

    for currency in currencies:
        currency_code = currency['currency']
        amount = currency['amount']
        if currency_code != default_currency:
            amounts.append(
                convert_currency(currency_code, default_currency, amount))
            approx = True
        else:
            amounts.append(amount)

    return {
        'approx': approx,
        'amount': sum_amounts(amounts),
        'currency': default_currency
    }


def _dict_to_list(dict_obj, id_field=None):

    ans = []

    for key, value in dict_obj.items():
        ans.append(value)
        if id_field is not None:
            ans[-1][id_field] = key

    return ans


def _transform_currencies_dict(currencies_dict):

    for key, value in currencies_dict.items():
        currencies_dict[key] = {'amount': value}

    return _dict_to_list(currencies_dict, id_field='currency')


def _aggregate_direction_transactions(transactions):

    summary = {
        'default_currency': {
            'currency': settings.DEFAULT_CURRENCY,
            'amount': Amount(),
            'approx': False
        },
        'currencies': defaultdict(lambda: Amount())
    }
    categories = defaultdict(
        lambda: {
            'currencies': defaultdict(lambda: Amount()),
            'name': None,
            'default_currency': {
                'currency': settings.DEFAULT_CURRENCY,
                'amount': Amount(),
                'approx': False
            }
        }
    )

    for transaction in transactions:
        # categories
        categories[transaction.category.id]['currencies'][transaction.currency] += Amount(
            transaction.amount_int, transaction.amount_decimal
        )
        # categories -> default currency
        categories[transaction.category.id]['default_currency']['amount'] += Amount(
            transaction.default_currency_amount_int,
            transaction.default_currency_amount_decimal
        )
        if settings.DEFAULT_CURRENCY != transaction.currency:
            categories[transaction.category.id]['default_currency']['approx'] = True

        categories[transaction.category.id]['name'] = transaction.category.name
        # summary
        summary['currencies'][transaction.currency] += Amount(
            transaction.amount_int,
            transaction.amount_decimal
        )
        # summary -> default currency
        summary['default_currency']['amount'] += Amount(
            transaction.default_currency_amount_int,
            transaction.default_currency_amount_decimal
        )
        if transaction.currency != settings.DEFAULT_CURRENCY:
            summary['default_currency']['approx'] = True

    for category_id in categories:
        categories[category_id]['currencies'] = _transform_currencies_dict(
            categories[category_id]['currencies'])

        if categories[category_id]['default_currency']['approx'] == False:
            categories[category_id]['default_currency'] = None
        else:
            del categories[category_id]['default_currency']['approx']

    if summary['default_currency']['approx'] == False:
        summary['default_currency'] = None
    else:
        del summary['default_currency']['approx']

    categories = _dict_to_list(categories, id_field='id')

    summary['currencies'] = _transform_currencies_dict(summary['currencies'])

    return {
        'summary': summary,
        'categories': categories
    }


def aggregate_transactions(transactions):

    income = _aggregate_direction_transactions(
        transactions.filter(direction=0, category__isnull=False))
    expense = _aggregate_direction_transactions(
        transactions.filter(direction=1, category__isnull=False))

    convert_amount(income)
    convert_amount(expense)

    return {
        'income': income,
        'expense': expense
    }
