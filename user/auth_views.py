from django.contrib.auth.models import update_last_login
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed

from drfTuto.utils import PasswordNotMatch
from drfTuto.renderer import CustomRenderer
from user.models import User
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from django.contrib.auth.hashers import check_password

from user.serializers import UserSerializer
from user.services import UserServices

import smtplib
from email.mime.text import MIMEText

smtp_info = {
    'gmail.com': ('smtp.gmail.com', 587),
    'naver.com': ('smtp.naver.com', 587),
}

smtp = smtplib.SMTP('smtp.gmail.com', 587)

smtp.ehlo()

smtp.starttls() #tls 암호화, 587 port 사용시 필요


class BasicSignUpView(APIView):
    serializer_class = UserSerializer
    renderer_classes = [CustomRenderer]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")

        if password != confirm_password:
            raise PasswordNotMatch

        email = request.data.get("email")
        nickname = request.data.get("nickname")

        user = User.objects.create_user(email=email, password=password, nickname=nickname)

        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PasswordChangeView(APIView):
    serializer = UserSerializer
    renderer_classes = [CustomRenderer]

    def post(self, request, *args, **kwargs):
        user = request.user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        if not check_password(current_password, user.password):
            raise AuthenticationFailed

        user.set_password(new_password)
        user.save(update_fields=["password"])

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CheckDuplicateUsernameView(APIView):
    renderer_classes = [CustomRenderer]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")

        existing_email = User.objects.filter(email=email).first()
        if existing_email:
            return Response({"details": "Provided email already exists."}, status=status.HTTP_409_CONFLICT)

        return Response({"email": email}, status=status.HTTP_200_OK)

class EmailVerification(APIView):
    renderer_classes = [CustomRenderer]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        generated_code = UserServices.generate_random_code()

        # set code in cookie
        res = JsonResponse({'success': True})
        res.set_cookie('email_verification_code', generated_code, max_age=300)

        # 메일 내용
        msg = MIMEText('이메일 인증 코드 : ', generated_code)

        # 메일 제목
        msg['Subject'] = '이메일 인증 코드입니다'

        success = smtp.sendmail('june416412@gmail.com', email, msg.as_string()) #발신 메일, 수신 메일, 본문 내용

        if success > 0:
            return Response(status=status.HTTP_200_OK)
        elif success == 0:
            return Response({"details": "Failed to send email"},status=status.HTTP_400_BAD_REQUEST)


class EmailConfirmation(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if 'email_verification_code' in request.COOKIES:
            code_cookie = request.COOKIES['email_verification_code']
        else:
            return Response({"details": "No cookies attached"}, status=status.HTTP_400_BAD_REQUEST)

        code_input = request.data.get("verification_code")
        if code_cookie == code_input:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"details": "Verification code does not match."}, status=status.HTTP_400_BAD_REQUEST)

smtp.login('june416412@gmail.com', '')