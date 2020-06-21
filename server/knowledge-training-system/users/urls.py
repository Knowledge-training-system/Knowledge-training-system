from . import views
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('teacher/<str:identity>/',views.user_detail),
    path('login/<str:username>/<str:password>/',views.login), #login
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
]