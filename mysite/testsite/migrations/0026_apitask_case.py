# Generated by Django 2.2.3 on 2020-05-05 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testsite', '0025_taskresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='apitask',
            name='case',
            field=models.TextField(default='NA'),
        ),
    ]
