from django.contrib import admin
from .models import ImageModel,UserAddressModel ,MyUserModel
# Register your models here.
admin.site.register(ImageModel)
admin.site.register(UserAddressModel)
admin.site.register(MyUserModel)