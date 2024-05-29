from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "content", 
            "author",
            "created_at",
            "is_reply"
        ]
        extra_kwargs = {
            'author': {'required': False},
            'is_reply': {'required': False}
        }    

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "content_ai",
            "author",
            "category",
            "view_count",
            "like_counts",
        ]
        read_only_fields = ["author", "category",]


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('content', None)
        return representation

class PostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True, required=False)
    
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "content_ai",
            "author",
            "category",
            "view_count",
            "like_counts",
            "created_at",
            "updated_at",
            "comments"
        ]
        read_only_fields = ["author", "category",]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('category', None)
        return representation