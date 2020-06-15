from django.db import models
from jsonfield import JSONField

# Create your models here.
class QuestionsList(models.Model):
    question = models.CharField(max_length=100)
    questionType = models.IntegerField()
    knowledgePoint = models.CharField(max_length=20)
    difficulty = models.IntegerField()
    options = JSONField()
    answer = models.CharField(max_length=40)
    score = models.IntegerField()