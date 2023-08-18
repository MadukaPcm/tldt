from rest_framework import serializers
from . models import UploadedImage,LeadModel,User,PCMUsersWithPermissions
from django.db import models
from django.db.models import fields
from django.contrib.auth import authenticate

class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        # fields = ['image']
        fields = '__all__'
        
#          # tuts #               #
class LeadModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadModel
        fields = '__all__'

#customer serializer...
class CustomSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()   

# user authentication with token..
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email')
        
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','password')
        extra_kwargs = {'password':{'write_only':True}}
        
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],validated_data['email'],validated_data['password'])
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect Credentials passed.')
   
class MyPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PCMUsersWithPermissions
        fields = ('user_with_permission_unique_id','user_with_permission_permission','user_with_permission_user')
          
######### LEARNING CRUD APIS WITH DJANGO REST FRAMEWORK ################
