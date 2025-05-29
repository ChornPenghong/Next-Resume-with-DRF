from django.urls import re_path, path, include
from rest_framework.routers import DefaultRouter 
from .views import LanguageViewSet, SkillViewSet, PositionViewSet, ExperienceViewSet
from . import views

router = DefaultRouter()
router.register(r'languages', LanguageViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'experiences', ExperienceViewSet)

urlpatterns = [
    re_path('login', views.login),
    re_path('register', views.register),
    re_path('user-detail', views.userDetail),
    re_path('update-profile', views.updateProfile),
    re_path('test_token', views.test_token),
    path('', include(router.urls))
]