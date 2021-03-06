# Generated by Django 3.2 on 2021-12-05 10:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('testsite', '0004_automationtask_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutomationTaskContent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('taskname', models.CharField(max_length=32)),
                ('apiname', models.CharField(max_length=32)),
                ('url', models.CharField(max_length=32)),
                ('status', models.TextField(default='待执行')),
                ('ctime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='AutomationTaskReport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('taskname', models.CharField(max_length=32)),
                ('apiname', models.CharField(max_length=32)),
                ('success_num', models.IntegerField(default=0)),
                ('error_num', models.IntegerField(default=0)),
                ('runner', models.TextField(default='自动化')),
                ('ctime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
