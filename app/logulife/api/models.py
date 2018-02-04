from django.db import models
from django.contrib.auth.models import User

from logulife.api import exceptions


class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def username(self):

        return self.user.username

    @classmethod
    def get_customer(cls, user):

        try:
            customer = cls.objects.get(user=user)
        except cls.DoesNotExist:
            raise exceptions.LogulifeException('Пользователь не существует')

        return customer

    def __str__(self):

        return 'Customer [{0} - {1}]'.format(self.user.id, self.user.username)

    def __repr__(self):

        return self.__str__()


class Source(models.Model):

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user_id = models.IntegerField()

    class Meta:

        unique_together = ('owner', 'user_id')


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

        return 'Source [{0} - {1}]'.format(self.id, self.name)

    def __repr__(self):

        return self.__str__()


class Record(models.Model):

    text = models.CharField(max_length=1000)

    # Так как записи представляют ценность для обучения классификатора,
    # удалять их нельзя никогда
    owner = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    source = models.ForeignKey(Source, null=True, on_delete=models.SET_NULL)

    source_record_id = models.IntegerField()
    timestamp = models.DateTimeField()
    label = models.CharField(max_length=100, blank=True, null=True)
    label_confirmed = models.BooleanField(default=False)
    need_verification = models.BooleanField(default=False)

    class Meta:

        unique_together = ('source', 'source_record_id')


    @classmethod
    def get_record(cls, user, source_name, source_record_id):

        customer = Customer.get_customer(user=user)
        source = Source.get_source(owner=customer, name=source_name)

        try:
            record = cls.objects.get(
                owner=customer,
                source=source,
                source_record_id=source_record_id)
        except cls.DoesNotExist:
            raise exceptions.LogulifeException('Запись не существует')

        return record

    def __str__(self):

        return 'Record [{0} - {1}]'.format(self.id, self.text[:140])

    def __repr__(self):

        return self.__str__()
