from django.urls import path
from .views import ArticleListCreateAPIView, ArticleDetailAPIView, CategoryListCreateAPIView, ArticleLikeView, CommentCreateView, CommentListView, CommentDeleteView, CommentUpdateView

# URL 패턴 설정
urlpatterns = [
    path('', ArticleListCreateAPIView.as_view(), name='article-list-create'),
    path('<int:pk>/', ArticleDetailAPIView.as_view(), name='article-detail'),
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('<int:article_id>/like/', ArticleLikeView.as_view(), name='article-like'),
    path('<int:article_id>/comments/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('comments/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment-edit'),
]