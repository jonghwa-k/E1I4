from rest_framework import serializers
from .models import User
from articles.serializers import ArticleSerializer, CommentSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname')


class UserProfileSerializer(UserSerializer):
    articles = ArticleSerializer(many=True, read_only=True)
    profile_comments = CommentSerializer(many=True, read_only=True)
    like_article_list = serializers.SerializerMethodField()
    like_comment_list = serializers.SerializerMethodField()

    def get_like_article_list(self, obj):
        like_article = obj.like_article.all()
        return ArticleSerializer(like_article, many=True).data

    def get_like_comment_list(self, obj):
        like_comment = obj.like_comment.all()
        return CommentSerializer(like_comment, many=True).data

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('created_at', 'bio', 'articles', 'profile_comments', 'like_article_list', 'like_comment_list')