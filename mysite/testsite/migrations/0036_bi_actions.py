# Generated by Django 2.2.3 on 2020-07-14 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testsite', '0035_startuptime_time_detail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bi_Actions',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.TextField()),
                ('actions', models.TextField()),
                ('utime', models.DateTimeField()),
            ],
        ),
    ]
