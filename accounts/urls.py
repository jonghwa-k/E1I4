from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView,
    LogoutView,
    SignupView,
    ProfileUpdateView,
    ProfileView,
    ChangePasswordView,
    DeleteAccountView,
    FollowView,
)

urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("signup/", SignupView.as_view(), name="signup"),
    path('account/delete/', DeleteAccountView.as_view(), name='delete-account'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path("profile/<str:username>/update/", ProfileUpdateView.as_view(), name="profile-update"),
    path('password/change/', ChangePasswordView.as_view(), name='change-password'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('follow/<str:username>/', FollowView.as_view(), name='follow'),
]