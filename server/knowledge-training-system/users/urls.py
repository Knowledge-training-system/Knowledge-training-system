from . import views
from django.urls import path


urlpatterns = [
    path('teacher/<str:identity>/',views.user_detail),
    path('login/<str:userId>/<int:pwd>/',views.login)
]