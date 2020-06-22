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

from modelsApp.models import QuestionsList
from modelsApp.models import Paper
from modelsApp.serializers import QuestionSerializer
from modelsApp.serializers import releaseExaminationSerializer
from modelsApp.serializers import PaperSerializer
from modelsApp.serializers import submitPaperAnswerSerializer
from users.models import ExtraUser

import random
import ast
from django.utils import timezone

"""
@api_view(['GET'])
def getQa(request, questionId):
    questions = QuestionsList.objects.all()   
    Q = QuestionsList.objects.get(id=questionId)
    questions_serializer = QuestionSerializer(Q)
    print(questions_serializer.data['options'])
    return Response(data = questions_serializer.data) 


@api_view(['GET'])
def deleteQuestion(request, Qid):
    #id=request.data['qid']
    try:
        
        Q.delete()
    except QuestionsList.DoesNotExist:
        return Response(data = f'未找到序号为{Qid}的问题', status=status.HTTP_404_NOT_FOUND)

    return Response(data = '删除成功') 
"""


class QuestionViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,mixins.DestroyModelMixin, mixins.UpdateModelMixin,viewsets.GenericViewSet):
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


@swagger_auto_schema(methods=['POST'],  request_body=releaseExaminationSerializer)
@api_view(['POST'])
def releaseExamination(request):
    request.encoding='utf-8'
    releaseTeacherId = request.data['releaseTeacherId'] #.username
    knowledgePointList = request.data['knowledgePointList']
    #questionTypeList = request.data['questionTypeList']
    questionNumber0 = request.data['questionNumber0']
    questionNumber1 = request.data['questionNumber1']
    questionNumber2 = request.data['questionNumber2']
    questionNumber3 = request.data['questionNumber3']

    averageDifficulty = request.data['averageDifficulty']
    studentIdList = request.data['studentIdList']
    submitStartTime = request.data['submitStartTime']
    submitEndTime = request.data['submitEndTime']


    searchResults = QuestionsList.objects.all().filter(knowledgePoint__in = knowledgePointList)   
    searchResults = searchResults.filter(difficulty__gte = averageDifficulty - 2 )
    searchResults = searchResults.filter(difficulty__lte = averageDifficulty + 2 )

    searchResults0 = searchResults.filter(questionType = 0)  #questionType__in = questionTypeList
    searchResults1 = searchResults.filter(questionType = 1)
    searchResults2 = searchResults.filter(questionType = 2)
    searchResults3 = searchResults.filter(questionType = 3)
    questions_serializer0 = QuestionSerializer(searchResults0, many=True)
    questions_serializer1 = QuestionSerializer(searchResults1, many=True)
    questions_serializer2 = QuestionSerializer(searchResults2, many=True)
    questions_serializer3 = QuestionSerializer(searchResults3, many=True)
    QIdList0 = [Q['questionId'] for Q in questions_serializer0.data]
    QIdList1 = [Q['questionId'] for Q in questions_serializer1.data]
    QIdList2 = [Q['questionId'] for Q in questions_serializer2.data]
    QIdList3 = [Q['questionId'] for Q in questions_serializer3.data]

    #students = User.objects.all().filter(studentId__in = studentIdList)   
    #students_serializer = UserSerializer(students, many=True)
    if questionNumber0 > len(QIdList0):
        questionNumber0 = len(QIdList0)
    if questionNumber1 > len(QIdList1):
        questionNumber1 = len(QIdList1)
    if questionNumber2 > len(QIdList2):
        questionNumber2 = len(QIdList2)
    if questionNumber3 > len(QIdList3):
        questionNumber3 = len(QIdList3)
    questionNumberList = [questionNumber0, questionNumber1, questionNumber2, questionNumber3]
    
    k = -1
    for studentId in studentIdList:
        k += 1
        QIdList = random.sample(QIdList0, questionNumber0) + random.sample(QIdList1, questionNumber1) + random.sample(QIdList2, questionNumber2) + random.sample(QIdList3, questionNumber3) 
        maxScore = 0
        for QId in QIdList:
            maxScore += QuestionsList.objects.get(questionId = QId).score
        paper1 = Paper(studentId = studentId, QIdList = QIdList, releaseTeacherId = releaseTeacherId, submitStartTime = submitStartTime, submitEndTime = submitEndTime, questionNumberList = questionNumberList, maxScore = maxScore)
        paper1.save()
        if k==0:
            firstPaperId = paper1.paperId
    
    data={}
    data['releasePaperNumber'] = len(studentIdList)

    thePaper = PaperSerializer(Paper.objects.get(paperId = firstPaperId)).data
    data['firstPaperId'] = thePaper['paperId']
    data['submitted'] = thePaper['submitted']
    data['maxScore'] = thePaper['maxScore']
    submitted = thePaper['submitted']
    data['submitStartTime'] = thePaper['submitStartTime']
    data['submitEndTime'] = thePaper['submitEndTime']
    data['questions'] = []
    PaperData = PaperSerializer(thePaper).data
    pos = -1
    #if submitted!=1:
    for i in range(4):
        for j in range(ast.literal_eval(PaperData['questionNumberList'])[i]):
            pos += 1
            QId = ast.literal_eval(PaperData['QIdList'])[pos]
            aQuestionData = QuestionSerializer(QuestionsList.objects.get(questionId = QId)).data
            aQuestionData['options'] = ast.literal_eval(aQuestionData['options'])
            aQuestionData['trueAnswer'] = ast.literal_eval(aQuestionData['answer'])
            del aQuestionData['answer']
            
                #aQuestionData['trueAnswer'] = ''
            #[['A'],['A'],['A'], ['A'],['A'],['A'],['A'],['A'],['A'], ['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A']]
            #[ ['民族','a'],['A'],['A'],['民族'],['A'],['A'],['A'],['A'],['A'], ['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A']]
            data['questions'].append(aQuestionData)
    return Response(data = data) 


