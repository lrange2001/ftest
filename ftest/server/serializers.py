from rest_framework import serializers
from server.models import Group,Server,Serverdetails



class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class ServerSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True,many=True)
    class Meta:
        model = Server
        fields = '__all__'

class ServerdetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serverdetails
        fields = '__all__'

