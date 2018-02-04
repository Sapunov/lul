from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):

        return 'Customer [{0} - {1}]'.format(self.user.id, self.user.username)

    def __repr__(self):

        return self.__str__()


class Source(models.Model):

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user_id = models.IntegerField()

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

    def __str__(self):

        return 'Record [{0} - {1}]'.format(self.id, self.text[:140])

    def __repr__(self):

        return self.__str__()
