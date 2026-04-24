from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id','post','content','author','created_at' )
        read_only_fields = ['post']
        
    def validate_content(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Content cannot be empty!!')
        if len(value)< 3:
            raise serializers.ValidationError('Content must be atleast 3 characters')
        if len(value) > 500:
            raise serializers.ValidationError('Content too long, should be less than 500 characters')
        return value
    def validate_author(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError('Username must be atleast 3 characters')
        if not value:
            raise serializers.ValidationError('Author field cannot be empty')
        return value
            
        

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)
    
    class Meta:
        model = Post
        fields = ('id','title','description','image','owner','created_at','updated_at','comments')
        
    def validate_title(self, value):
        if len(value) < 4:
            raise serializers.ValidationError('Title must be atleast 4 characters')
        if not value:
            raise serializers.ValidationError('Title cannot be empty')
        
        return value
    
    def validate_description(self, value):
        if not value:
            raise serializers.ValidationError('Description field cannot be empty')
        if 'title' in value:
            raise serializers.ValidationError('Please, do not use the same word as your title')    
        

                