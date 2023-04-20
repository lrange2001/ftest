from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from appdeploy.models import App,AppDeploy
from appdeploy.serializers import AppSerializer,AppDeploySerializer
from appdeploy import serializers
from rest_framework.views import Response

from server.models import Server,Serverdetails
from server.other import register_serverinfoTodb
# Create your views here.
import os
import read_config
import shutil
from server.other.get_node import to_node
class AppView(ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer


class AppApiView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            Appobj = App.objects.all()
            result = serializers.AppSerializer(Appobj,many=True)
            res = {"code":200,"data":result.data}
        except Exception as f:
            res = {'code': 500,"message":f}
        return Response(res)

    def post(self, request, *args, **kwargs):
        if request.FILES.getlist('file'):
            '''读取配置文件 目标存放位置'''
            path = read_config.main('uploadconf')
            path = path['app_data_path']
            files =  request.FILES.getlist('file')
            for file in files:
                f = open(os.path.join(path,file.name),'wb+')
                for txt in file.chunks():
                   f.write(txt)
                f.close()
            return Response({'code':200,'message':'上传数据成功'})
        else:
            AppName = request.data.get('AppName')
            AppRun = request.data.get('AppRUN')
            AppSTOP = request.data.get('AppSTOP')
            AppDEPLOY = request.data.get('AppDEPLOY')

            files = request.data.get('fileList')
            for fileName in files:
                '''读取配置文件 目标存放位置'''
                path = read_config.main('uploadconf')
                path = path['app_data_path']
                fileName = fileName['name']
                AppDir = os.path.join(path,AppName)
                try:
                    os.mkdir(AppDir)
                except Exception as f:
                    pass
                shutil.move(os.path.join(path,fileName),os.path.join(AppDir,fileName))
            App.objects.create(
                app_name=AppName,
                app_deploy=AppDEPLOY,
                app_start=AppRun,
                app_stop=AppSTOP,
                app_script=str(AppDir)
            ).save()
            return Response({'code':200,'message':'自定义APP已完成添加'})
    def put(self, request):
        AppName = request.data.get('app_name')
        AppRun = request.data.get('app_start')
        AppSTOP = request.data.get('app_stop')
        AppDEPLOY = request.data.get('app_deploy')
        files = request.data.get('fileList')
        id = str(request.path).split('/')[3]
        path = read_config.main('uploadconf')
        path = path['app_data_path']
        AppDir = os.path.join(path,AppName)
        updateDATA = {
            "app_name": AppName,
            "app_start": AppRun,
            "app_stop": AppSTOP,
            "app_deploy": AppDEPLOY,
            "app_script": AppDir,
        }
        if len(files) != 0:
            for fileName in files:
                fileName = fileName['name']
                try:
                    os.remove(AppDir)
                    os.mkdir(AppDir)
                except Exception as f:
                    print(f)
                shutil.move(os.path.join(path, fileName), os.path.join(AppDir, fileName))
        try:
            Appobj = App.objects.get(id=id)
            Appobj.app_name = AppName
            Appobj.app_start = AppRun
            Appobj.app_stop = AppSTOP
            Appobj.app_deploy = AppDEPLOY
            Appobj.app_script = AppDir
            Appobj.save()
        except Exception as f:
            return Response({'code':500,'message':'%s'%f})
        return Response({'code':200,'message':'同步数据已完成'})

    def delete(self, request, *args, **kwargs):
        id = str(request.path).split('/')[3]
        appobj = App.objects.get(id=id)
        path = appobj.app_script
        try:
            os.remove(path)
            message = '删除成功'
            code = 200
            App.objects.filter(id=id).delete()
        except Exception as f:
            message = f
            code = 500
        return Response({'code':code,'message':'%s'%message})

class AppRunApiview(APIView):
    def get(self, request, *args, **kwargs):
        appid = str(request.path).split('/')[3]
        Appobj = App.objects.get(id=appid)
        result = Appobj.appdeploy_set.all()
        data = []
        for i in result.all():
            data.append(
                {"id": i.id, "private_ip": i.app_private_ip, "public_ip": i.app_public_ip, "app_hostname": i.app_hostanme}
            )
        res = {
            'code': 200,
            "data": data
        }
        return  Response(res)
    def post(self, request, *args, **kwargs):
        hostname = request.data.get('hostname')
        app_id = request.data.get('app_id')
        appobj = App.objects.get(id=app_id)
        Serverobj = Server.objects.get(hostname=hostname)

        ServerdetailsObj = Serverdetails.objects.get(hostname=hostname)
        sshsftpobj = to_node(
            username=Serverobj.username,
            password=Serverobj.auth_password,
            port=Serverobj.port,
            host=Serverobj.ipaddress,
            auth_type=int(Serverobj.auth_choice),
            key=Serverobj.auth_key
        )
        '''上传部署材料'''
        path = read_config.main('uploadconf')
        lpath = path['app_data_path']
        appdir = os.path.join(lpath,appobj.app_name)
        for file in os.listdir(appdir):
            file_upload = os.path.join(appdir,file)
            sshsftpobj.transport_object_upload(local_path=file_upload,remote_path='/tmp/%s'%file)
        sshsftpobj.to_command_node(command='cd /tmp/ && %s'%appobj.app_deploy)
        sshsftpobj.to_command_node(command='cd /tmp/ && %s' % appobj.app_start)

        AppDeploy.objects.create(
            app_hostanme=ServerdetailsObj.hostname,
            app_public_ip=ServerdetailsObj.public_ip,
            app_private_ip=ServerdetailsObj.private_ip,
        )
        apprunobj = AppDeploy.objects.get(app_hostanme=ServerdetailsObj.hostname)
        apprunobj.app_server.add(appobj)

        res = {
            'code': '200',
            'message': '已部署并且运行成功'
        }
        return Response(res)
'''
{
"id":10,
"app_name":"ftest",
"app_deploy":"ftest install",
"app_start":"ftest run",
"app_stop":"ftest stop",
"fileList":[{"name":"a.md","percentage":100,"status":"success","size":22,"raw":{"uid":1680834944504},"uid":1680834944504,"response":{"code":200,"message":"上传数据成功"}}]}
'''