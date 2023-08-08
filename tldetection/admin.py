from django.contrib import admin
from . models import UploadedImage,User,PCMUserRoles,PCMUserPermissionsGroup,PCMUserPermissions,PCMUserRolesWithPermissions,PCMUsersWithPermissions,PCMUsersWithRoles,Workshop,Profile,LeadModel

# UAA-Models.
admin.site.register(User)
admin.site.register(PCMUserRoles)
admin.site.register(PCMUserPermissionsGroup)
admin.site.register(PCMUserPermissions)
admin.site.register(PCMUserRolesWithPermissions)
admin.site.register(PCMUsersWithPermissions)
admin.site.register(PCMUsersWithRoles)

#Other - Models.
admin.site.register(LeadModel)
admin.site.register(UploadedImage)
admin.site.register(Workshop)
admin.site.register(Profile)
