from .models import Language, User, Skill, UserProfile
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer): 
    class Meta: 
        model= User
        fields = "__all__"
        
class UserProlfileSerializer(serializers.ModelSerializer): 
    class Meta: 
        model= UserProfile
        fields = "__all__"
        
class LanguageSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Language
        fields = "__all__"
        
class SkillSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S %p", read_only=True)
    updated_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S %p", read_only=True)
    class Meta:
        model = Skill
        fields = "__all__"
        