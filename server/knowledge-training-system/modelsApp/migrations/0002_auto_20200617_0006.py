# Generated by Django 3.0.7 on 2020-06-16 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelsApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionslist',
            name='difficulty',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)]),
        ),
        migrations.AlterField(
            model_name='questionslist',
            name='knowledgePoint',
            field=models.CharField(choices=[('毛泽东思想', '毛泽东思想'), ('新民主主义革命理论', '新民主主义革命理论'), ('社会主义改造理论', '社会主义改造理论'), ('社会主义建设道路初步探索理论成果', '社会主义建设道路初步探索理论成果'), ('邓小平理论', '邓小平理论')], max_length=40),
        ),
        migrations.AlterField(
            model_name='questionslist',
            name='question',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='questionslist',
            name='questionType',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3)], default=0),
        ),
        migrations.AlterModelTable(
            name='questionslist',
            table='modelsapp_questionslist',
        ),
    ]