from rest_framework import serializers
from .models import Article, Comment


class CommentSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()

    def get_like_count(self, obj):
        return obj.likes.all().count()

    class Meta:
        model = Comment
        fields = ('id', "author", "article", "content", "created_at", "updated_at", "like_count")
        read_only_fields = ("article",)


class ArticleSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    def get_like_count(self, obj):
        return obj.likes.all().count()

    class Meta:
        model = Article
        fields = ('id', "title", "content", "image", "url", "author", "like_count", "comments")