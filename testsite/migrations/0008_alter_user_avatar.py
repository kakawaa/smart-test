# Generated by Django 3.2 on 2022-01-08 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testsite', '0007_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.TextField(default='https://v.xxxx.mobi/d4/pic/cms/xxxx/1641643508536.png?t=1641643508672'),
        ),
    ]
