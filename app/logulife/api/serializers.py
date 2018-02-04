from django.conf import settings
from django.db.utils import IntegrityError
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from logulife.api import models
from logulife.api import common
from logulife.api import exceptions


def deserialize(serializer_class, data):

    serializer = serializer_class(data=data)
    serializer.is_valid(raise_exception=True)

    return serializer


def serialize(serializer_class, instance, data=None, **kwargs):

    if data is None:
        serializer = serializer_class(instance, **kwargs)
    else:
        serializer = serializer_class(instance, data=data, **kwargs)
        serializer.is_valid(raise_exception=True)

    return serializer


class Customer(serializers.Serializer):

    id = serializers.IntegerField()
    username = serializers.CharField()


class Source(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    owner = Customer(read_only=True)


class Record(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(required=True)
    owner = Customer(read_only=True)
    source = Source(read_only=True)
    source_name = serializers.CharField(write_only=True)
    source_record_id = serializers.IntegerField(required=True)

    # Если пустое, взять текущее время
    timestamp = serializers.DateTimeField(
        format=settings.DATETIME_FORMAT,
        input_formats=(settings.DATETIME_FORMAT,),
        allow_null=True,
        required=False)

    label = serializers.CharField(required=False, allow_null=True)
    label_confirmed = serializers.BooleanField(required=False)
    need_verification = serializers.BooleanField(required=False)

    def validate(self, data):

        if not 'timestamp' in data:
            data['timestamp'] = timezone.now()
        else:
            data['timestamp'] = common.local_to_utc(data['timestamp'])

        return data

    def create(self, validated_data):

        customer = models.Customer.get_customer(user=validated_data.pop('user'))
        validated_data['owner'] = customer

        validated_data['source'] = models.Source.get_source(
            name=validated_data.pop('source_name'),
            owner=customer)

        try:
            record = models.Record.objects.create(**validated_data)
        except IntegrityError:
            raise exceptions.LogulifeException('Запись с переданными параметрами уже существует')

        return record

    def update(self, instance, validated_data):

        instance.text = validated_data['text']
        instance.save()

        return instance
