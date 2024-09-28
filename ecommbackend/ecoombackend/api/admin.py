from django.contrib import admin
from .models import ImageModel,UserAddressModelData ,MyUserModel
# Register your models here.
admin.site.register(ImageModel)
admin.site.register(UserAddressModelData)
admin.site.register(MyUserModel)