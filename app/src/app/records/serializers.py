from django.conf import settings
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from app.common import get_logger
from app.records import misc
from app.records.models import (
    LabelsPredicted, Source, Record, Entity)


log = get_logger(__name__)


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class LabelsPredictedSerializer(serializers.ModelSerializer):

    class Meta:

        model = LabelsPredicted
        fields = ('label', 'confidence')


class EntitySerializer(serializers.ModelSerializer):

    class Meta:

        model = Entity
        exclude = ('id', 'record', 'entity_data')

    def to_representation(self, entity):

        result = super().to_representation(entity)
        existing_keys = set(result.keys())

        for attr_name, attr_value in entity.entity_attrs.items():
            if attr_name not in existing_keys:
                result[attr_name] = attr_value

        return result


class RecordSerializer(serializers.ModelSerializer):

    source = serializers.SlugRelatedField(slug_field='name', read_only=True)
    owner = UserSerializer()
    labels_predicted = LabelsPredictedSerializer(many=True)
    entities = EntitySerializer(many=True)

    class Meta:

        model = Record
        exclude = ('deleted',)

    def to_representation(self, record):

        result = super().to_representation(record)
        result['labels_predicted'].sort(
            key=lambda it: it['confidence'], reverse=True)

        return result


class RecordCreateSerializer(serializers.Serializer):

    text = serializers.CharField()
    source = serializers.CharField(
        required=False, default=settings.DEFAULT_SOURCE_NAME)
    ext_id = serializers.CharField(required=False)
    timestamp = serializers.DateTimeField(required=False)
    label = serializers.CharField(required=False, default=None, allow_null=True)

    def validate(self, attrs):

        user = self.context['request'].user
        source_name = attrs.pop('source')
        label = attrs['label']

        if source_name == settings.DEFAULT_SOURCE_NAME:
            attrs['source'] = Source.get_or_create_default(user)
            attrs['ext_id'] = None
        else:
            try:
                source = Source.objects.get(owner=user, name=source_name)
            except Source.DoesNotExist:
                raise ValidationError(
                    {'source_name': _('This user does not have this source')})

            if 'ext_id' not in attrs:
                raise ValidationError(
                    {'ext_id': _('This field is required.')}, 'required')

            attrs['source'] = source

            if Record.objects.filter(
                    owner=user, source=source, ext_id=attrs['ext_id']).exists():
                raise ValidationError(
                    {'ext_id': _('Record with specific ID of this source already exists')})

        if label is not None:
            if label not in settings.ALLOWED_LABELS:
                raise ValidationError({'label': _('Unsupported label')})

        if 'timestamp' not in attrs:
            attrs['timestamp'] = timezone.now()

        attrs['label_confirmed'] = label is not None
        attrs['owner'] = user

        return attrs

    def create(self, validated_data):

        record = Record.objects.create(**validated_data)

        if not record.label_confirmed:
            prediction_results = record.predict_labels()
            log.debug('Prediction results: %s', prediction_results)

        entities = record.extract_entities()
        log.debug('Extracted entities: %s', entities)

        record.notify_create()

        return record


class RecordIdSerializer(serializers.Serializer):

    record_id = serializers.CharField(write_only=True)

    def validate(self, attrs):

        record_id = attrs['record_id']

        try:
            record = Record.get_record_by_id(
                record_id, self.context['request'].user)
        except ValueError as exc:
            raise ValidationError({'record_id': str(exc)})
        except Record.DoesNotExist:
            raise NotFound()

        attrs['record'] = record

        return attrs


class RecordUpdateDeleteSerializer(RecordIdSerializer):

    text = serializers.CharField()

    def create(self, validated_data):

        record = validated_data['record']

        if record.text != validated_data['text']:
            record.text = validated_data['text']
            record.label = None
            record.label_confirmed = False
            record.save()

            prediction_results = record.predict_labels()
            log.debug('Prediction results: %s', prediction_results)

            entities = record.extract_entities()
            log.debug('Extracted entities: %s', entities)

            record.notify_update()

        return record


class LabelSetSerializer(RecordIdSerializer):

    label = serializers.CharField()
    force = serializers.BooleanField(default=False)

    def validate(self, attrs):

        super().validate(attrs)

        record = attrs['record']
        label = attrs['label']
        force = attrs['force']

        if record.label_confirmed and not force:
            raise ValidationError({'label': _('Label already confirmed')})

        if label not in settings.ALLOWED_LABELS:
            raise ValidationError({'label': _('This label is not allowed')})

        return attrs


class LabelConfirmSerializer(RecordIdSerializer):

    def validate(self, attrs):

        super().validate(attrs)

        record = attrs['record']

        if record.label_confirmed:
            raise ValidationError({'label': _('Label already confirmed')})

        if record.label is None:
            raise ValidationError({'detail': _('No label to confirm. Set label first')})

        attrs['label'] = record.label

        return attrs
