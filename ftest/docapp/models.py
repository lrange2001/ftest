from django.db import models

# Create your models here.
class docdb(models.Model):
    docName = models.CharField(max_length=100,verbose_name='文件名称')
    docPath = models.CharField(max_length=100,verbose_name='文件路径')

    class Meta:
        app_label = 'docapp'
        db_table = 'docdb'