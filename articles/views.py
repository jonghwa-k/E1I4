from rest_framework import generics, permissions, serializers, status, views
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Article, Category, Comment
from .serializers import ArticleSerializer, CategorySerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

# 카테고리 목록 조회 및 등록 (관리자만 생성 가능)
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

# 게시글(Article) 목록 조회 및 등록 View
class ArticleListCreateAPIView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'description', 'created_by__username', 'category']
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# 게시물 상세 조회, 수정, 삭제 View
class ArticleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        # 게시물 인스턴스 가져오기
        instance = self.get_object()

        # 작성자 확인: 작성자만 삭제할 수 있도록 제한
        if request.user != instance.created_by:
            raise serializers.ValidationError({"error": "You do not have permission to delete this article."})

        # 삭제 처리
        self.perform_destroy(instance)

        # 200 OK 상태와 함께 삭제 성공 메시지 반환
        return Response({"detail": "게시물이 성공적으로 삭제되었습니다."}, status=status.HTTP_200_OK)

# 게시글 좋아요 추가/제거 View
class ArticleLikeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if article.likes.filter(id=request.user.id).exists():
            return Response({"detail": "Already liked this article."}, status=status.HTTP_400_BAD_REQUEST)
        
        article.likes.add(request.user)
        return Response({"detail": "Article liked."}, status=status.HTTP_200_OK)

    def delete(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if not article.likes.filter(id=request.user.id).exists():
            return Response({"detail": "You haven't liked this article."}, status=status.HTTP_400_BAD_REQUEST)
        
        article.likes.remove(request.user)
        return Response({"detail": "Article unliked."}, status=status.HTTP_200_OK)

# 댓글 생성 View
class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        article_id = self.kwargs['article_id']
        article = get_object_or_404(Article, id=article_id)
        serializer.save(author=self.request.user, article=article)

# 댓글 목록 조회 View
class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        article_id = self.kwargs['article_id']
        return Comment.objects.filter(article_id=article_id)

# 댓글 삭제 View
class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise serializers.ValidationError({"error": "You do not have permission to delete this comment."})
        instance.delete()

# 댓글 수정 View
class CommentUpdateView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        comment = self.get_object()
        if self.request.user != comment.author:
            raise serializers.ValidationError({"error": "You do not have permission to edit this comment."})
        serializer.save()