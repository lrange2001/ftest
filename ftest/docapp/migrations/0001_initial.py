# Generated by Django 3.0.1 on 2023-04-03 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='docdb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docName', models.CharField(max_length=100, verbose_name='文件名称')),
                ('docPath', models.CharField(max_length=100, verbose_name='文件路径')),
            ],
            options={
                'db_table': 'docdb',
            },
        ),
    ]
