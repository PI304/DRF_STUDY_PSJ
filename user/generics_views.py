from user.models import MyUser
from user.serializers import UserSerializer
from rest_framework import generics, mixins
from rest_framework.response import Response
from datetime import datetime

class UserList(generics.ListCreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetireveAPIView): #검색
    queryset = MyUser.objects.all()
    serialzier_class = UserSerializer

class UserUpdate(generics.UpdateAPIView): #업데이트
    queryset = MyUser.objects.all()
    serialzier_class = UserSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=partial)

        serializer.is_valid(raise_exception=True)

        serializer.save(
            updated_at=datetime.now()
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDestroy(generics.DestroyAPIView):
    queryset = MyUser.objects.all()
    serialzier_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save(update_fields=["is_active"])
        serializer = UserSerializer(instance)

        return Response(serializer.data, status=status.HTTP_200_OK)