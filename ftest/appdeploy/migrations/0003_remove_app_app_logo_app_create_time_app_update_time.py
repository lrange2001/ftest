# Generated by Django 4.1.3 on 2023-04-02 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appdeploy', '0002_alter_app_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='app',
            name='app_logo',
        ),
        migrations.AddField(
            model_name='app',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间'),
        ),
        migrations.AddField(
            model_name='app',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间'),
        ),
    ]
