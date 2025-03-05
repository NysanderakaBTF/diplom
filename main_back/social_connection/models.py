from django.db import models
from django.conf import settings

class SocialMediaToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='social_tokens')
    platform = models.CharField(max_length=50, choices=[
        ('instagram', 'Instagram'),
        ('pinterest', 'Pinterest'),
        ('facebook', 'Facebook'),
        ('vk', 'VK'),
    ])
    extra = models.JSONField(default=dict)
    token = models.CharField(max_length=500)
    token_secret = models.CharField(max_length=500, blank=True, null=True)  # For OAuth1.0 (e.g., Pinterest)
    expires_at = models.DateTimeField(blank=True, null=True)  # For tokens with expiration

    def __str__(self):
        return f"{self.user.username}'s {self.platform} token"