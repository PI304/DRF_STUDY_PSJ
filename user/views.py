from rest_framework import viewsets
from user.models import MyUser
from user.serializers import UserSerializer
from rest_framework import generics

class UserView(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer

