from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound
from datetime import timedelta

from app.spender.models import Category, Transaction, TransactionsSharing
from app.spender import timeperiods


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class RecordSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    text = serializers.CharField()
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)


class CategorySerializer(serializers.ModelSerializer):

    owner = UserSerializer(read_only=True)

    class Meta:

        model = Category
        fields = (
            'id', 'name', 'description',
            'owner', 'direction', 'direction_human')
        read_only_fields = ('id',)

    def validate(self, attrs):

        name = attrs['name']
        direction = attrs['direction']
        user = self.context['request'].user

        if Category.objects.filter(
                name=name,
                owner=user,
                direction=direction).exists():
            raise ValidationError({'name': _('This category already exists')})

        return attrs

    def create(self, validated_data):

        cat = Category.objects.create(
            name=validated_data['name'],
            description=validated_data.get('description', ''),
            owner=self.context['request'].user,
            direction=validated_data['direction'])

        return cat


class CategoryDeleteSerializer(serializers.Serializer):

    id = serializers.IntegerField()

    def validate(self, attrs):

        cat_id = attrs['id']

        try:
            category = Category.objects.get(
                pk=cat_id,
                owner=self.context['request'].user)
        except Category.DoesNotExist:
            raise NotFound({'id': _('Category not found')})

        attrs['category'] = category

        return attrs


class CategoryVariantSerializer(serializers.ModelSerializer):

    confidence = serializers.FloatField(default=0.0, read_only=True)

    class Meta:

        model = Category
        fields = ('id', 'name', 'confidence', 'direction')


class DefaultCurrency(serializers.Serializer):

    amount = serializers.FloatField()
    currency = serializers.CharField()


class TransactionSerializer(serializers.ModelSerializer):

    owner = UserSerializer()
    record = serializers.PrimaryKeyRelatedField(read_only=True)
    record = RecordSerializer()
    direction = serializers.ChoiceField(choices=('income', 'expense'))
    # category_variants = CategoryVariantSerializer(many=True)
    category = CategorySerializer()
    default_currency = DefaultCurrency(allow_null=True)

    class Meta:

        model = Transaction
        fields = (
            'id', 'amount', 'category',
            'category_confirmed', 'currency', 'direction',
            'owner', 'record', 'timestamp',
            'direction_human', 'default_currency')


class CategorySetSerializer(serializers.Serializer):

    transaction_id = serializers.IntegerField()
    category_id = serializers.IntegerField()

    def validate(self, attrs):

        category_id = attrs['category_id']
        transaction_id = attrs['transaction_id']

        try:
            transaction = Transaction.objects.get(
                owner=self.context['request'].user,
                pk=transaction_id)
        except Transaction.DoesNotExist:
            raise NotFound({'transaction_id': _(
                'Specified transactions does not exist for the user')})

        try:
            category = Category.objects.get(pk=category_id)
            if category.owner is not None and category.owner != self.context['request'].user:
                raise Category.DoesNotExist
        except Category.DoesNotExist:
            raise ValidationError({'category_id': _(
                'User does not have specified category')})

        attrs['transaction'] = transaction
        attrs['category'] = category

        return attrs


class CategoryIdSerializer(serializers.Serializer):

    transaction_id = serializers.IntegerField()

    def validate(self, attrs):

        transaction_id = attrs['transaction_id']

        try:
            transaction = Transaction.objects.get(
                owner=self.context['request'].user,
                pk=transaction_id)
        except Transaction.DoesNotExist:
            raise NotFound({'transaction_id': _(
                'Specified transactions does not exist for the user')})

        if transaction.category is None:
            raise ValidationError({'category': _('Category not set')})

        attrs['transaction'] = transaction

        return attrs


WITH_CATEGORY = '_with'

NO_CATEGORY = '_null'


class FilterParamsSerializer(serializers.Serializer):

    q = serializers.CharField(required=False, default='')
    page = serializers.IntegerField(required=False, default=1)
    period = serializers.CharField(required=False, default='month')
    # По умолчанию выводить записи всех категорий
    category = serializers.CharField(required=False, default=WITH_CATEGORY)
    other_owners = serializers.CharField(required=False)

    PERIODS = {
        'week': timeperiods.week,
        'today': timeperiods.today,
        'yesterday': timeperiods.yesterday,
        'month': timeperiods.month,
        'year': timeperiods.year,
        'month-one': timeperiods.month_one,
        'month-two': timeperiods.month_two,
        'whole': timeperiods.whole
    }

    def validate(self, attrs):

        user = self.context['request'].user
        period = attrs['period']
        category = attrs['category']
        other_owners_ids = attrs.get('other_owners', None)

        if period in FilterParamsSerializer.PERIODS:
            if period == 'whole':
                start, end = FilterParamsSerializer.PERIODS[period](user)
            else:
                start, end = FilterParamsSerializer.PERIODS[period]()
            attrs['timestamp_from'] = start
            attrs['timestamp_to'] = end
        else:
            raise ValidationError({'period': _('Unsupported period')})

        if category not in (WITH_CATEGORY, NO_CATEGORY):
            attrs['category'] = int(category)

        if other_owners_ids:
            other_owners = []
            try:
                other_owners_ids = [int(it) for it in other_owners_ids.split(',')]
                for user_id in other_owners_ids:
                    if user_id == user.pk:
                        continue
                    try:
                        other_user = User.objects.get(pk=user_id)
                        if TransactionsSharing.objects.filter(
                                owner=other_user, other_user=user).exists():
                            other_owners.append(other_user)
                    except User.DoesNotExist:
                        continue
            except ValueError:
                raise ValidationError({'owners': _('Owner ids invalid')})

            attrs['other_owners_users'] = other_owners

        return attrs
