# Generated by Django 4.1.3 on 2023-04-04 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docdb',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
