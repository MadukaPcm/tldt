from django.urls import path,include
from rest_framework import routers
from knox import views as knox_views
from . import views

#dealing with routers....add()
router = routers.DefaultRouter()
router.register('leads', views.LeadViewset, 'leads')

urlpatterns = [
    #   #tuts #         #
    path('custom/',views.CustomAPIView.as_view()),
    path('api/', include(router.urls)),
    
    # user authentication with token....
    path('auth/', include('knox.urls')),
    path('auth/register', views.SignUpAPI.as_view()),
    path('auth/verify/<str:token>/', views.AccountVerificationView.as_view()),
    path('auth/login', views.SignInAPI.as_view()),
    path('auth/user', views.MainUser.as_view()),
    path('auth/logout',knox_views.LogoutView.as_view(), name="knox_logout"),
    ######### LEARNING CRUD APIS WITH DJANGO REST FRAMEWORK ################
    
    
    
    # path('home/', views.PredictionView, name='main_url'),
    # path('', views.UploadedImageList.as_view(), name='uploaded-image-list'),
    # path('upload-image/', views.ImageUploadView.as_view(), name='upload_image'),
    
]
