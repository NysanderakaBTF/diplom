from rest_framework import serializers
from .models import SocialMediaToken

class SocialMediaTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaToken
        fields = ['id', 'user', 'platform', 'token', 'token_secret', 'expires_at', 'extra']
        read_only_fields = ['user']  # User is automatically set in the view