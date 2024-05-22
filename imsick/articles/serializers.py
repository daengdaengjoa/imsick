from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["article_id", "title", "content", "created_at", "updated_at"]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["article_id", "account", "article", "created_at"]
        # read_only_fields = ["created_at"]