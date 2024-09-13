from django.db import models
from django.db.models import F, ExpressionWrapper, IntegerField, Count
from django.shortcuts import render, get_object_or_404
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
    ordering_fields = ['created_at', 'popularity']
    ordering = ['-created_at']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()

        # 인기도 계산 (좋아요 수 + 댓글 수 * 3 - 경과 일수 * 5)
        queryset = queryset.annotate(
            likes_count=Count('likes'),
            comments_count=Count('comments'),
            # 경과 일수를 직접 계산 (초 단위를 일 단위로 변환)
            days_since_created=ExpressionWrapper(
                (Now() - F('created_at')) / (60 * 60 * 24),  # 초를 일수로 변환
                output_field=IntegerField()
            )
        ).annotate(
            # 인기도 점수 계산: (좋아요 수 + 댓글 수 * 3 - 경과 일수 * 5)
            popularity=F('likes_count') + F('comments_count') * 3 - F('days_since_created') * 5
        )

        # 요청된 경우 인기순 정렬
        ordering = self.request.query_params.get('ordering')
        if ordering == 'popularity':
            return queryset.order_by('-popularity')

        # 기본 최신순 정렬
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
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
        if article.created_by != request.user:
            return Response({'error': '수정 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = self.get_object(pk)
        if article.created_by != request.user:
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