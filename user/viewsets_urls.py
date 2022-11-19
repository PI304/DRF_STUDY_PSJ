from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from user.views import UserView

user_list = UserView.as_view({
    'get': 'list',
    'post': 'create'
})

user_detail = UserView.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
})

urlpatterns = format_suffix_patterns([
    path("/", user_list, name="user_list"),
    path("<int:pk>/", user_detail, name="user_detail")
])