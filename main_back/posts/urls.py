from django.urls import path
from .views import (
    PostListCreate,
    PostDetail,
    ImageListDelete,
    ImageUpload,
    DownloadImage,
)

urlpatterns = [
    # Post management
    path('', PostListCreate.as_view(), name='post_list_create'),  # List and create posts
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),  # Retrieve, update, delete a single post

    # Image management
    path('<int:post_id>/images/', ImageListDelete.as_view(), name='image_list_delete'),  # List or delete images for a post
    path('<int:post_id>/images/upload/', ImageUpload.as_view(), name='image_upload'),  # Upload an image for a post
    path('<int:pk>/download/', DownloadImage.as_view(), name='image_download'),  # Download a specific image
]