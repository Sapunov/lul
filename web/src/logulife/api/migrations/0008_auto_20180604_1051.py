# Generated by Django 2.0.6 on 2018-06-04 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20180604_1044'),
    ]

    operations = [
        migrations.RenameField(
            model_name='record',
            old_name='_prediction_confidence',
            new_name='prediction_confidence',
        ),
    ]
