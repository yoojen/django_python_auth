from django.contrib import admin
from .models import UserModel, OtpModel

admin.register([UserModel, OtpModel])