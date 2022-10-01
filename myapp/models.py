from enum import unique
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import random


USERTYPE = (
    ("Admin", "Admin"),
    ("Staff", "Staff"),

)   

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.email,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.is_superuser = True
        if user.is_superuser: user.user_type = "Admin"
        user.is_staff = True
        user.save(using=self._db)
        return user

DEVICE_TYPE = (
    ("Guard", "Guard"),
    ("Light", "Light")
)


class MyUser(AbstractBaseUser):
    user_type = models.CharField("User Type", max_length=10, default='Staff', choices=USERTYPE)
    full_name = models.CharField(max_length=100, null=False,blank=False)
    email = models.CharField(max_length=100, null=False,blank=False,unique=True)
    phone_number = models.CharField(max_length=10, null=False,blank=False)
    device_type = models.CharField("Device Type", max_length=10, default='Guard', choices=DEVICE_TYPE)
    device = models.CharField(max_length=100, null=True,blank=True)
    is_superuser = models.BooleanField("Super User", default=False)
    is_staff = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
  

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
    

class InDateTime(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE, related_name="in_date")
    in_date_time = models.DateTimeField()


   

class OutDateTime(models.Model):
    indate = models.OneToOneField(InDateTime,on_delete=models.CASCADE, related_name="out_date")
    out_date_time = models.DateTimeField()


