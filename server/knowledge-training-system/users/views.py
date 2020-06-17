from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer,loginSerializer
from rest_framework import viewsets
from rest_framework import mixins
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView


@api_view(['GET'])
def user_detail(request, identity):
    """
    获取所有老师或者所有学生。
    """
    try:
        snippets = User.objects.filter(identity=identity)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(snippets, many = True)
        return Response(serializer.data)

class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
   
   
'''
@swagger_auto_schema(methods=['POST'], request_body=loginSerializer)
@api_view(['POST'])
def login(request):
    if request.method == 'post':
        userId = request.data['userId']
        password = request.data['password']
        print(userId)
        print(password)
        #user = User.objects.filter(userId = userId, password=password)
        user = User.objects.get(userId = userId)
        if user:
            if user.password == password:
                return Response('密码错误')
            else:
                return Response('登录成功')
        else:
            return Response('用户id错误')
'''


@api_view(['GET'])
def login(request, userId,pwd):
    """
    用户登录验证
    """
    try:
        user = User.objects.filter(userId=userId,password=pwd)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if user:
            return Response('登录成功')
        else:
            return Response('用户id或密码错误')
