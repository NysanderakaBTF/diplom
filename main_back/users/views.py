from adrf.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .models import User
from .permissions import IsAdmin
from .serializers import UserSerializer


class GetListUsers(APIView):
    permission_classes = [IsAdmin]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    async def get(self, request):
        limit = request.GET.get('limit', 20)
        offset = request.GET.get('offset', 0)
        u1 = self.queryset[offset:offset+limit]
        users = self.serializer_class(data=u1, many=True)
        users.is_valid()
        a = await users.adata
        return Response(a)

# me, login and registration is implemented in dj-rest-auth

class MakeUserAdmin(APIView):
    permission_classes = [IsAdmin]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    async def post(self, request, user_id):
        user = self.queryset.get(pk=user_id)
        user.is_staff = True
        user.save()
        ss = await self.serializer_class(user).adata
        return Response(ss)

class BanUser(APIView):
    permission_classes = [IsAdmin]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    async def post(self, request, user_id):
        user = self.queryset.get(pk=user_id)
        user.is_staff = False
        user.is_active = False
        user.save()
        return Response(data=None, status=status.HTTP_200_OK)

