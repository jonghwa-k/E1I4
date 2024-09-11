from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .validators import validate_user_data

class UserCreateView(APIView):
    def post(self, request):
        rlt_message=validate_user_data(request.data)
        if rlt_message is None:
            return Response({"message": rlt_message}, status = 400)
        
        username = request.data.get("username")
        password = request.data.get("password")
        name = request.data.get("name")
        email = request.data.get("email")
        nickname = request.data.get("nickname")  
        bio = request.data.get("bio")

        user = User.objects.create_user(
            username=username,
            password=password,
            name =name,
            email=email,
            nickname=nickname,
            bio = bio,
        )

        return Response(
            {       
                    "id": user.pk,
                    "username":user.username,
                    "nickname":user.nickname,
            }
        )