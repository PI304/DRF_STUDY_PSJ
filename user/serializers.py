from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "nickname",
            "profile_image_url",
            "profile_message",
            "last_login",
            "is_active",
            "created_at",
            "updated_at",
        ]
