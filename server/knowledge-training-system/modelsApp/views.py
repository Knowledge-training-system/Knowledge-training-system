from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
from django.core import serializers

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view

from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import QuestionsList
from .serializers import QuestionSerializer
"""
@api_view(['GET'])
def getAllQuestions(request):
    questions = QuestionsList.objects.all()   
    questions_serializer = QuestionSerializer(questions, many=True)
    return Response(data = questions_serializer.data) 


@api_view(['GET'])
def deleteQuestion(request, Qid):
    #id=request.data['qid']
    try:
        Q = QuestionsList.objects.get(id=Qid)
        Q.delete()
    except QuestionsList.DoesNotExist:
        return Response(data = f'未找到序号为{Qid}的问题', status=status.HTTP_404_NOT_FOUND)

    return Response(data = '删除成功') 
"""


class QuestionViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,mixins.DestroyModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,viewsets.GenericViewSet):
    queryset = QuestionsList.objects.all()
    serializer_class = QuestionSerializer


@api_view(['GET'])
def searchQuestion(request, questionType, knowledgePoint, difficulty):
    request.encoding='utf-8'
    searchResults = QuestionsList.objects.all()   
    questionTypes=['单选题','多选题','填空题','判断题'] #questionTypes.index(
    if questionType!='全部':
        searchResults = searchResults.filter(questionType=questionTypes.index(questionType))   

    knowledgePoints=['毛泽东思想','新民主主义革命理论','社会主义改造理论','社会主义建设道路初步探索理论成果','邓小平理论']#,'三个代表重要思想','科学发展观','习近平新时代思想','中特社总任务','五位一体总体布局']
    if knowledgePoint!='全部':
        searchResults = searchResults.filter(knowledgePoint=knowledgePoint)

    if difficulty!='全部':
        if difficulty=='易':
            searchResults = searchResults.filter(difficulty__lt=5) #小于   #<input type="radio" name="difficulty"> #单选按钮
        elif difficulty=='难':
            searchResults = searchResults.filter(difficulty__gte=5) #大于等于

    questions_serializer = QuestionSerializer(searchResults, many=True)
    return Response(data = questions_serializer.data) 


def releaseExamination(request):
    request.encoding='utf-8'
    knowledgePointList=request.GET['knowledgePointList']
    questionTypeList=request.GET['questionTypeList']
    questionNumber=request.GET['questionNumber']
    averageDifficulty=request.GET['averageDifficulty']

    context={}
    return render(request, 'testHtml.html', context)
    
