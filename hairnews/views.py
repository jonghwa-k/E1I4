from rest_framework.views import APIView
from rest_framework.response import Response

class MainView(APIView):
    def get(self, request):
        data = {
            'message': '메인페이지'
        }
        return Response(data)