from rest_framework import generics, permissions, serializers, status, views
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from django.utils.timezone import now
from django.db.models import F, ExpressionWrapper, IntegerField, Count
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from .models import Article, Category, Comment
from .serializers import ArticleSerializer, CategorySerializer, CommentSerializer

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

class ArticleListCreateAPIView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description', 'created_by__username', 'category']
    ordering_fields = ['created_at', 'popularity']
    ordering = ['-created_at']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            likes_count=Count('likes'),
            comments_count=Count('comments'),
            days_since_created=ExpressionWrapper(
                now() - F('created_at'),
                output_field=IntegerField()
            ) / (24 * 3600)
        ).annotate(
            popularity=ExpressionWrapper(
                F('likes_count') + F('comments_count') * 3 - F('days_since_created') * 5,
                output_field=IntegerField()
            )
        )
        return queryset.order_by('-popularity', '-created_at')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ArticleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.created_by:
            return Response({"error": "You do not have permission to delete this article."}, 
                            status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response({"detail": "게시물이 성공적으로 삭제되었습니다."}, status=status.HTTP_200_OK)

class ArticleLikeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if article.likes.filter(id=request.user.id).exists():
            article.likes.remove(request.user)
            liked = False
        else:
            article.likes.add(request.user)
            liked = True
        return Response({"liked": liked}, status=status.HTTP_200_OK)

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        article = get_object_or_404(Article, id=self.kwargs['article_id'])
        serializer.save(author=self.request.user, article=article)

class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Comment.objects.filter(article_id=self.kwargs['article_id'])

class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise serializers.ValidationError({"error": "You do not have permission to delete this comment."})
        instance.delete()

class CommentUpdateView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        comment = self.get_object()
        if self.request.user != comment.author:
            raise serializers.ValidationError({"error": "You do not have permission to edit this comment."})
        serializer.save()


# 내가 좋아요한 게시글 목록 보기
class LikedArticlesListView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        # 사용자가 좋아요한 게시글만 반환
        return Article.objects.filter(likes=self.request.user)


# 내가 좋아요한 댓글 목록 보기
class LikedCommentsListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        # 사용자가 좋아요한 댓글만 반환 (댓글에 좋아요 기능이 있어야 함)
        return Comment.objects.filter(likes=self.request.user)


# 내가 작성한 글 목록 보기
class MyArticlesListView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        # 사용자가 작성한 게시글만 반환
        return Article.objects.filter(created_by=self.request.user)


# 내가 작성한 댓글 목록 보기
class MyCommentsListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        # 사용자가 작성한 댓글만 반환
        return Comment.objects.filter(author=self.request.user)