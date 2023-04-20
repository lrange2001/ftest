from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password
from log.logserver import outputLog


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            res = {
                "token": token.key,
                "code": 200,
                "message": "登录成功"
            }
        else:
            res = {
                "code": 502,
                # 'message': '认证失败:%s'%serializer.errors['non_field_errors'][0]
                "message": "认证失败"
            }
        return Response(res)


class UpdatePassword(APIView):
    def post(self, request):
        username = request.data.get('username')
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        end_password = request.data.get('end_password')

        if new_password == end_password:
            new_make_password = make_password(new_password)
        else:
            resp = {"code": 500,"message": "两次密码不同"}
            outputLog(logger_name='server').info('%s修改密码错误 服务端返回%s'%(username,resp))
            return Response(resp)

        user = User.objects.filter(username=username)
        if not user.exists():
            resp = {'code': 404,'message':'用户不存在'}
            outputLog(logger_name='server').info('%s修改密码错误 服务端返回%s'%(username,resp))
            return Response(resp)
        userobj = User.objects.get(username=username)
        if check_password(old_password,userobj.password):
            userobj.password = new_make_password
            userobj.save()
            resp = {'code': 200,'message': '修改密码成功'}
            outputLog(logger_name='server').info('%s修改密码成功 服务端返回%s'%(username,resp))
        else:
            resp = {'code': 500,'message': '密码不正确'}
            outputLog(logger_name='server').info('%s修改密码错误 服务端返回%s'%(username,resp))
        return Response(resp)
