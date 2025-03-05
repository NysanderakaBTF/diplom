from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SocialMediaTokenViewSet

router = DefaultRouter()
router.register(r'social-tokens', SocialMediaTokenViewSet, basename='socialtoken')

urlpatterns = [
    path('', include(router.urls)),
]