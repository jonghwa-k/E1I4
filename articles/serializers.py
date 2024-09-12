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

# Article(게시글) 모델에 대한 Serializer
class ArticleSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    category = serializers.ChoiceField(choices=[('News', 'News'), ('자유게시판', '자유게시판')])
    total_likes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'description', 'image', 'created_at', 'created_by', 'category', 'total_likes']
        read_only_fields = ['id', 'created_at', 'created_by']

    def create(self, validated_data):
        article = Article.objects.create(**validated_data)
        return article

    def update(self, instance, validated_data):
        # 게시물 수정 시 category 필드는 선택적
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.category = validated_data.get('category', instance.category)  # 수정 시 카테고리는 선택적
        instance.save()
        return instance

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']