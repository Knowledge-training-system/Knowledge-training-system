# Generated by Django 3.0.7 on 2020-06-16 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelsApp', '0003_auto_20200617_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionslist',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]