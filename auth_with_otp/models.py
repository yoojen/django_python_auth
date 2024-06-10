from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from random import randint
from django.utils import timezone

class UserModelManager(BaseUserManager):

    def create_user(self, phone_number, **extra_fields):
        if not phone_number:
            raise ValueError("Phone number is required")
        
        extra_fields.setdefault('is_active', False)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.save()
        return user
    
    def create_superuser(self, phone_number, password, **extra_fields):

        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if not phone_number:
            raise ValueError("Phone number is required")
        if not extra_fields.get('is_superuser'):
            raise ValueError("is_superuser must be True")
        if not extra_fields.get('is_staff'):
            raise ValueError("is_staff must be True")
        user = self.create_user(phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    

class UserModel(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=13, unique=True)
    # password = models.CharField(null=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserModelManager()


class OtpModel(models.Model):
    user=models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='user')
    otp = models.CharField(max_length=6, unique=True)
    otp_expiry=models.DateTimeField(null=True)
    max_try = models.PositiveBigIntegerField(default=3)
    attempt_timeout = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_otp(self):
        """Generate otp token and save it to the database"""
        self.otp = randint(100000, 999999)
        self.otp_expiry = timezone.now() + timedelta(minutes=5)
        self.max_try = self.max_try - 1
        self.save()
        return self.otp
    
    def verify_otp(self, otp):
        """Verify otp entered by the user"""
        if self.max_try <= 0:
           self.attempt_timeout = timezone.now() + timedelta(hours=1)
           raise ValueError("You've attempted more than 3 times, try again after 1hr")
        if self.otp_expiry < timezone.now():
            raise ValueError("Your OTP has been expired, try to regenerate new one")
        self.otp = None
        return otp == self.otp
    
    def regenerate_otp(self, otp):
        """This method generates new otp to sent to the user"""
        self.otp = randint(100000, 999999)
        self.otp_expiry = timezone.now() + timedelta(minutes=10)
        self.max_try = 3
        self.save()
        return self.otp