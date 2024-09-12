from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from .serializers import ArticleSerializer
from .models import Article
from rest_framework.permissions import AllowAny


class AriticleCreateAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [permission() for permission in self.permission_classes]
    
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)  
            return Response(serializer.data, status=201) 
        
    def get(self, request):
        articles = Article.objects.all().order_by('-id')
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    

# 글 상세페이지 조회, 글 수정, 글 삭제
# 글 상세페이지는 비회원도 볼 수 있음
class ArticleDetailAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [permission() for permission in self.permission_classes]

    def get(self, request, pk):
        article = get_object_or_404(Article, id=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        article = get_object_or_404(Article, id=pk)
        if article.author != request.user:
            return Response({'error': '수정 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        article = get_object_or_404(Article, id=pk)
        if article.author != request.user:
            return Response({'error': '삭제 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)