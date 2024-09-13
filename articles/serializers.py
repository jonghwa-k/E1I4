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
    author = serializers.ReadOnlyField(source='author.username')  # 작성자 필드를 읽기 전용으로 설정
    like_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    category = serializers.ChoiceField(choices=[('News', 'News'), ('자유게시판', '자유게시판')])

    def get_like_count(self, obj):
        return obj.likes.all().count()

    class Meta:
        model = Article
        fields = ('id',  "category", "title", "image","content", "author",  "url", "like_count", "comments")