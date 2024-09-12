from rest_framework import serializers
from .models import Article
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("article",)


class ArticleSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only = True)

    class Meta:
        model = Article
        fields = ('id', "title", "content","image","url","author")