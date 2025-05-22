from django.shortcuts import render
from authentication.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def login(request):
    pass

@csrf_exempt
def register(request): 
    try:
        if request.method != 'POST':
            return JsonResponse({
                'message': 'Method not allowed'
            }, status=405)

        email = request.POST['email'],
        password = request.POST['password']

        user = User.objects.create_user(
            email = email,
            password = password
        )

        return JsonResponse({
            'id': user.id,
            'email': user.email
        }, status=201)
    
    except Exception as e:
        return JsonResponse({
            'message': 'An error occurred, ' + str(e)
        }, status=500)
    