# Generated by Django 3.2 on 2021-12-25 17:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('testsite', '0020_delete_automationtaskresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutomationTaskResult',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('taskname', models.TextField()),
                ('apiname', models.TextField()),
                ('casename', models.TextField()),
                ('status', models.TextField()),
                ('parameter', models.TextField()),
                ('assert_type', models.TextField()),
                ('pre_value', models.TextField()),
                ('final_value', models.TextField()),
                ('response', models.TextField()),
                ('runner', models.TextField(default='自动化')),
                ('ctime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
