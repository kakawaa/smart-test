# Generated by Django 2.2.6 on 2020-11-02 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testsite', '0050_service_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='admin_type',
            field=models.CharField(default='', max_length=32),
        ),
    ]
