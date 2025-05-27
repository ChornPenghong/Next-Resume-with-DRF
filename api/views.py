from .models import Language, Skill, UserProfile
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework import status, viewsets,filters
from .serializers import UserSerializer, LanguageSerializer, SkillSerializer
from rest_framework.decorators import authentication_classes, permission_classes,api_view
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

@api_view(['POST'])
def login(request): 
    user = get_object_or_404(User, username=request.data['username'], is_active=True)
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    token = Token.objects.get(user=user)
    return Response({
        'token': token.key,
        'user': UserSerializer(user).data
    })

@api_view(['POST'])
def register(request): 
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])
        user.save()
        
        # create user profile data
        user_profile = UserProfile.objects.create(
            user=user,
            full_name = serializer.data['username']
        )
        token = Token.objects.create(user=user)
        return Response({
            'token': token.key,
            'user': serializer.data
        })
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for {}".format(request.user.username))


# @api_view(['PUT'])
# def updateProfile()

### Language
class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def list(self, request): 
        queryset = self.filter_queryset(self.get_queryset())
        serializer = LanguageSerializer(queryset, many=True)
        return Response({
            "success": True,
            "data": serializer.data
        })
        
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def create(self, request): 
        serializer = LanguageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "data": serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        language = get_object_or_404(queryset, pk=pk)
        serializer = LanguageSerializer(language)
        return Response({
            "success": True,
            "data": serializer.data
        })
        
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def update(self, request, pk=None):
        queryset = self.get_queryset()
        language = get_object_or_404(queryset, pk=pk)
        serializer = LanguageSerializer(language, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "data": serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes([IsAuthenticated]) 
    def destroy(self, request, pk=None):
        queryset = self.get_queryset()
        language = get_object_or_404(queryset, pk=pk)
        language.delete()
        return Response({
            "success": True,
            "data": "Language deleted successfully"
        })         
        
### Skill
class SkillViewSet(viewsets.ModelViewSet): 
    queryset = Skill.objects.all()
    serializers = SkillSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def list(self, request): 
        queryset = self.filter_queryset(self.get_queryset())
        serializer = SkillSerializer(queryset, many=True)
        
        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def create(self, request):
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "data": serializer.data
            })
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def update(self, request, pk=None): 
        queryset = self.get_queryset()
        skill = get_object_or_404(queryset, pk=pk)
        serializer = SkillSerializer(skill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "data": serializer.data
            })
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def destroy(self, pk=None):
        queryset = self.get_queryset()
        skill = get_object_or_404(queryset, pk=pk)
        skill.delete()
        return Response({
            "success": True,
            "data": "Skill deleted successfully"
        })
        
