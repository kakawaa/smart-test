# Generated by Django 2.2.3 on 2020-06-25 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testsite', '0028_operation_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='startuptime',
            name='timecost',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='startuptime',
            name='type',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='operation_log',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
