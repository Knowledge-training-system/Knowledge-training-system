from django.db import models


class User(models.Model):
    userId = models.CharField(max_length=20,primary_key = True)
    password = models.IntegerField()
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=5)
    age = models.IntegerField()
    identity = models.CharField(max_length=20)
    phonenum =models.CharField(max_length=20)
    email = models.EmailField()

    class Meta:
        db_table = 'users'