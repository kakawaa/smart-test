# Generated by Django 2.2.3 on 2020-07-06 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testsite', '0034_bugmonitor'),
    ]

    operations = [
        migrations.AddField(
            model_name='startuptime',
            name='time_detail',
            field=models.TextField(default=''),
        ),
    ]
