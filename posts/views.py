from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

@api_view(['GET','POST'])
@permission_classes([AllowAny])
def postView(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PostSerializer( data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'The post is created successfully!!','data': serializer.data},
                            status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def postDetail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    serializer = PostSerializer(post)
    
    return Response(serializer.data)


@api_view(['GET','POST'])
@permission_classes([AllowAny])
def postComments(request, pk):
  
    if request.method =='GET':
          comments = Comment.objects.filter(post_id = pk)
          serializer = CommentSerializer(comments, many=True)
          return Response(serializer.data)
    elif request.method == 'POST':
       
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post_id =pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      
        
        
    
    