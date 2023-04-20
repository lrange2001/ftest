from django.db import models

from server.models import Server
# Create your models here.
class App(models.Model):
    app_name = models.CharField(max_length=100,unique=True,verbose_name='应用名称')
    app_script = models.CharField(verbose_name='应用安装材料',max_length=100)
    app_deploy = models.URLField(verbose_name='应用安装指令',max_length=100,null=True,blank=True)
    app_start = models.CharField(max_length=100,verbose_name='应用启动指令')
    app_stop = models.CharField(max_length=100,verbose_name='应用停止指令')
    create_time = models.DateTimeField(auto_now_add=True,null=True,blank=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,null=True,blank=True,verbose_name='更新时间')
    class Meta:
        app_label = 'appdeploy'
        db_table = 'myapp_app'


class AppDeploy(models.Model):
    app_hostanme = models.CharField(max_length=100,verbose_name='已运行主机名')
    app_public_ip = models.CharField(max_length=100,blank=True,null=True,verbose_name='公网IP')
    app_private_ip = models.CharField(max_length=100,blank=True,null=True,verbose_name='内网IP')
    app_server = models.ManyToManyField(to=App)

    class Meta:
        app_label = 'appdeploy'
        db_table = 'myapp_runserver'