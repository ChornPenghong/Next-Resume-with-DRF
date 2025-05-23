from django.urls import re_path, path, include
from rest_framework.routers import DefaultRouter 
from .views import LanguageViewSet, SkillViewSet
from . import views

router = DefaultRouter()
router.register(r'languages', LanguageViewSet)
router.register(r'skills', SkillViewSet)

urlpatterns = [
    re_path('login', views.login),
    re_path('register', views.register),
    re_path('test_token', views.test_token),
    path('', include(router.urls))
]