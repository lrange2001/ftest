# Generated by Django 4.1.3 on 2023-04-04 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appdeploy', '0009_remove_app_app_package_app_app_deploy_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='app',
            name='app_restart',
        ),
        migrations.AlterField(
            model_name='app',
            name='app_script',
            field=models.CharField(max_length=100, verbose_name='应用安装材料'),
        ),
    ]