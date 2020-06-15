from django.conf.urls import url
from django.urls import path
 
from . import views
 
urlpatterns = [
    url(r'^$', views.addQuestion),
    path('getAllQuestions/', views.getAllQuestions),
    path('getAllQuestions/searchQuestion/', views.searchQuestion),
    path('getAllQuestions/addQuestion/', views.addQuestion),
    path('getAllQuestions/deleteQuestion/', views.deleteQuestion),
]
