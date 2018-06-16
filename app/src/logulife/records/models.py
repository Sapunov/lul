import json

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import NotFound

from logulife.common import get_logger
from logulife.records import classification
from logulife.records import entity_extraction
from logulife.records.signals import ready_to_process


log = get_logger(__file__)


class Source(models.Model):

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def get_or_create_default(cls, user):

        source, _created = cls.objects.get_or_create(
            owner=user, name=settings.DEFAULT_SOURCE_NAME)

        return source

    class Meta:

        unique_together = ('name', 'owner')

    def __str__(self):

        return '<Source: {0},{1}>'.format(self.name, self.owner.username)

    def __repr__(self):

        return self.__str__()


class Entity(models.Model):

    record = models.ForeignKey(
        'Record', on_delete=models.CASCADE, related_name='entities')
    name = models.CharField(max_length=50)
    raw = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    pos_start = models.IntegerField()
    pos_end = models.IntegerField()
    entity_data = models.TextField()

    @classmethod
    def create_entity(cls, record, entity):

        entity = cls.objects.create(
            record=record,
            name=entity.entity_name,
            raw=entity.raw,
            value=entity.value,
            pos_start=entity.start,
            pos_end=entity.end,
            entity_data=json.dumps(entity.get_attrs())
        )

        return entity

    class Meta:

        verbose_name_plural = 'Entities'

    @property
    def entity_attrs(self):

        data = json.loads(self.entity_data)
        return data

    def __str__(self):

        return '<{0}: {1}>'.format(self.name, self.raw)

    def __repr__(self):

        return self.__str__()


class LabelsPredicted(models.Model):

    record = models.ForeignKey('Record',
        on_delete=models.CASCADE, related_name='labels_predicted', null=True)
    label = models.CharField(max_length=100)
    confidence = models.FloatField()

    def __str__(self):

        return '<LabelsPredicted: label={0}; confidence={1}>'.format(
            self.label,
            self.confidence)

    def __repr__(self):

        return self.__str__()


class Tag(models.Model):

    text = models.CharField(max_length=100, primary_key=True)

    @classmethod
    def get_or_create(cls, tag_text):

        tag_text = tag_text.lower().replace(' ', '_')
        tag, _created = cls.objects.get_or_create(text=tag_text)

        return tag


class Record(models.Model):

    text = models.CharField(max_length=1000)
    # Так как записи представляют ценность для обучения классификатора,
    # удалять их нельзя никогда
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    source = models.ForeignKey(Source, null=True, on_delete=models.SET_NULL)
    ext_id = models.CharField(max_length=40, null=True, blank=True)
    timestamp = models.DateTimeField()
    label = models.CharField(max_length=100, blank=True, null=True)
    label_confirmed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name='+')

    class Meta:

        unique_together = ('source', 'ext_id')

    @classmethod
    def get_record_by_id(cls, record_id, user):

        log.debug('Trying to get record with record_id:%s, user:%s', record_id, user)

        if '_' in record_id:
            try:
                source_name, ext_id = record_id.split('_')
            except ValueError:
                raise ValueError(
                    _('Wrong record id. Right pattern: <source>_<record_id>'))
        else:
            source_name = settings.DEFAULT_SOURCE_NAME
            try:
                ext_id = int(record_id)
            except ValueError:
                raise ValueError(_('Record id must be of type int'))

        if source_name == settings.DEFAULT_SOURCE_NAME:
            record = cls.objects.get(owner=user, pk=ext_id, deleted=False)
        else:
            record = cls.objects.get(
                owner=user, source__name=source_name, ext_id=ext_id, deleted=False)

        return record

    def archive_record(self):

        self.deleted = True
        self.save()

    def set_label(self, label, confirm=False):

        self.label = label
        if confirm:
            self.label_confirmed = True
            self.labels_predicted.all().delete()

        self.save()

    def predict_labels(self):

        prediction_results = classification.text.predict_labels(self.text)
        labels_predicted = []

        for label, confidence in prediction_results[:settings.SAVED_PREDICTION_RESULTS]:
            labels_predicted.append(LabelsPredicted.objects.create(
                record=self, label=label, confidence=round(confidence, 4)))

        top_result = labels_predicted[0]

        if top_result.confidence > settings.LABEL_CLASSIFICATION_THRESHOLD:
            self.set_label(top_result.label)

        return labels_predicted

    def _process_tags(self):

        tag_entities = set(self.entities.filter(
            name='TagEntity').values_list('value', flat=True))

        if tag_entities:
            current_tags = set(self.tags.all().values_list('text', flat=True))

            to_delete = current_tags - tag_entities
            to_add = tag_entities - current_tags

            self.tags.filter(text__in=to_delete).delete()

            for tag_text in to_add:
                tag = Tag.get_or_create(tag_text)
                self.tags.add(tag)

    def extract_entities(self):

        self.entities.all().delete() # Delete old entities before

        extracted_entities = entity_extraction.extract_entities(self.text)
        entities = []
        for entity in extracted_entities:
            entities.append(Entity.create_entity(self, entity))

        self._process_tags()

        return entities

    @classmethod
    def learn_from_records(cls):

        records = cls.objects.filter(label__isnull=False, label_confirmed=True)

        if records.count() > 0:
            text_records = []
            labels = []

            for record in records:
                text_records.append(record.text)
                labels.append(record.label)

            classification.text.learn(text_records, labels)

    def notify_create(self):

        pass

    def notify_update(self):

        pass

    def notify_delete(self):

        pass

    def __str__(self):

        return '<Record: {0}>'.format(self.text[:140])

    def __repr__(self):

        return self.__str__()
