from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from logulife.api import exceptions
from logulife.api import classification


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

        return '<Source: {0}>'.format(self.name)

    def __repr__(self):

        return self.__str__()


class Record(models.Model):

    text = models.CharField(max_length=1000)

    # Так как записи представляют ценность для обучения классификатора,
    # удалять их нельзя никогда
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    source = models.ForeignKey(Source, null=True, on_delete=models.SET_NULL)

    source_record_id = models.IntegerField()
    timestamp = models.DateTimeField()
    label = models.CharField(max_length=100, blank=True, null=True)
    label_confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        if not self.timestamp:
            self.timestamp = timezone.now()

        return super(Record, self).save(*args, **kwargs)

    class Meta:

        unique_together = ('source', 'source_record_id')

    def predict_label(self):

        results = classification.text.predict_label(self.text)
        self.label = results[0][0]
        self.save()

        return self.label

    @classmethod
    def get_record(cls, user, source_name, source_record_id):

        source = Source.get_source(owner=user, name=source_name)

        try:
            record = cls.objects.get(
                owner=user,
                source=source,
                source_record_id=source_record_id)
        except cls.DoesNotExist:
            raise exceptions.LogulifeException('Запись не существует')

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

    def __str__(self):

        return '<Record: {0}>'.format(self.text[:140])

    def __repr__(self):

        return self.__str__()
