from rest_framework import serializers
from .models import Article, Category, Comment
from accounts.models import User  # CustomUser 대신 User로 변경

# 작성자 정보에서 username만 직렬화하는 Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

# 카테고리 Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
        
# Article(게시글) 모델에 대한 Serializer
class ArticleSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    category = serializers.ChoiceField(choices=[('News', 'News'), ('자유게시판', '자유게시판')])
    comments = CommentSerializer(many=True, read_only=True)  # 댓글 리스트 추가
    total_likes = serializers.IntegerField(read_only=True)
    popularity = serializers.IntegerField(read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'description', 'image', 'created_at', 'updated_at', 'created_by', 'category', 'total_likes', 'comments', 'popularity']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by', 'comments', 'total_likes', 'popularity']


    def create(self, validated_data):
        return Article.objects.create(**validated_data)


    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
