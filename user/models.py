from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(
            self,
            email=None,
            password=None
        ):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self,
            email=None,
            password=None
        ):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    id = models.BigAutoField(
        primary_key=True
        null=False
        ) 
    #id-유저번호/bigautofield 1~~ int/primary_key = user 클래스의 첫 밸류
    
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=False
    )

    nickname = models.CharField(
        max_length=20,
        null=False,
        blank=False
    )
    
    profile_image_url = models.URLField(
        max_length=512,
        blank=True,
        default="https://hermes4164.web.app/assets/img/%EC%9C%A0%EB%A0%B9.jpg", #본인 팩맨 유령 프사, 추후 변경
        null=True
    )
    
    profile_message = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True) #개체가 처음 생성될때 시각으로 설정 
    
    updated_at = models.DateTimeField(auto_now=True) #개체가 저장될때마다 현재 시각으로 설정
    
    is_active = models.BooleanField(
        default=True
        null=False
        )

    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']  #email, 비밀번호, 닉네임은 필수지만 user를 생성할때 이미 email과 비밀번호는 명시

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

"""
참조
https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#substituting-a-custom-user-model
https://docs.djangoproject.com/en/3.2/ref/models/fields/#model-field-types
https://docs.djangoproject.com/en/3.2/topics/db/models/#field-types
"""
