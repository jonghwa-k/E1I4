from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.UserCreateView.as_view()),
    path("login/", views.UserLoginView.as_view()),
    path("profile/<str:username>/", views.UserProfileView.as_view()),
    path("logout/", views.LogoutView.as_view()),
    path("passwordchange/", views.UserPasswordChangeView.as_view()),
    path("delete/",views.UserWithdraView.as_view()),
]