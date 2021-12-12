# Generated by Django 3.2 on 2021-12-05 17:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('testsite', '0005_automationtaskcontent_automationtaskreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutomationTaskCase',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('taskname', models.CharField(max_length=32)),
                ('apiname', models.CharField(max_length=32)),
                ('casenum', models.IntegerField(default=1)),
                ('url', models.CharField(max_length=32)),
                ('status', models.TextField(default='待执行')),
                ('case_type', models.TextField(default='Get')),
                ('request_content', models.TextField(null=True)),
                ('ctime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='AutomationTaskCaseAssert',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('taskname', models.CharField(max_length=32)),
                ('apiname', models.CharField(max_length=32)),
                ('casenum', models.IntegerField(default=1)),
                ('parameter', models.CharField(max_length=32)),
                ('value', models.CharField(max_length=32)),
                ('assert_type', models.CharField(max_length=32)),
                ('ctime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
