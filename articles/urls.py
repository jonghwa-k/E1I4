from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.AriticleCreateAPIView.as_view()),
    path("<int:pk>/", views.ArticleDetailAPIView.as_view()),
    path("<int:pk>/like/", views.ArticleLikeAPIView.as_view()),
    path("<int:pk>/comments/", views.CommentCreateAPIView.as_view()),
    path("comments/<int:comment_pk>/", views.CommentDetailAPIView.as_view()),
    path("comments/<int:comment_pk>/like/", views.CommentLikeAPIView.as_view()),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)