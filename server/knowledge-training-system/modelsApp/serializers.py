from rest_framework import serializers
from .models import QuestionsList


class QuestionSerializer(serializers.ModelSerializer):
       class Meta:
           model = QuestionsList
           fields = "__all__"

class loginSerializer(serializers.ModelSerializer):
       class Meta:
           model = QuestionsList
           fields = ( 'userId', 'password')