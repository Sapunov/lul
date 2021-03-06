# Generated by Django 2.0.6 on 2018-06-15 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='ext_id',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='source_record_id',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.RemoveField(
            model_name='record',
            name='prediction_confidence',
        ),
        migrations.AlterUniqueTogether(
            name='record',
            unique_together={('source', 'ext_id')},
        ),
    ]
