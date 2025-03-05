from adrf.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveDestroyAPIView
from adrf.views import APIView
from django.http import FileResponse
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from .models import Post, Image
from .permissions import IsAuthenticated, IsAuthorOrAdmin
from .serializers import PostSerializer, ImageSerializer, PostShortSerializer


class PostShortInfo(APIView):
    permission_classes = (IsAuthenticated,)
    async def get(self, request):
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if request.user.is_staff:  # Admin can see all posts
            posts = Post.objects.all().order_by('-pub_datetime')
        else:  # Authors see only their posts
            posts = Post.objects.filter(author=request.user).order_by('-pub_datetime')

        if start_date:
            start_date = parse_datetime(start_date)
            posts = posts.filter(pub_datetime__gte=start_date)
        if end_date:
            end_date = parse_datetime(end_date)
            posts = posts.filter(pub_datetime__lte=end_date)
        dd = await PostShortSerializer(data=posts, many=True).adata
        return Response(dd)


class PostListCreate(APIView):
    permission_classes = [IsAuthenticated]  # Listing is limited to authenticated users

    async def get(self, request):
        # Filter posts for the authenticated user (author or admin)
        if request.user.is_staff:  # Admin can see all posts
            posts = Post.objects.all().order_by('-pub_datetime')
        else:  # Authors see only their posts
            posts = Post.objects.filter(author=request.user).order_by('-pub_datetime')
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if start_date:
            start_date = parse_datetime(start_date)
            posts = posts.filter(pub_datetime__gte=start_date)
        if end_date:
            end_date = parse_datetime(end_date)
            posts = posts.filter(pub_datetime__lte=end_date)
        serializer = await PostSerializer(posts, many=True).adata
        return Response(serializer)

    async def post(self, request):
        request.data.setdefault('author', request.user.pk)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Author is set to the logged-in user
            aa = await serializer.adata
            return Response(aa, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    permission_classes = [IsAuthenticated, IsAuthorOrAdmin]

    async def get(self, request, pk):
        post = Post.objects.filter(pk=pk).first()
        if not post:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, post)  # Check if the user is the author or admin
        serializer = await PostSerializer(post).adata
        return Response(serializer)

    async def put(self, request, pk):
        post = Post.objects.filter(pk=pk).first()
        if not post:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, post)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            ss = await serializer.adata
            return Response(ss)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    async def delete(self, request, pk):
        post = Post.objects.filter(pk=pk).first()
        if not post:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageListDelete(APIView):
    permission_classes = [IsAuthenticated, IsAuthorOrAdmin]

    async def get(self, request, post_id):
        post = Post.objects.filter(pk=post_id).first()
        if not post:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, post)
        images = Image.objects.filter(post=post)
        serializer = await ImageSerializer(images, many=True).adata
        return Response(serializer)

    async def delete(self, request, pk):
        image = Image.objects.filter(pk=pk).first()
        if not image:
            return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, image.post)  # Validate permissions against the associated post
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ImageUpload(APIView):
    """
    Upload an image for a specific post.
    """
    permission_classes = [IsAuthenticated, IsAuthorOrAdmin]
    parser_classes = [MultiPartParser, FormParser]  # Handle file uploads

    async def post(self, request, post_id):
        post = Post.objects.filter(pk=post_id).first()
        if not post:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, post)  # Ensure user has permissions for the post
        request.data.setdefault('post', post.pk)
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post)
            ss = await serializer.adata
            return Response(ss, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DownloadImage(APIView):
    """
    Serve an image for download.
    """
    permission_classes = [IsAuthenticated, IsAuthorOrAdmin]

    async def get(self, request, pk):
        image = Image.objects.filter(pk=pk).first()
        if not image:
            return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, image.post)  # Ensure permissions for the associated post

        # Serve the image file for download
        return FileResponse(image.image.open(), as_attachment=True, filename=image.image.name)