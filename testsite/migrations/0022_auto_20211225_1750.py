# Generated by Django 3.2 on 2021-12-25 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testsite', '0021_automationtaskresult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='automationtaskresult',
            name='final_value',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='automationtaskresult',
            name='response',
            field=models.TextField(null=True),
        ),
    ]
