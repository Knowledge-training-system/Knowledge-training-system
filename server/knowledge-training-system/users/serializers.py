from rest_framework import serializers
from .models import ExtraUser
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
       class Meta:
        model = User
        fields = "__all__"


class ExtraUserSerializer(serializers.ModelSerializer):
       class Meta:
           model = ExtraUser
           fields = ( 'age', 'name', 'gender', 'identity', 'phonenum')


class loginSerializer(serializers.ModelSerializer):
       extra = ExtraUserSerializer()
       
       def update(self, instance, validated_data):
           """
           print("username" in validated_data)
           if "username" in validated_data: 
               instance.username = validated_data['username']
           if "password" in validated_data: 
               instance.password = validated_data['password']
           if "email" in validated_data: 
               instance.email = validated_data['email']

           #searchResults = QuestionsList.objects.all().filter(knowledgePoint__in = knowledgePointList)
           if "extra" in validated_data: 
               if hasattr(validated_data['extra'],'age'):
                   instance.extra.age = validated_data['extra']['age']
               if hasattr(validated_data["extra"],"name"):
                   instance.extra.name = validated_data["extra"]["name"]
               if hasattr(validated_data['extra'],'gender'):
                   instance.extra.gender = validated_data['extra']['gender']
               if hasattr(validated_data['extra'],'identity'):
                   instance.extra.identity = validated_data['extra']['identity']
               if hasattr(validated_data['extra'],'phonenum'):
                   instance.extra.phonenum = validated_data['extra']['phonenum']
           """

           #print("username" in validated_data)
           #print('!!!!!!!!!!!!!!')
           instance.username = validated_data['username']
           instance.password = validated_data['password']
           instance.email = validated_data['email']
           instance.extra.age = validated_data['extra']['age']
           instance.extra.name = validated_data['extra']['name']
           instance.extra.gender = validated_data['extra']['gender']
           instance.extra.identity = validated_data['extra']['identity']
           instance.extra.phonenum = validated_data['extra']['phonenum']
           
           instance.save()
           return instance 
       
           
       class Meta:
           model = User
           fields = ( 'username', 'password', 'email', 'extra', 'id') #这里是自带用户表中的id

"""
class UserSerializer(serializers.ModelSerializer):
       class Meta:
           model = ExtraUser
           fields = ('username', 'password' )


class loginSerializer(serializers.ModelSerializer):
       theUser = UserSerializer(read_only = True)
       class Meta:
           model = ExtraUser
           fields = ( 'age', 'name', 'gender', 'identity', 'theUser')
"""

