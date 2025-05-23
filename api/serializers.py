from .models import Language, User, Skill
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer): 
    class Meta: 
        model= User
        fields = "__all__"
        
class LanguageSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Language
        fields = "__all__"
        
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"
        