from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.postView, name='post'),
    path('posts/<int:pk>/', views.postDetail, name='post_detail'),
    path('posts/<int:pk>/comments/', views.postComments, name='post_comments')
    
]