from rest_framework import serializers
from .models import Article

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"