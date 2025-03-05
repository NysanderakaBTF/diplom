from adrf.serializers import ModelSerializer
from .models import Post, Image


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'post', 'created']


class PostSerializer(ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)  # Related images

    class Meta:
        model = Post
        fields = ['id', 'text', 'tags', 'pub_datetime', 'status', 'author', 'images', 'title']

class PostShortSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'pub_datetime', 'status', 'author', 'title']