from rest_framework import serializers
from .models import Language, User, Skill, UserProfile, UserPosition, userExperience, Institute, UserEducation, UserLanguage, UserReference

class UserSerializer(serializers.ModelSerializer): 
    class Meta: 
        model= User
        exclude = ['password', 'groups', 'user_permissions']
        
class UserProfileSerializer(serializers.ModelSerializer): 
    user = UserSerializer(read_only=True)
    class Meta: 
        model= UserProfile
        fields = [
            'id',
            'full_name',
            'email',
            'phone',
            'address',
            'description',
            'linkedin',
            'github',
            'website',
            'user', 
        ]
        
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
        
class UserPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPosition
        fields = ['id', 'name']
        
class ExperienceSerializer(serializers.ModelSerializer):
    position = UserPositionSerializer(read_only=True)
    user_profile = UserProfileSerializer(read_only=True)
    
    position_id = serializers.PrimaryKeyRelatedField(
        queryset=UserPosition.objects.all(),
        write_only=True
    )
    
    class Meta:
        model = userExperience
        fields = '__all__'
        
    def create(self, validated_data):
        position = validated_data.pop('position_id')
        experience = userExperience.objects.create(position=position, **validated_data)
        return experience

class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = '__all__'
        
class UserEducationSerializer(serializers.ModelSerializer):
    institute = InstituteSerializer(read_only=True)
    user_profile = UserProfileSerializer(read_only=True)
    institute_id = serializers.PrimaryKeyRelatedField(
        queryset=Institute.objects.all(),
        write_only=True
    )
    class Meta:
        model = UserEducation
        fields = '__all__'
        
    def create(self, validated_data):
        institute = validated_data.pop('institute_id')
        education = UserEducation.objects.create(institute=institute, **validated_data)
        return education
    
class UserLangaugeSerializer(serializers.ModelSerializer):
    language = LanguageSerializer(read_only=True)
    user_profile = UserProfileSerializer(read_only=True)
    
    language_id = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(),
        write_only=True
    )
    class Meta:
        model = UserLanguage
        fields = '__all__'
        
    def create(self, validated_data):
        language = validated_data.pop('language_id')
        language = UserLanguage.objects.create(language=language, **validated_data)
        return language

    def update(self, instance, validated_data):
        language = validated_data.pop('language_id', None)
        if language is not None:
            instance.language = language

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class UserReferenceSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(read_only=True)
    class Meta:
        model = UserReference
        fields = '__all__'