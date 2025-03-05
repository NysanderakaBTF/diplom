from rest_framework import viewsets, permissions
from .models import SocialMediaToken
from .serializers import SocialMediaTokenSerializer

class SocialMediaTokenViewSet(viewsets.ModelViewSet):
    queryset = SocialMediaToken.objects.all()
    serializer_class = SocialMediaTokenSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only see their own tokens
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the user to the current user
        serializer.save(user=self.request.user)