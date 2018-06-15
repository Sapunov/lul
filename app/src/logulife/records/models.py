import json

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from rest_framework.exceptions import NotFound
from django.conf import settings

from . import exceptions
from . import classification
from . import entity_extraction
from .signals import ready_to_process


class Source(models.Model):

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def get_or_create_default(cls, user):

        source, _ = cls.objects.get_or_create(
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
    raw = models.CharField(max_length=200, blank=True)
    entity_data = models.TextField()

    def save(self, *args, **kwargs):

        if not self.pk:
            self.raw = json.loads(self.entity_data)['raw']

        super().save(*args, **kwargs)

    class Meta:

        verbose_name_plural = 'Entities'

    @property
    def entity_attrs(self):

        data = json.loads(self.entity_data)
        return data

    def __str__(self):

        return '<Entity: {0}>'.format(self.raw)

    def __repr__(self):

        return self.__str__()


class LabelPredictionResult(models.Model):

    record = models.ForeignKey('Record',
        on_delete=models.CASCADE, related_name='label_prediction_results', null=True)
    label = models.CharField(max_length=100)
    confidence = models.FloatField()

    def __str__(self):

        return '<PredictionResult: label={0}; confidence={1}>'.format(
            self.label,
            self.confidence)


class Record(models.Model):

    text = models.CharField(max_length=1000)
    # Так как записи представляют ценность для обучения классификатора,
    # удалять их нельзя никогда
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    source = models.ForeignKey(Source, null=True, on_delete=models.SET_NULL)
    ext_id = models.CharField(max_length=40, null=True)
    timestamp = models.DateTimeField()
    label = models.CharField(max_length=100, blank=True, null=True)
    label_confirmed = models.BooleanField(default=False)

    class Meta:

        unique_together = ('source', 'ext_id')

    def predict_label(self):

        pass

    def extract_entities(self):

        # Delete old entities before
        for entity in self.entities.all():
            entity.delete()

        entities = entity_extraction.extract_entities(self.text)
        for entity in entities:
            attrs = json.dumps(entity.get_attrs())
            Entity.objects.create(
                record=self,
                name=entity.entity_name,
                entity_data=attrs)

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

    def notify_listeners(self):

        ready_to_process.send(sender=Record, instance=self)

    def __str__(self):

        return '<Record: {0}>'.format(self.text[:140])

    def __repr__(self):

        return self.__str__()
