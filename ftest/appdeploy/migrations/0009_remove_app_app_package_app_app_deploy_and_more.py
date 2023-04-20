# Generated by Django 4.1.3 on 2023-04-04 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appdeploy', '0008_auto_20230403_2146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='app',
            name='app_package',
        ),
        migrations.AddField(
            model_name='app',
            name='app_deploy',
            field=models.URLField(blank=True, max_length=100, null=True, verbose_name='应用安装指令'),
        ),
        migrations.AlterField(
            model_name='app',
            name='app_restart',
            field=models.CharField(max_length=100, verbose_name='应用重启指令'),
        ),
        migrations.AlterField(
            model_name='app',
            name='app_script',
            field=models.FileField(upload_to='knowledge_ase/', verbose_name='应用安装材料'),
        ),
        migrations.AlterField(
            model_name='app',
            name='app_start',
            field=models.CharField(max_length=100, verbose_name='应用启动指令'),
        ),
        migrations.AlterField(
            model_name='app',
            name='app_stop',
            field=models.CharField(max_length=100, verbose_name='应用停止指令'),
        ),
        migrations.AlterField(
            model_name='app',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
