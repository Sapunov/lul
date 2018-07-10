from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound

from app.spender.models import Category, Transaction


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class RecordSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    text = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:

        model = Category
        fields = ('id', 'name', 'description')
        read_only_fields = ('id',)

    def validate(self, attrs):

        name = attrs['name']

        if Category.objects.filter(name=name).exists():
            raise ValidationError({'name': _('This category already exists')})

        return attrs

    def create(self, validated_data):

        cat = Category.objects.create(
            name=validated_data['name'],
            description=validated_data.get('description', ''))

        return cat


class TransactionSerializer(serializers.ModelSerializer):

    owner = UserSerializer()
    record = serializers.PrimaryKeyRelatedField(read_only=True)
    record = RecordSerializer()
    direction = serializers.ChoiceField(choices=('income', 'expence'))

    class Meta:

        model = Transaction
        fields = (
            'id', 'amount', 'category',
            'category_confirmed', 'currency', 'direction',
            'owner', 'record', 'timestamp', 'direction_human')
