# Generated by Django 3.2 on 2021-12-22 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testsite', '0018_automationtaskcaseassert_assert_type_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='automationtaskcontent',
            name='url',
            field=models.TextField(default=''),
        ),
    ]