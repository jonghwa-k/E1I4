from django.utils import timezone
from rest_framework import status, views, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import SignupSerializer, ProfileUpdateSerializer
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        
        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful. Token has been blacklisted."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

class ProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'username'

class ProfileUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'username'
    
    

class ChangePasswordView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            return Response({"detail": "Both old and new passwords are required."}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(old_password):
            return Response({"detail": "Wrong old password."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)

class DeleteAccountView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        password = request.data.get("password")

        # Check if password is provided
        if not password:
            return Response({"detail": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Verify that the provided password is correct
        if not user.check_password(password):
            return Response({"detail": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)

        # Deactivate the account instead of deleting it
        user.is_active = False  # Set the is_active field to False
        user.deactivation_date = timezone.now()  # Set the current time as the deactivation date
        user.save()  # Save the updated user object

        return Response({"detail": "Account deactivated successfully. It will be permanently deleted in 30 days."}, status=status.HTTP_204_NO_CONTENT)


