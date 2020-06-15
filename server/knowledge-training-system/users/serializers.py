from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
       class Meta:
        model = User
        fields = ( 'userId', 'password', 'name', 'gender', 'age', 'identity', 'phonenum', 'email')

class loginSerializer(serializers.ModelSerializer):
       class Meta:
        model = User
        fields = ( 'userId', 'password')