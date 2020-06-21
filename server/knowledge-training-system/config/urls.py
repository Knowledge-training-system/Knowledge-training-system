from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include
from rest_framework import  routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from users import views as users_views
from modelsApp import views as modelsApp_views


router = routers.DefaultRouter()
router.register('users', users_views.UserViewSet)
router.register('AllQuestions', modelsApp_views.QuestionViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v1',
      description="所有view",
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # 配置django-rest-framwork API路由
    path('', include(router.urls)),
    path('users/', include('users.urls')),
    
    #教师端管理题库问题相关url
    path('AllQuestions/searchQuestion/<str:questionType>/<str:knowledgePoint>/<str:difficulty>', modelsApp_views.searchQuestion),
    path('AllQuestions/releaseExamination', modelsApp_views.releaseExamination), 
    path('Teacher/<int:userId>/AllPaper', modelsApp_views.getTeacherAllPaper),
    
    #学生端答卷相关url
    path('Student/<int:userId>/AllPaper', modelsApp_views.getUserAllPaper), 
    path('Student/PaperDetail/<int:paperId>', modelsApp_views.getPaperDetail), 
    path('Student/submitPaperAnswer/<int:paperId>', modelsApp_views.submitPaperAnswer),
    

    # 配置drf-yasg路由
    #path('^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
