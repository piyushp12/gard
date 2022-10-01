from dataclasses import fields
from rest_framework import serializers
from myapp.models import *

# class BlockchainSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MyUser
#         fields = ['device_id','status']



class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ("__all__")
