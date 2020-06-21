from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer,loginSerializer
from .models import ExtraUser

from rest_framework import viewsets
from rest_framework import mixins
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from django.contrib.auth import login
from django.contrib.auth import authenticate

from django.shortcuts import render

from django.http import HttpResponse,JsonResponse

from rest_framework import authentication
from rest_framework import exceptions


@api_view(['GET'])
def user_detail(request, identity):
    """
    获取所有老师或者所有学生。
    """
    try:
        user = User.objects.filter(extra__identity=identity)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = loginSerializer(user, many = True)
        return Response(serializer.data)

class UserViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = loginSerializer
   


@swagger_auto_schema(methods=['POST']) #, request_body=loginSerializer    
@api_view(['POST'])
def login(request, username, password):
    #if request.method == 'post':
        #username = request.data['username']
        #password = request.data['password']

        user = User.objects.filter(username = username, password=password).first()
        #extraUser = ExtraUser.objects.filter(theUser_id = user.id).first()
        serializer = loginSerializer(user)#extraUser

        if user is not None:
            return Response(serializer.data)
        else:
            return Response('登录失败 #用户id或密码错误')


'''
#@swagger_auto_schema(methods=['POST'], request_body=loginSerializer) #@api_view(['POST'])
def userLogin(request, username, password):
    #if request.method == 'POST':
        #username = request.data['username']
        #password = request.data['password']
        user = User.objects.get(username = username, password=password)
        #user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            print(user.id)
            request.session['is_login'] = True
            return render(request,context = {"foo": "成功"})
        else:
            return render(request)
'''
'''

@swagger_auto_schema(methods=['POST'], request_body=loginSerializer)
@api_view(['POST'])
def login(request):
    user = User.objects.create_user(username="lee", email='lee@163.com', password=111111)
    user = User.objects.get(username="lee")
    user.extra.phone = 10086100861  # 更改ExtraUser里的字段信息
    user.extra.address = "china"
    user.save()
    
    # 假设下面是用户输入
    phone = 10086100861
    password = 111111
    user = one_to_one_authenticate(phone=phone, password=password)  # 使用自己的authenticate
    if user:
        print(user.username)
    else:
        print("no such user")
    return HttpResponse("one to one successful")
'''


                
