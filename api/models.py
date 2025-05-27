from django.db import models
from django.contrib.auth.models import User

class TimeStampsModel(models.Model): 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

class UserProfile(TimeStampsModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    description = models.TextField()
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    website = models.URLField(blank=True)
    
    def __str__(self):
        return self.full_name

class UserPosition(TimeStampsModel):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class userExperience(TimeStampsModel):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    position = models.ForeignKey(UserPosition, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)  
    responsibilities = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.company} - {self.position.name}"

class Institute(TimeStampsModel):
    name = models.CharField(max_length=100)
    address = models.TextField()
    website = models.URLField(blank=True)
    
    def __str__(self):
        return self.name

class UserEducation(TimeStampsModel):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    grade = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.degree} at {self.institute.name}"

class Language(TimeStampsModel):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class UserLanguage(TimeStampsModel):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    level = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.language.name} - {self.level}"

class Skill(TimeStampsModel):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class UserSkill(TimeStampsModel):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.skill.name} - {self.level}"

class UserReference(TimeStampsModel):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    
    def __str__(self):
        return f"{self.name} - {self.company}"
    