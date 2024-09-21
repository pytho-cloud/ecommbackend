from django.db import models

# Create your models here.
class ImageModel(models.Model):

    image_name  = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/")


    def __str__(self) -> str:
        return self.image_name
    
    

class MyUserModel(models.Model):

    username = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    date = models.DateField(auto_created=True,null=True)
    phone = models.CharField(max_length=10,null=True,blank=True)
    alternate_phone = models.CharField(max_length=10,null=True,blank=True)
    last_login = models.DateTimeField(null=True, blank=True) 

    def __str__(self) -> str:
        return self.username
    
class UserAddressModel(models.Model):

    user = models.ForeignKey(MyUserModel, on_delete=models.SET_NULL, null=True, related_name='addresses')
    address = models.TextField()
    last_update = models.DateField()


    def __str__(self) -> str:
        return self.address 




