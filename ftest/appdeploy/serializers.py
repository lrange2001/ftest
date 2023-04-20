from rest_framework import serializers
from appdeploy.models import App,AppDeploy
from server.serializers import ServerSerializer


class AppSerializer(serializers.ModelSerializer):
    server = ServerSerializer(read_only=True,many=True)
    class Meta:
        model = App
        fields = '__all__'

class AppDeploySerializer(serializers.ModelSerializer):
    app_server = ServerSerializer(read_only=True,many=True)
    class Meta:
        model = AppDeploy
        fields = '__all__'