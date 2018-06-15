from django.conf import settings
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from . import exceptions
from . import misc
from .models import LabelPredictionResult, Source, Record
from logulife.common import get_logger


log = get_logger(__name__)


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class LabelPredictionResultSerializer(serializers.ModelSerializer):

    class Meta:

        model = LabelPredictionResult
        fields = ('label', 'confidence')


class RecordSerializer(serializers.ModelSerializer):

    source = serializers.SlugRelatedField(slug_field='name', read_only=True)
    owner = UserSerializer()
    label_prediction_results = LabelPredictionResultSerializer(many=True)

    class Meta:

        model = Record
        fields = '__all__'


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
        return record
