# Generated by Django 3.2 on 2021-12-05 18:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('testsite', '0008_auto_20211205_1754'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutomationTaskCaseAssert',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('taskname', models.CharField(max_length=32)),
                ('apiname', models.CharField(max_length=32)),
                ('casenum', models.IntegerField(default=1)),
                ('parameter', models.TextField(default='code')),
                ('value', models.TextField(default='200')),
                ('assert_type', models.TextField(default='==')),
                ('ctime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.RemoveField(
            model_name='automationtaskcase',
            name='assert_type',
        ),
        migrations.RemoveField(
            model_name='automationtaskcase',
            name='parameter',
        ),
        migrations.RemoveField(
            model_name='automationtaskcase',
            name='value',
        ),
    ]
