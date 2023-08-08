from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import FileExtensionValidator
# from django.utils.translation import gettext as _
from django.conf import settings
from django.core.validators import RegexValidator
import uuid


######### LEARNING CRUD APIS WITH DJANGO REST FRAMEWORK ################

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique = True)
    #institute = models.ForeignKey(Institute,on_delete=models.DO_NOTHING)
    # profileImage = models.FileField(upload_to='profileImages/', 
    #                                 validators=[FileExtensionValidator(
    #                                     allowed_extensions=['png','jpg','jpeg','mp4'])], 
    #                                 default='profileImages/profile_default.png',null=True,blank=True)
    
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+255-000-000-000' ")
    # phone_number = models.CharField(validators=[phone_regex], max_length=13, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return "{}".format(self.email)
    

class PCMUserRoles(models.Model):
    # id = models.AutoField(primary_key=True)
    role_unique_id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True,primary_key=True)
    # institute = models.ForeignKey(Institute,on_delete=models.DO_NOTHING)
    role_name = models.CharField(default='', max_length=1600)
    role_description = models.CharField(default='', max_length=1600)
    role_createdby = models.ForeignKey(User, related_name='user_role_creator', on_delete=models.CASCADE)
    role_createddate = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.role_name)

    def get_role_permissions(self):
        return self.user_role_with_permission_role.all()

    class Meta:
        db_table = 'tsms_user_roles'
        ordering = ['-role_createddate']
        verbose_name_plural = "User Roles"


#these permissionsGroup model_name are binded to the ui:
class PCMUserPermissionsGroup(models.Model):
    # primary_key = models.AutoField(primary_key=True)
    # id = models.AutoField(primary_key=True)
    permission_group_unique_id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True,primary_key=True)
    permission_group_name = models.CharField(default='', max_length=1600)
    permission_group_description = models.CharField(default='', max_length=600, null=True)
    permission_group_createdby = models.ForeignKey(User, related_name='permission_group_creator',
                                                   on_delete=models.CASCADE)
    permission_group_createddate = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.permission_group_name, self.permission_group_description)

    class Meta:
        db_table = 'tsms_user_permissions_group'
        ordering = ['-permission_group_createddate']
        verbose_name_plural = "Permission Groups"


#these permissionsGroup model_name are binded to the ui:
class PCMUserPermissions(models.Model):
    # primary_key = models.AutoField(primary_key=True)
    permission_unique_id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True,primary_key=True)
    permission_name = models.CharField(default='', max_length=1600)
    permission_code = models.CharField(default='', max_length=1600)
    permission_group = models.ForeignKey(PCMUserPermissionsGroup, related_name='permission_group',
                                         on_delete=models.CASCADE, null=True)
    permission_createdby = models.ForeignKey(User, related_name='user_permission_creator', on_delete=models.CASCADE)
    permission_createddate = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.permission_name, self.permission_group)

    class Meta:
        db_table = 'tsms_user_permissions'
        ordering = ['-permission_createddate']
        verbose_name_plural = "User Permissions"


class PCMUserRolesWithPermissions(models.Model):
    # primary_key = models.AutoField(primary_key=True)
    role_with_permission_unique_id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True,primary_key=True)
    role_with_permission_role = models.ForeignKey(PCMUserRoles, related_name='user_role_with_permission_role',
                                                  on_delete=models.CASCADE)
    role_with_permission_permission = models.ForeignKey(PCMUserPermissions,
                                                        related_name='user_role_with_permission_permission',
                                                        on_delete=models.CASCADE)
    permission_read_only = models.BooleanField(default=True)
    role_with_permission_createdby = models.ForeignKey(User, related_name='user_role_with_permission_creator',
                                                       on_delete=models.CASCADE)
    role_with_permission_createddate = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'dtp_user_role_with_permissions'
        ordering = ['-role_with_permission_createddate']
        verbose_name_plural = "Roles with Permissions"

class PCMUsersWithPermissions(models.Model):
    # primary_key = models.AutoField(primary_key=True)
    user_with_permission_unique_id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True,primary_key=True)
    user_with_permission_permission = models.ForeignKey(PCMUserPermissions, related_name='user_permission_name', on_delete=models.CASCADE)
    user_with_permission_user = models.ForeignKey(User, related_name='permission_user', on_delete=models.CASCADE)
    user_with_permission_createdby = models.ForeignKey(User, related_name='user_with_permission_creator', on_delete=models.CASCADE)
    user_with_permission_createddate = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'tsms_user_with_permissions'
        ordering = ['-user_with_permission_createddate']
        verbose_name_plural = "Users with Permissions"
        
class PCMUsersWithRoles(models.Model):
    # primary_key = models.AutoField(primary_key=True)
    user_with_role_unique_id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True,primary_key=True)
    user_with_role_role = models.ForeignKey(PCMUserRoles, related_name='user_role_name', on_delete=models.CASCADE)
    user_with_role_user = models.ForeignKey(User, related_name='role_user', on_delete=models.CASCADE)
    user_with_role_createdby = models.ForeignKey(User, related_name='user_with_role_creator', on_delete=models.CASCADE)
    user_with_role_createddate = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'tsms_user_with_roles'
        ordering = ['-user_with_role_createddate']
        verbose_name_plural = "Users with Roles"
    
######### END OF UAA MODELS #############  
    
    
    
class Workshop(models.Model):
    id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True,primary_key=True)
    name = models.CharField(max_length=100,blank=True,null=True)
    email = models.EmailField(max_length=50,blank=True,null=True)
    
    updatedBy = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="user_brnch",blank=True,null=True)
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)
    status= models.BooleanField(default=True)
    
    class Meta:
        ordering =['-createdAt','-updatedAt']
    
    def __str__(self):
        return str(self.name)


class Profile(models.Model):
    id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True,primary_key=True)
    user = models.OneToOneField(User, related_name='profil',on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, related_name='workshop_profile', on_delete=models.CASCADE, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True,null=True)
    dob = models.DateField(null=True,blank=True)

    updatedBy = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="user_profil",blank=True,null=True)
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)
    status= models.BooleanField(default=True)
    
    class Meta:
        ordering =['-createdAt','-updatedAt']
    
    def __str__(self):
        return self.user.email
    
class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploaded_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    prediction_result = models.CharField(max_length=100, blank=True, null=True)
    
    
#           # tuts #               #

class LeadModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    message = models.CharField(max_length=500)
    owner = models.ForeignKey(User, related_name="leads", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    