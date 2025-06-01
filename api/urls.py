from . import views
from django.urls import re_path, path, include
from rest_framework.routers import DefaultRouter 
from .views import LanguageViewSet, SkillViewSet, PositionViewSet, ExperienceViewSet, InstituteViewSet, UserEducationViewSet, UserLanguageViewSet, UserReferenceViewSet

router = DefaultRouter()
router.register(r'languages', LanguageViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'experiences', ExperienceViewSet)
router.register(r'institutes', InstituteViewSet)
router.register(r'educations', UserEducationViewSet)
router.register(r'user-languages', UserLanguageViewSet)
router.register(r'user-references', UserReferenceViewSet)

urlpatterns = [
    re_path('login', views.login),
    re_path('register', views.register),
    re_path('user-detail', views.userDetail),
    re_path('update-profile', views.updateProfile),
    re_path('test_token', views.test_token),
    path('', include(router.urls))
]
