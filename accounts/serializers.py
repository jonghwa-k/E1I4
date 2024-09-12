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
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('created_at', 'bio', 'articles', 'profile_comments')