from django.db import models

# Create your models here.


# class ServerDetails(models.Model):




class Group(models.Model):
    groupname = models.CharField(max_length=100,unique=True,verbose_name='组名称')

    class Meta:
        app_label = 'server'
        db_table = 'myapp_group'



class Server(models.Model):
    hostname = models.CharField(max_length=100,unique=True,blank=False,verbose_name='主机名')
    username = models.CharField(max_length=100,blank=False,verbose_name='用户名')
    ipaddress = models.GenericIPAddressField(blank=False,verbose_name='IP地址')
    port = models.IntegerField(blank=False,verbose_name='端口号')
    auth_choice = models.CharField(max_length=30,blank=False,choices=((1,'密码'),(2,'密钥')),verbose_name='认证类型')
    auth_password = models.CharField(max_length=100,null=True,verbose_name='密码')
    auth_key = models.CharField(max_length=100,null=True,blank=True,verbose_name='密钥')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    group = models.ManyToManyField(Group)

    class Meta:
        app_label = 'server' #标记app名称
        db_table = 'myapp_server' #自定义生成的表名称



class Serverdetails(models.Model):
    hostname = models.CharField(max_length=100,blank=True,null=True,unique=True,verbose_name='服务器主机名称')
    public_ip = models.CharField(max_length=100,blank=True,null=True,verbose_name='公网ip')
    os_version = models.CharField(max_length=100,blank=True,null=True,verbose_name='系统版本')
    disk = models.CharField(max_length=200,blank=True,null=True,verbose_name='磁盘')
    memory = models.CharField(max_length=200,blank=True,null=True,verbose_name='内存')
    private_ip = models.CharField(max_length=100,blank=True,null=True,verbose_name='内网ip')
    machine_type = models.CharField(max_length=100,blank=True,null=True,verbose_name='服务器类型')
    cpu_num = models.CharField(max_length=100,blank=True,null=True,verbose_name='CPU核数')
    cpu_model = models.CharField(max_length=100,blank=True,null=True,verbose_name='CPU信息')
    put_shelves_date = models.CharField(max_length=100,blank=True,null=True,verbose_name='运行时间')
    class Meta:
        app_label = 'server'
        db_table = 'myapp_serverdetails'
    # class Meta:
    #     app_label = 'serverdetails'
    #     db_table = 'myapp_server_details'



