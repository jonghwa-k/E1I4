from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname')

class UserProfileSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('created_at','bio',)