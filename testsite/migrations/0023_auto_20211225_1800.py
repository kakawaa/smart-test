# Generated by Django 3.2 on 2021-12-25 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testsite', '0022_auto_20211225_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='automationtaskcontent',
            name='run_id',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='automationtaskresult',
            name='run_id',
            field=models.TextField(default=''),
        ),
    ]
