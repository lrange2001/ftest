# Generated by Django 4.1.3 on 2023-04-03 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appdeploy', '0006_alter_app_app_package_alter_app_app_script'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='app_script',
            field=models.FileField(upload_to='', verbose_name='应用安装脚本'),
        ),
    ]