@api_view(['GET'])
def getUserAllPaper(request, userId):
    UserAllPaper = Paper.objects.all().filter(studentId = userId)
    
    data=[]
    PaperData = PaperSerializer(UserAllPaper, many=True).data
    for paper in PaperData:
        aPaperDict = {}
        aPaperDict['paperId'] = paper['paperId']
        aPaperDict['submitted'] = paper['submitted']  #是否已提交
        sum = 0
        for Num in ast.literal_eval(paper['questionNumberList']):
            #print(Num)
            sum += Num
        
        aPaperDict['questionTotalNumber'] = sum #总题数
        
        aPaperDict['score'] = paper['score']
        aPaperDict['teacherId'] = paper['releaseTeacherId']
        aPaperDict['maxScore'] = paper['maxScore']
        aPaperDict['submitTime'] = paper['submitTime']
        aPaperDict['submitStartTime'] = paper['submitStartTime']
        aPaperDict['submitEndTime'] = paper['submitEndTime']
        data.append(aPaperDict)
    return Response(data = data)  


@api_view(['GET'])
def getTeacherAllPaper(request, userId):
    UserAllPaper = Paper.objects.all().filter(releaseTeacherId = userId)
    data=[]
    PaperData = PaperSerializer(UserAllPaper, many=True).data
    for paper in PaperData:
        aPaperDict = {}
        aPaperDict['paperId'] = paper['paperId']
        aPaperDict['submitted'] = paper['submitted']  #是否已提交
        sum = 0
        for Num in ast.literal_eval(paper['questionNumberList']):
            #print(Num)
            sum += Num
        
        aPaperDict['questionTotalNumber'] = sum #总题数
        
        aPaperDict['score'] = paper['score']
        aPaperDict['studentId'] = paper['studentId']
        aPaperDict['submitTime'] = paper['submitTime']
        aPaperDict['maxScore'] = paper['maxScore']
        aPaperDict['submitStartTime'] = paper['submitStartTime']
        aPaperDict['submitEndTime'] = paper['submitEndTime']
        data.append(aPaperDict)
    return Response(data = data)  


