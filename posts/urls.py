from django.urls import path
from .views import PostViewSet, register, login_view
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
# router.register(r'comments', CommentViewSet, basename='comments')



urlpatterns = [
    path('auth/register/', register, name='api-register'),
    path('auth/login/', login_view, name='api-login'),
    
    # path('posts/<int:pk>/comments', post_detail, name='post-detail')

 ] + router.urls
