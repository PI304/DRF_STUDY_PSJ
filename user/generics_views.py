from user.models import MyUser
from user.serializers import UserSerializer
from rest_framework import generics, mixins
from rest_framework.response import Response
from datetime import datetime
from rest_framework import status
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
import smtplib
from email.mime.text import MIMEText

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.filter(is_active=True).all()
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


class SignUpView(generic.CreateView):
    form_class = UserCreationForm #장고 기본 회원가입 뷰
    success_url = reverse_lazy("login") #로그인시 뒤로가기
    #template_name = "registration/signup.html"

smtp_info = {
    'gmail.com': ('smtp.gmail.com', 587),
    'naver.com': ('smtp.naver.com', 587),
}

smtp = smtplib.SMTP('smtp.gmail.com', 587)

smtp.ehlo()

smtp.starttls()

smtp.login('june416412@gmail.com', 'saavdmfpsgadfuou')

msg = MIMEText('내용 : 본문 내용')
msg['Subject'] = '제목: 파이썬으로 gmail 보내기'

smtp.sendmail('발신 할 메일 주소', '수신 받을 메일 주소', msg.as_string())

smtp.quit()