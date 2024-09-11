from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import User
from .validators import validate_user_data
from .serializers import UserSerializer, UserProfileSerializer


class UserCreateView(APIView):
    permission_classes=[AllowAny]

    def post(self, request):
        rlt_message=validate_user_data(request.data)
        if rlt_message is not None:
            return Response({"message": rlt_message}, status = 400)

        # user = User.objects.create_user(
        #     username=request.data.get("username"),
        #     password=request.data.get("password"),
        #     name =request.data.get("name"),
        #     email=request.data.get("email"),
        #     nickname=request.data.get("nickname") ,
        #     bio = request.data.get("bio")
        # )

        #상위코드 간소화
        user = User.objects.create_user(**request.data)
        
        refresh=RefreshToken.for_user(user) # 토큰발급        

        serializer = UserSerializer(user)
        response_dict=serializer.data
        response_dict['access'] = str(refresh.access_token)
        response_dict['refresh'] = str(refresh)
        return Response(response_dict)


class UserLoginView(APIView):
    permission_classes=[AllowAny]

    def post(self, request):
        username= request.data.get("username")
        password= request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"message": "아이디 또는 비밀번호가 틀렸습니다."}, status=400)
        
        
        refresh=RefreshToken.for_user(user)
        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        )
    

class UserProfileView(APIView):
    def get(self, request, username):
        user= get_object_or_404(User, username=username)
        serializer=UserProfileSerializer(user)
        return Response(serializer.data)
