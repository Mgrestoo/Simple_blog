from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination  
from rest_framework.decorators import action  
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error':'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'error':'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)  
    
    user = User.objects.create_user(username=username, password=password)
    
    
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({'token':token.key, 'username':user.username}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    password = request.data.get('password')
    username = request.data.get('username')
    
    
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error':'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)   
    
    if not user.check_password(password):
        return Response({'error':'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED) 
    
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'username':user.username}, status=status.HTTP_201_CREATED)
class Custompagination(PageNumberPagination):
    page_query_param = 'p'
class PostViewSet(ModelViewSet):
    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = Custompagination
    filter_backends = [DjangoFilterBackend,SearchFilter, OrderingFilter]
    filterset_fields = ['title']
    search_fields = ['^title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
    
    @action(detail=True, methods=['post','get'], url_path='comments')
    def comments(self,request,pk=None):
        post = self.get_object()
        
        if request.method =='GET':
            comments= post.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        
        elif request.method=='POST':
            serializer = CommentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)    
        
   
        



