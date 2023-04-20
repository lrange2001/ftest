from django.shortcuts import render
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from server.models import Group,Server,Serverdetails
from server.serializers import  ServerSerializer,GroupSerializer,ServerdetailsSerializer
# Create your views here.
from server.other.get_node import to_node
import os
from ftest.settings import BASE_DIR
from log.logserver import outputLog
from rest_framework import  filters
import json
from server.other.register_serverinfoTodb import get_serverdetails

class GroupView(ModelViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ServerView(ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            res = {'code':200,'message':'创建成功'}
            return Response(res)
        else:
            res = {'code':500,'message':serializer.errors}
            return Response(res)
class ServerdetailsView(ModelViewSet):
    queryset = Serverdetails.objects.all()
    serializer_class = ServerdetailsSerializer

    filter_backends = [filters.SearchFilter,filters.OrderingFilter] #指定django默认的过滤器
    search_fields = ('hostname',)



'''采集主机'''
class gather_node(APIView):
    def get(self,request,*args,**kwargs):
        gather_node_data = Serverdetails.objects.all()
        result = ServerdetailsSerializer(gather_node_data,many=True)
        message = {
            'code': 200,
            'data': result.data,
        }
        return Response(message)
    def post(self, request, *args, **kwargs):
        hostname = request.data.get('hostname')
        if not hostname:
            message = {"code": 404,"message": "请提供hostname字段"}
            outputLog(logger_name='server').warning('%s同步服务器 服务端返回%s' % (hostname, message))
            return Response(message)
        if  not Server.objects.filter(hostname=hostname).exists():
            message = {'code': 404,'message': "未找到相关主机"}
            outputLog(logger_name='server').debug('%s同步服务器 服务端返回%s' % (hostname, message))
            return Response(message)
        else:
            result = Server.objects.get(hostname=hostname)
            sftpobj = to_node(
                username=result.username,
                port=result.port,
                auth_type=int(result.auth_choice),
                password=result.auth_password,
                key=result.auth_key,
                host=result.ipaddress
                )
            serverdir  = os.path.join(BASE_DIR,'server')
            scriptspath = os.path.join(serverdir,'other')
            getnodescriptpath = os.path.join(scriptspath,'python_node_exporter.py')
            remotepath = '/tmp/python_node_exporter.py'
            try:
                sftpobj.transport_object_upload(local_path=getnodescriptpath,remote_path=remotepath)
            except Exception as f:
                try:
                    res = {'code':500,'message':'%s'%f}
                    Serverdetails.objects.create(hostname=hostname)
                    return Response(res)
                except Exception as t:
                    res = {'code': 500, 'message': '%s' % t}
                    return Response(res)


            data = sftpobj.to_command_node('python /tmp/python_node_exporter.py')
            if len(data['stderr']) < 1:
                data = data['stdout']
                data = data.decode('utf-8')
                getServerDetails = get_serverdetails(data)
                message = {'code': getServerDetails['code'],'message':getServerDetails['message'],}
                outputLog(logger_name='server').info('%s同步服务器 服务端返回%s' % (hostname, message))
            else:
                data = data['stderr']
                message = {'code': 503,'message': '采集失败'}
                outputLog(logger_name='server').info('%s同步服务器 服务端返回%s' % (hostname, message))
            return Response(message)
class One_click_synchronization(APIView):
    def get(self,request):
        serverobj = Server.objects.all()
        from django.core import serializers
        syncdata = serializers.serialize('json',serverobj)
        syncdata = json.loads(syncdata)
        hostlist = []
        res_error = {'code':500}
        error = False
        error_list = []
        res = {'code':200,'message':'全部同步完成'}
        for sync in syncdata:
            hostlist.append(sync['fields']['hostname'])
        for hostname in hostlist:
            result = Server.objects.get(hostname=hostname)
            sftpobj = to_node(
                username=result.username,
                port=result.port,
                auth_type=int(result.auth_choice),
                password=result.auth_password,
                key=result.auth_key,
                host=result.ipaddress
                )
            serverdir  = os.path.join(BASE_DIR,'server')
            scriptspath = os.path.join(serverdir,'other')
            getnodescriptpath = os.path.join(scriptspath,'python_node_exporter.py')
            remotepath = '/tmp/python_node_exporter.py'
            try:
                sftpobj.transport_object_upload(local_path=getnodescriptpath,remote_path=remotepath)
                data = sftpobj.to_command_node('python /tmp/python_node_exporter.py')
                data = data['stdout']
                data = data.decode('utf-8')
                get_serverdetails(data)
            except Exception as f:
                error = True
                error_list.append('%s同步失败,错误:%s'%(hostname,f))
                res_error.update({
                    "message": error_list
                })
        if error:
            return Response(res_error)
        else:
            return Response(res)


# def delete_node(request):
#     if request.method == 'POST':
#         print(request)
#         delete_hostname = request.POST.get('hostname')
#         serverobj = Server.objects.filter(hostname=delete_hostname)
#         serverobj.delete()
#         res = {'code':200,'message':'删除成功'}
#         return JsonResponse(res)
#     else:
#         return JsonResponse({'code':404,'message':'method must be POST'})
'''删除/查询/修改 主机 由于是主机名非ID 不遵循restful风格  单独逻辑'''
class NodeSX(APIView):
    def get(self,request,*args,**kwargs):
        path = request.path
        path_vals = path.split('/')
        key = path_vals[-2]
        serverobj = Server.objects.filter(hostname=key)
        from django.core import serializers
        json_data = serializers.serialize('json',serverobj)
        json_data = json.loads(json_data)
        result_data = json_data[0]['fields']
        return Response({'code':200,'data':result_data})
    def post(self, request, *args, **kwargs):
        delete_hostname = request.data.get('hostname')
        serverobj = Server.objects.filter(hostname=delete_hostname)
        serverobj.delete()
        res = {'code':200,'message':'删除成功'}
        return Response(res)


class UpdateNode(APIView):
    def post(self,request, *args, **kwargs):
        serobj = Server.objects.filter(hostname=request.data.get('hostname'))
        serobj.update(
            ipaddress=request.data.get('ipaddress'),
            username=request.data.get('username'),
            auth_choice=request.data.get('auth_choice'),
            auth_password=request.data.get('auth_password'),
            auth_key=request.data.get('auth_key'),
            port=request.data.get('port')
        )
        res = {'code':200,'message':'修改成功'}
        return Response(res)



