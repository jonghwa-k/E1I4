from django.shortcuts import  get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
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

        if not User.objects.filter(username=username).exists():
            return Response({"message": "아이디가 틀렸습니다."}, status=400)
        
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"message": "비밀번호가 틀렸습니다."}, status=400)
        
        
        refresh=RefreshToken.for_user(user)
        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        )


class UserProfileView(APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request, username):
        user = get_object_or_404(User, username=username)
        if request.user != user:
            raise PermissionDenied("수정 권한이 없습니다")

        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({"message": '로그아웃 실패!'}, status=400)
        token = RefreshToken(refresh_token) # RefreshToken 객체 생성
        token.blacklist() # 블랙리스트에 추가
        return Response({"message":"로그아웃 성공!"}, status=205)


class UserPasswordChangeView(APIView):
    def put(self, request):
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            return Response({"message": "이전 비밀번호와 새 비밀번호를 모두 입력해주세요!"}, status=400)

        if not request.user.check_password(old_password):
            return Response({"message": "이전 비밀번호가 틀렸습니다"}, status=400)

        request.user.set_password(new_password)
        request.user.save()
        return Response({"message":"비밀번호 변경 성공!"}, status=200)


class UserDeleteView(APIView):
    def post(self, request):
        password = request.data.get("password")
        if not request.user.check_password(password):
            return Response({"message": "이전 비밀번호가 틀렸습니다"}, status=400)

        request.user.is_active=False
        request.user.save()
        return Response({"message":"회원탈퇴성공!!"}, status=200)
