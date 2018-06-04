import json

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from rest_framework.exceptions import NotFound
from django.conf import settings

from logulife.api import exceptions
from logulife.api import classification
from logulife.api import entity_extraction
from logulife.api.signals import ready_to_process


class Source(models.Model):

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:

        unique_together = ('name', 'owner')

    @classmethod
    def get_source(cls, name, owner):

        try:
            source = cls.objects.get(name=name.lower(), owner=owner)
        except cls.DoesNotExist:
            raise exceptions.LogulifeException(
                'Источник данных `{0}` не существует у пользователя `{1}`'.format(
                    name, owner.username))

        return source

    def __str__(self):

        return '<Source: {0},{1}>'.format(self.name, self.owner.username)

    def __repr__(self):

        return self.__str__()


class Entity(models.Model):

    record = models.ForeignKey(
        'Record', on_delete=models.CASCADE, related_name='entities')
    name = models.CharField(max_length=50)
    entity_data = models.TextField()

    class Meta:

        verbose_name_plural = 'Entities'

    @property
    def entity_attrs(self):

        data = json.loads(self.entity_data)
        return data


class Record(models.Model):

    text = models.CharField(max_length=1000)

    # Так как записи представляют ценность для обучения классификатора,
    # удалять их нельзя никогда
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    source = models.ForeignKey(Source, null=True, on_delete=models.SET_NULL)

    source_record_id = models.IntegerField()
    timestamp = models.DateTimeField()
    label = models.CharField(max_length=100, blank=True, null=True)
    prediction_confidence = models.FloatField(default=0.0)
    label_confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        if not self.timestamp:
            self.timestamp = timezone.now()

        return super(Record, self).save(*args, **kwargs)

    class Meta:

        unique_together = ('source', 'source_record_id')

    def predict_label(self):

        results = classification.text.predict_label(self.text)
        top_result = results[0]
        label, confidence = top_result

        if not self.label_confirmed:
            self.label = label
            self.prediction_confidence = round(confidence, 4)

            if self.prediction_confidence >= settings.LABEL_CLASSIFICATION_THRESHOLD:
                self.label_confirmed = True

            self.save()

        return top_result

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
    def get_record(cls, user, source_name, source_record_id):

        source = Source.get_source(owner=user, name=source_name)

        try:
            record = cls.objects.get(
                owner=user,
                source=source,
                source_record_id=source_record_id)
        except cls.DoesNotExist:
            raise NotFound('Запись не существует')

        return record

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

    def notify_apps(self):

        if self.label_confirmed:
            ready_to_process.send(sender=Record, instance=self)

    def __str__(self):

        return '<Record: {0}>'.format(self.text[:140])

    def __repr__(self):

        return self.__str__()