@api_view(['GET'])
def getPaperDetail(request, paperId):
    thePaper = PaperSerializer(Paper.objects.get(paperId = paperId)).data
    data={}
    data['paperId'] = thePaper['paperId']
    data['submitted'] = thePaper['submitted']
    submitted = thePaper['submitted']
    data['submitStartTime'] = thePaper['submitStartTime']
    data['submitEndTime'] = thePaper['submitEndTime']
    data['submitAnswerList'] = thePaper['submitAnswerList']
    data['questions'] = []
    PaperData = PaperSerializer(thePaper).data
    pos = -1
    
    for i in range(4):
        for j in range(ast.literal_eval(PaperData['questionNumberList'])[i]):
            pos += 1
            QId = ast.literal_eval(PaperData['QIdList'])[pos]
            aQuestionData = QuestionSerializer(QuestionsList.objects.get(questionId = QId)).data
            aQuestionData['options'] = ast.literal_eval(aQuestionData['options'])
            aQuestionData['trueAnswer'] = ast.literal_eval(aQuestionData['answer'])

            if thePaper['submitAnswerList']:
                aQuestionData['submittedAnswer'] = ast.literal_eval(thePaper['submitAnswerList'])[pos]#
            else:
                aQuestionData['submittedAnswer'] = None

            del aQuestionData['answer']
            
            if submitted==1:
                questionJudgeList = []
                for k in range(len(aQuestionData['trueAnswer'])):
                    if aQuestionData['trueAnswer'][k]==ast.literal_eval(thePaper['submitAnswerList'])[pos][k]:
                        questionJudgeList.append(1) 
                    else:
                        questionJudgeList.append(0)
                aQuestionData['judge']=questionJudgeList
            if submitted==0:
                pass
                #aQuestionData['trueAnswer'] = ''
            #[['A'],['A'],['A'], ['A'],['A'],['A'],['A'],['A'],['A'], ['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A']]
            #[ ['民族','a'],['A'],['A'],['民族'],['A'],['A'],['A'],['A'],['A'], ['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A'],['A']]
            data['questions'].append(aQuestionData)


    return Response(data = data)  


@swagger_auto_schema(methods=['POST'],  request_body=submitPaperAnswerSerializer)
@api_view(['POST'])
def submitPaperAnswer(request, paperId):
    thePaper = Paper.objects.get(paperId = paperId)
    now = timezone.now()
    #print(now)
    if now > thePaper.submitEndTime or now < thePaper.submitStartTime:
        return Response(data = f'提交失败！不在规定时间范围内')  
    
    submitAnswerList = request.data['submitAnswerList'] #ast.literal_eval(
    QIdList = thePaper.QIdList #ast.literal_eval(
    thePaper.submitAnswerList = submitAnswerList
    thePaper.submitted = 1
    thePaper.submitTime = now
    
    score = 0
    for i in range(len(QIdList)):
        QId = QIdList[i]
        aQuestionData = QuestionSerializer(QuestionsList.objects.get(questionId = QId)).data
        trueAnswer = ast.literal_eval(aQuestionData['answer'])
        for k in range(len(trueAnswer)):
            if trueAnswer[k]==submitAnswerList[i][k]: #回答正确
                if aQuestionData['questionType']!=2: #如果不是填空题
                    score += aQuestionData['score']
                else:
                    score += 2
    thePaper.score = score
    thePaper.save()
    data = {}
    data['submitAnswerNumber'] = len(thePaper.submitAnswerList)
    data['score'] = thePaper.score
    data['maxScore'] = thePaper.maxScore
    return Response(data = data) 
    

"""
{
  "submitAnswerList": [ ["民族"],["A"],["A"],["民族"],["A"],["A"],["A"],["A"],["A"], ["A"],["A"],["A"],["A"],["A"],["A"],["A"],["A"],["A"],["A"],["A"],["A"],["A"],["A"],["A"],["A"],["A"]]
}
"""
"""测试
{
  "knowledgePointList": [
    "毛泽东思想"
  ],
  "questionTypeList": [
    "单选题"
  ],
  "questionNumber": 0,
  "averageDifficulty": 5,
  "studentIdList": [
    "000004",'000005','000011'
  ]
}
"""
    
