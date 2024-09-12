from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status

class AriticleCreateAPIView(APIView):
    def post(self, request):
        pass