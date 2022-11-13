from user.models import MyUser
from user.serializers import UserSerializer
from rest_framework import generics, mixins, filters
from rest_framework.response import Response
from datetime import datetime
from rest_framework import status


class UserList(generics.ListCreateAPIView):
    queryset = MyUser.objects.filter(is_active=True).all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["nickname", "email"]
    
class UserDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = MyUser.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=partial)

        serializer.is_valid(raise_exception=True)

        serializer.save(
            updated_at=datetime.now()
        )
        return Response(serializer.dwsata, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save(update_fields=["is_active"])
        serializer = UserSerializer(instance)

        return Response(serializer.data, status=status.HTTP_200_OK)