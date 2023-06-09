# Generated by Django 4.1.3 on 2023-04-02 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('server', '0010_alter_server_auth_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=100, unique=True, verbose_name='应用名称')),
                ('app_logo', models.FileField(upload_to='', verbose_name='应用logo')),
                ('app_package', models.FileField(upload_to='', verbose_name='应用包')),
                ('app_script', models.FileField(upload_to='', verbose_name='应用安装脚本')),
                ('app_start', models.CharField(max_length=100, verbose_name='应用启动方式')),
                ('app_stop', models.CharField(max_length=100, verbose_name='应用停止方式')),
                ('app_restart', models.CharField(max_length=100, verbose_name='应用重启方式')),
                ('server', models.ManyToManyField(to='server.server')),
            ],
        ),
    ]
