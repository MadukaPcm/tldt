from django.shortcuts import render,HttpResponse
from rest_framework import serializers,viewsets,permissions,generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib import auth 
from knox.models import AuthToken
from . serializers import *
from . models import *

from django.core.mail import send_mail
from django.conf import settings


#           # tuts #               #
class LeadViewset(viewsets.ViewSet):
    serializer_class = LeadModelSerializer
    permission_classes = [
        # permissions.IsAuthenticated
    ]
    
    # def get_queryset(self):
    #     return self.request.user.leads.all()
    
    def list(self, request):
        lead = LeadModel.objects.all()
        serializer = LeadModelSerializer(lead, many=True)
        return Response(serializer.data)
    
    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)
    
    #  def create(self, request):
    #     serializer = CollageSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    def create(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        message = request.data.get('message')
        owner = request.data.get('owner')
        # owner = request.user.id
        
        if name and owner:
            try:
                owner_id = int(owner)  # Convert owner to integer
            except ValueError:
                return Response({'errors': 'Invalid owner value'}, status=status.HTTP_400_BAD_REQUEST)

            lead = LeadModel.objects.create(name=name,email=email,message=message,owner_id=owner_id)
            serializer = LeadModelSerializer(lead)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            errors = {'errors':'Missing or invalid data'}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    

# for customer serializer for getting data...
class CustomAPIView(APIView):
    def post(self, request):
        serializer = CustomSerializer(data=request.data)
        if serializer.is_valid():
            name = request.data.get('name')
            email = request.data.get('email')
            
            #you can now perform additional processing here....
            
            response_data = {
                'message': 'Data posted succesfully',
                'name':name,
                'email':email
            }
            return Response(response_data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# user authentication with token....
class SignUpAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = AuthToken.objects.create(user)
        
        #sending email.verification
        # user_instance = user.instance
        # send_verification_email(user_instance.email,token)
        
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token":token[1]
        })
        
def send_verification_email(email,token):
    subject = 'Verify your account'
    message = f'click the link to verify your account: {settings.CLIENT_URL}/verify/{token}'
    from_email = settings.DEFAULT_FROM_EMAIL 
    recepient_list = [email]
    
    send_mail(subject,message,from_email,recepient_list)
    
#Verification view. 
class AccountVerificationView(generics.GenericAPIView):
    def get(self,request,token):
        try:
            token_obj = AuthToken.objects.get(token_key=token)
            user = token_obj.user 
            user.is_active = True 
            user.save()
            token_obj.delete()
            return Response({'message':'Account verified successfully'}, status=status.HTTP_200_OK)
        except AuthToken.DoesNotExist:          
            return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class SignInAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data 
        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            "token":AuthToken.objects.create(user)[1]
        })
        
class MainUser(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user
    
######### LEARNING CRUD APIS WITH DJANGO REST FRAMEWORK ################







































# #my imports bro 
# import sys
# import os
# import glob
# import re
# import numpy as np
# import tensorflow as tf

# # from tensorflow.compat.v1 import ConfigProto
# # from tensorflow.compat.v1 import InteractiveSession

# # config = ConfigProto()
# # config.gpu_options.per_process_gpu_memory_fraction = 0.5
# # config.gpu_options.allow_growth = True
# # session = InteractiveSession(config=config)
# # Keras
# # from tensorflow.keras.applications.resnet50 import preprocess_input
# # from tensorflow.keras.models import load_model
# # from tensorflow.keras.preprocessing import image


# #api imports.............add()
# from rest_framework.views import APIView
# from rest_framework.parsers import MultiPartParser
# from rest_framework.response import Response
# # from .serializers import ImageUploadSerializer
# import base64
# from rest_framework.decorators import parser_classes

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import io


# import cv2
# from io import BytesIO
# from PIL import Image


# from django.conf import settings

# # MODEL_PATH ='model_inception.h5'
# # Load your trained model
# # model = load_model(MODEL_PATH)


# # Create your views here.
# def MainView(request):
    
   
#     dk = str(model.summary())
    
#     # print("This is model history"+ dk)
    
#     return HttpResponse("Main page.")

# from rest_framework import generics
# from .models import UploadedImage
# from .serializers import UploadedImageSerializer

# class UploadedImageList(generics.ListAPIView):
#     queryset = UploadedImage.objects.all()
#     serializer_class = UploadedImageSerializer
    
    
# import os
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.conf import settings
# from .models import UploadedImage
# from .serializers import UploadedImageSerializer

# class ImageUploadView(APIView):
#     def post(self, request):
#         image_serializer = UploadedImageSerializer(data=request.data)

#         if image_serializer.is_valid():
#             image_serializer.save()
#             uploaded_image = image_serializer.instance

#             # Get the path of the uploaded image
#             image_path = os.path.join(settings.MEDIA_ROOT, str(uploaded_image.image))

#             # Use the image_path for prediction using the model file
#             preds = model_predict(image_path, model)
#             result=preds
    
#             print("The predicted result is: "+ result)

#             # Save the prediction result to the model
#             uploaded_image.prediction_result = result
#             uploaded_image.save()

#             return Response({'rr': result}, status=status.HTTP_201_CREATED)
#         else:
#             return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# def PredictionView(request):
    
#     # Save the file to ./uploads
#     # basepath = os.path.dirname(__file__)
#     # file_path = os.path.join(
#     #     basepath, 'uploads', secure_filename(f.filename))
#     # f.save(file_path)

#     # Get the path to the image file in the media folder
#     file_path = os.path.join(settings.MEDIA_ROOT, 'leaf/login.png')
    
#     # Make prediction
#     preds = model_predict(file_path, model)
#     result=preds
    
#     print("The predicted result is: "+ result)
#     return HttpResponse(result)



# def model_predict(img_path, model):
#     print(img_path)
#     img = image.load_img(img_path, target_size=(224, 224))

#     # Preprocessing the image
#     x = image.img_to_array(img)
#     # x = np.true_divide(x, 255)
#     ## Scaling
#     x=x/255
#     x = np.expand_dims(x, axis=0)
   

#     # Be careful how your trained model deals with the input
#     # otherwise, it won't make correct prediction!
#    # x = preprocess_input(x)

#     preds = model.predict(x)
#     preds=np.argmax(preds, axis=1)
#     if preds==0:
#         preds="Bacterial spot"
#     elif preds==1:
#         preds="Early blight"
#     elif preds==2:
#         preds="Late blight"
#     elif preds==3:
#         preds="Leaf Mold"
#     elif preds==4:
#         preds="Septoria leaf spot"
#     elif preds==5:
#         preds="Spider mites Two spotted spider mite"
#     elif preds==6:
#         preds="Target Spot"
#     elif preds==7:
#         preds="Tomato Yellow Leaf Curl Virus"
#     elif preds==8:
#         preds="Tomato mosaic virus"
#     else:
#         preds="Healthy"
        
#     return preds


