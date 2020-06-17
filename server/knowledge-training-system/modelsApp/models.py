from django.db import models
from jsonfield import JSONField

knowledgePoints=['毛泽东思想','新民主主义革命理论','社会主义改造理论','社会主义建设道路初步探索理论成果','邓小平理论']#,'三个代表重要思想','科学发展观','习近平新时代思想','中特社总任务','五位一体总体布局']
difficultyChoices=[(i,i) for i in range(1,10)]
questionTypeChoices=[(i,i) for i in range(0,4)]
knowledgePointsChoices=[(i,i) for i in knowledgePoints]

# Create your models here.
class QuestionsList(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=200)
    questionType = models.IntegerField(choices=questionTypeChoices, default=0)
    knowledgePoint = models.CharField(choices=knowledgePointsChoices, max_length=40)
    difficulty = models.IntegerField(choices=difficultyChoices)
    options = JSONField()
    answer = JSONField() #models.CharField(max_length=40)
    score = models.IntegerField()
    
    class Meta:
        db_table = 'questionslist'