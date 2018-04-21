from django.conf import settings
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from logulife.api import misc
from logulife.api import exceptions
from logulife.api import models
from logulife.common import serialize, deserialize


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class SourceSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    owner = UserSerializer(read_only=True)


class RecordSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(required=True)
    owner = UserSerializer(read_only=True)
    source = SourceSerializer(read_only=True)
    source_name = serializers.CharField(write_only=True)
    source_record_id = serializers.IntegerField(required=True)

    # Если пустое, взять текущее время
    timestamp = serializers.DateTimeField(
        format=settings.DATETIME_FORMAT,
        input_formats=(settings.DATETIME_FORMAT,),
        allow_null=True,
        required=False)

    label = serializers.CharField(read_only=True)
    label_confirmed = serializers.BooleanField(read_only=True)

    def validate(self, data):

        if 'timestamp' not in data:
            data['timestamp'] = timezone.now()
        else:
            data['timestamp'] = misc.local_to_utc(data['timestamp'])

        return data

    def create(self, validated_data):

        validated_data['owner'] = self.context.get('request').user

        validated_data['source'] = models.Source.get_source(
            name=validated_data.pop('source_name'),
            owner=validated_data['owner'])

        try:
            record = models.Record.objects.create(**validated_data)
        except IntegrityError:
            raise exceptions.LogulifeException('Запись с переданными параметрами уже существует')

        return record

    def update(self, instance, validated_data):

        instance.text = validated_data['text']
        instance.save()

        return instance
