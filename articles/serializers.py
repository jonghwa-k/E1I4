from rest_framework import serializers
from .models import Article, Comment, Category

# 카테고리 Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

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
    category = serializers.StringRelatedField()  # 카테고리 이름 반환

    def get_like_count(self, obj):
        return obj.likes.all().count()

    class Meta:
        model = Article
        fields = ('id', "title", "content", "image", "url", "author", "like_count", "comments", "category")