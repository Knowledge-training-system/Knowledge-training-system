from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User
import os
import sys
#from users.models import User

from django.contrib.auth import get_user_model
print(get_user_model())

knowledgePoints=['毛泽东思想','新民主主义革命理论','社会主义改造理论','社会主义建设道路初步探索理论成果','邓小平理论']#,'三个代表重要思想','科学发展观','习近平新时代思想','中特社总任务','五位一体总体布局']
difficultyChoices=[(i,i) for i in range(3,8)]
questionTypeChoices=[(i,i) for i in range(0,4)]
knowledgePointsChoices=[(i,i) for i in knowledgePoints]

# Create your models here.
class QuestionsList(models.Model):
    questionId = models.AutoField(primary_key=True)
    question = models.CharField(max_length=200)
    questionType = models.IntegerField(choices=questionTypeChoices, default=0)
    knowledgePoint = models.CharField(choices=knowledgePointsChoices, max_length=40)
    difficulty = models.IntegerField(choices=difficultyChoices)
    options = JSONField()
    answer = JSONField() #models.CharField(max_length=40)
    score = models.IntegerField()
    
    class Meta:
        db_table = 'questionslist'


def JSONdefault1():
    return [1,1,1,1]

class Paper(models.Model):
    paperId = models.AutoField(primary_key=True)
    QIdList = JSONField()  #问题id列表
    questionNumberList = JSONField(default=JSONdefault1)  #各有多少题
    #answerList = JSONField(null = True)
    
                                                                                    #SET_DEFAULT
    releaseTeacherId = models.IntegerField()#models.ForeignKey('auth.User', to_field='id', on_delete = models.CASCADE, related_name='releaseTeacherId_user') #发布老师的ID
    studentId = models.IntegerField()#models.ForeignKey('auth.User', to_field='id', on_delete = models.CASCADE, related_name='studentId_user')
    releaseTime = models.DateTimeField(auto_now_add=True)  #发布时间
    submitStartTime = models.DateTimeField(default='2000-01-01 00:00')  #开始能提交时间
    submitEndTime = models.DateTimeField(default='2000-01-01 00:00')  #截止提交时间
    
    submitTime = models.DateTimeField(null = True)  #学生提交时间
    submitAnswerList = JSONField()  #学生提交的答案列表
    maxScore = models.IntegerField(null = True)
    score = models.IntegerField(null = True)
    submitted = models.BooleanField(default=0) #该试卷已提交

    
    class Meta:
        db_table = 'Papers'


