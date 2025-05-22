from django.urls import path, include
from . import views

urlpatterns = [
    path('posts/list', views.listPost),
    path('posts/store', views.storePost),
    path('posts/update/<int:id>', views.updatePost),
    path('posts/show/<int:id>', views.showPost),
    path('posts/delete/<int:id>', views.deletePost)
]
