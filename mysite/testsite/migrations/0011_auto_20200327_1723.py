# Generated by Django 2.2.3 on 2020-03-27 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testsite', '0010_user_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=32),
        ),
    ]
