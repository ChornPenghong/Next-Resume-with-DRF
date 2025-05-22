import json
from .models import Post
from datetime import datetime
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder

def listPost(request): 
    if request.method == 'GET':
        posts = list(Post.objects.values().order_by('-created_at'))
        
        for post in posts:
            post['created_at'] = post['created_at'].strftime("%Y-%m-%d %H:%M:%S %p")

        return JsonResponse({
            'success': True,
            'data': posts
        }, encoder=DjangoJSONEncoder, safe=False) 

@csrf_exempt
def storePost(request): 
    try:
        if request.method == 'POST': 
            data = json.loads(request.body)
            post = Post.objects.create(
                title = data['title'],
                content = data['content']
            )

            return JsonResponse({
                'id': post.id, 
                'title': post.title
            }, status=201)
        else:
            return JsonResponse({
                'message': 'The method is not allowed.'
            }, status=405)
    except Exception as e: 
        return JsonResponse(e)
    
@csrf_exempt 
def updatePost(request, id):
    if request.method != 'PUT':
        return JsonResponse({
            'message': 'The method is not allowed.'
        }, status=405)
    
    try:
        data = json.loads(request.body)
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Post not found.'
            }, status=200)
        
        if post.title == data['title']:
            return JsonResponse({
                'success': False,
                'message': 'Cannot update without any change.'
            }, status=200)
        
        post.title = data['title']
        post.content = data['content']
        post.save()

        return JsonResponse({
            'id': post.id,
            'title': post.title
        }, status=200)
    
    except Exception as e:
         return JsonResponse({
            'message': 'An error occurred.',
            'error': str(e)
        }, status=500)

@csrf_exempt
def deletePost(request, id):
    try:
        if request.method != 'DELETE':
            return JsonResponse({
                'message': 'The method is not allowed.'
            }, status=405)
        
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Post not found.' 
            }, status=200)
        
        post.delete()
        return JsonResponse({
            'success': True,
            'message': 'Post deleted successfully.'
        }, status=200)

    except Exception as e:
        return JsonResponse({
            'message': 'An error occurred, ' + str(e)
        }, status=500)

def showPost(request, id): 
    try: 
        if request.method != 'GET':
            return JsonResponse({
                'message': 'The method is not allowed.'
            }, status=405)
        
        try: 
            post = Post.objects.get(id=id)
        except Post.DoesNotExist: 
            return JsonResponse({
                'success': False,
                'message': 'Post not found.'
            }, status=200)
        
        return JsonResponse({
            'success': True,
            'data': post
        }, safe=False)
    except Exception as e:
        return JsonResponse({
            'message': 'An error occurred, ' + str(e)
        }, status=500)