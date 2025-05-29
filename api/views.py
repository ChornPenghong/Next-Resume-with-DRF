from django.contrib.auth.models import User
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework import status, viewsets,filters
from .models import Language, Skill, UserProfile, UserPosition, userExperience
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes,api_view
from .serializers import UserSerializer, LanguageSerializer, SkillSerializer, UserProfileSerializer, UserPositionSerializer, ExperienceSerializer
from rest_framework.decorators import action

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

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateProfile(request):
    user = User.objects.get(username=request.data['username'])
    user_profile = UserProfile.objects.get(user=user)
    user_profile.full_name = request.data['full_name']
    user_profile.email = request.data['email']
    user_profile.phone = request.data['phone']
    user_profile.address = request.data['address']
    user_profile.description = request.data['description']
    user_profile.linkedin = request.data['linkedin']
    user_profile.github = request.data['github']
    user_profile.website = request.data['website']
    user_profile.save()
    return Response({
        'success': True,
        'data': UserSerializer(user).data
    })
    
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def userDetail(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_profile_data = UserProfileSerializer(user_profile).data
    return Response({
        'success': True,
        'data': user_profile_data
    })

### Language
class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes([IsAuthenticated])
    
    @action(detail=False, methods=['get'], url_path='list-all')
    def listAll(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializers = self.get_serializer(queryset, many=True)

        data = [
            {
                "id" : item['id'],
                "name" : item['name'],
            }
            for item in serializers.data
        ]

        return Response({
            "success": True,
            "data": data
        })
        
    def list(self, request): 
        queryset = self.filter_queryset(self.get_queryset())
        serializer = LanguageSerializer(queryset, many=True)
        return Response({
            "success": True,
            "data": serializer.data
        })
        
    def create(self, request): 
        serializer = LanguageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "data": serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        language = get_object_or_404(queryset, pk=pk)
        serializer = LanguageSerializer(language)
        return Response({
            "success": True,
            "data": serializer.data
        })
        
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
    serializer_class = SkillSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'], url_path='list-all')
    def listAll(self, request): 
        queryset = self.filter_queryset(self.get_queryset())
        serializers = self.get_serializer(queryset, many=True)
        
        data = [
            {
                "id" : item['id'],
                "name" : item['name'],
            }
            for item in serializers.data
        ]
        
        return Response({
            "success": True,
            "data": data
        })
    
    def list(self, request): 
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "data": serializer.data
            })
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None): 
        queryset = self.get_queryset()
        skill = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(skill, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "data": serializer.data
            })
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        queryset = self.get_queryset()
        skill = get_object_or_404(queryset, pk=pk)
        skill.delete()
        return Response({
            "success": True,
            "data": "Skill deleted successfully"
        })
    
# Position
class PositionViewSet(viewsets.ModelViewSet):
    queryset = UserPosition.objects.all()
    serializer_class = UserPositionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='list-all')
    def listAll(self, request): 
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        position = [
            {
                "id" : item['id'],
                "name" : item['name'],
            }
            for item in serializer.data
        ]
        
        return Response({
            "success": True,
            "data": position
        })
        
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "data": serializer.data
        })

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "data": serializer.data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        queryset = self.get_queryset()
        position = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(position, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "data": serializer.data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = self.get_queryset()
        position = get_object_or_404(queryset, pk=pk)
        position.delete()
        return Response({
            "success": True,
            "data": "Position deleted successfully"
        })
        
class ExperienceViewSet(viewsets.ModelViewSet): 
    queryset = userExperience.objects.all()
    serializer_class = ExperienceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
         
        return Response({
            "success": True,
            "data": serializer.data
        })
        
    def create(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user_profile=user_profile)
            return Response({
                "success": True,
                "data": serializer.data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self, request, pk=None):
        experience = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(experience)
        
        return Response({
            "success": True,
            "data": serializer.data
        })

    def update(self, request, pk=None):
        queryset = self.get_queryset()
        experience = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(experience, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "data": serializer.data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        queryset = self.get_queryset()
        experience = get_object_or_404(queryset, pk=pk)
        experience.delete()
        return Response({
            "success": True,
            "data": "Experience deleted successfully"
        })