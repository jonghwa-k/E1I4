from django.db import models
from django.db.models import F, ExpressionWrapper, IntegerField, Count
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.timezone import now  # 현재 시간
from django.db.models.functions import ExtractDay, Now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters, status, generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from .serializers import ArticleSerializer, CommentSerializer, CategorySerializer
from .models import Article, Comment, Category
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter


# 카테고리 목록 및 생성 API (관리자만 생성 가능)
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


# 게시글 작성 및 목록 조회 API
class ArticleCreateAPIView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'content', 'author__username', 'category']
    filterset_fields = ['category']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')  # 최신순 정렬

    def perform_create(self, serializer):
        # author 필드를 현재 요청한 사용자로 설정
        serializer.save(author=self.request.user)


# 글 상세, 수정, 삭제 API
class ArticleDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()

    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        article = self.get_object(pk)
        if article.author != request.user:  # 수정 권한 검사
            return Response({'error': '수정 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = self.get_object(pk)
        if article.author != request.user:  # 삭제 권한 검사
            return Response({'error': '삭제 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 댓글 생성 API
class CommentCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(article=article, author=request.user)  # 댓글 작성자 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 댓글 수정, 삭제 API
class CommentDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, comment_pk):
        return get_object_or_404(Comment, pk=comment_pk)

    def put(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        if comment.author != request.user:
            return Response({'error': '수정 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        if comment.author != request.user:
            return Response({'error': '삭제 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 게시글 좋아요 API
class ArticleLikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        if request.user in article.likes.all():
            article.likes.remove(request.user)
            return Response("좋아요 취소", status=status.HTTP_200_OK)
        else:
            article.likes.add(request.user)
            return Response("좋아요", status=status.HTTP_200_OK)


# 댓글 좋아요 API
class CommentLikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            return Response("좋아요 취소", status=status.HTTP_200_OK)
        else:
            comment.likes.add(request.user)
            return Response("좋아요", status=status.HTTP_200_OK)