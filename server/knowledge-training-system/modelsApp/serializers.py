from rest_framework import serializers
from .models import QuestionsList
from modelsApp.models import Paper
from django.contrib.auth.models import User
from users.serializers import UserSerializer


knowledgePoints=['毛泽东思想','新民主主义革命理论','社会主义改造理论','社会主义建设道路初步探索理论成果','邓小平理论']#,'三个代表重要思想','科学发展观','习近平新时代思想','中特社总任务','五位一体总体布局']
knowledgeChoices=[(i,i) for i in knowledgePoints]
questionTypes=['单选题','多选题','填空题','判断题']
questionTypesChoices=[(i,i) for i in [0,1,2,3]]
#knowledgeChoices=[(i,i) for i in range(1, 192)]
class QuestionSerializer(serializers.ModelSerializer):
       class Meta:
           model = QuestionsList
           fields = "__all__"


class releaseExaminationSerializer(serializers.Serializer):#.ModelSerializer
    AllUser = User.objects.all()
    Userdata = []
    Userdata = UserSerializer(AllUser, many=True).data
    UserChoices = []
    for user in Userdata:
        if user['username'][0]=='0': #选取所有学生的username
            UserChoices.append((user['id'], user['id']))
    
    releaseTeacherId = serializers.IntegerField()
    knowledgePointList = serializers.MultipleChoiceField(choices = knowledgeChoices)
    questionTypeList = serializers.MultipleChoiceField(choices = questionTypesChoices)
    questionNumber0 = serializers.IntegerField()
    questionNumber1 = serializers.IntegerField()
    questionNumber2 = serializers.IntegerField()
    questionNumber3 = serializers.IntegerField()
    averageDifficulty = serializers.IntegerField(max_value=8, min_value=3)
    studentIdList = serializers.MultipleChoiceField(choices = UserChoices)
    submitStartTime = serializers.DateTimeField()
    submitEndTime = serializers.DateTimeField()
    #class Meta:


class PaperSerializer(serializers.ModelSerializer):
       class Meta:
           model = Paper
           fields = "__all__"
#class getUserPaperSerializer(serializers.Serializer, ):


class submitPaperAnswerSerializer(serializers.Serializer):
    submitAnswerList = serializers.JSONField()
    #class Meta:


"""
{
  "releaseTeacherId": 7,
  "knowledgePointList": [
    "毛泽东思想"
  ],
  "questionTypeList": [
    0,1
  ],
  "questionNumber0": 12,
  "questionNumber1": 13,
  "questionNumber2": 14,
  "questionNumber3": 15,
  "averageDifficulty": 4,
  "studentIdList": [
   6,8
  ],
  "submitStartTime": "2020-06-20T10:15:22.839Z",
  "submitEndTime": "2020-06-20T10:15:22.839Z"
}
"""
    