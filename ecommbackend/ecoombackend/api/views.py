from rest_framework.decorators import api_view
from rest_framework import status 
from rest_framework.response import Response
from pymongo import MongoClient
from rest_framework import  status
from rest_framework.views import APIView
import json
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from .models import MyUserModel
from .serializer import MyUserModelSerializer
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator as token_generator
from .models import ImageModel
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.shortcuts import get_object_or_404


client = MongoClient("localhost" ,27017)
db = client["data"]

collection = db["data"]




# Create your views here.



    
class ProductAPIView(APIView):


    def get(self,request,pk=None):


        single_product_name = request.GET.get('product_name')
        category_name = request.GET.get('category_name')
        
        if (single_product_name is not None) and (category_name is not None) :
            print(single_product_name,'------------ee',category_name)
    
            queryset = collection.find_one({"product_name": single_product_name ,"product_category": category_name})

            if queryset:  # Ensure the product exists
                queryset["_id"] = str(queryset["_id"])  

                response_data = {
                    "product": queryset         
                }
                print(response_data, '----------')
                return Response(response_data, status=status.HTTP_200_OK)

        if pk is None :
            print("if is ----------",pk)
            
            queryset =list(collection.find())

            for item in queryset:
                item["_id"] =  str(item["_id"])
            
         
            response_data = {
                "products": queryset,
                "brands": None
            }
            return Response(response_data,status=status.HTTP_200_OK)

        else:
            cursor = collection.find({"product_category": pk})
            brands_cursor = [
                {"$match": {"product_category": pk}},
                {"$group": {"_id": "null" , "brands" : {"$addToSet" : "$brand"}}},

                
                {"$project": {"brands": 1, "_id": 0}},
                
            ]
            queryset_for_brands = list(collection.aggregate(brands_cursor))
           
            print(queryset_for_brands,'-------------')
            queryset = list(cursor)
            if not queryset:
                return Response({"error": "No products found for this category"}, status=status.HTTP_404_NOT_FOUND)
            for item in queryset:
                item["_id"] = str(item["_id"])  # Convert ObjectId to string

            response_data = {
                "products": queryset,                "brands": queryset_for_brands
            }
            print(response_data,'----------')
            return Response(response_data, status=status.HTTP_200_OK)
    def post(self, request):
        data =  request.data.dict() 

        image_file = request.FILES.get('image') 
        product_name = request.data.get('product_name') 
        product_description  = request.data.get("product_description")
        product_price  = request.data.get("product_price")
        product_category  = request.data.get("product_category")
        image_instance = ImageModel(image_name=product_name, image=image_file)
        image_instance.save()
        image_url = "http://127.0.0.1:8000" + image_instance.image.url
        data = {
            "product_name": product_name,
            "product_price": product_price,
            "product_description": product_description,
            "product_category" :product_category,
            "image_url" : image_url
        }
        result = collection.insert_one(data)

        if result:
            return Response({"message": "Successfully inserted"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
       
        
        


# User Authentication Api 
class RegisterView(APIView):

    def post(self, request):
        serializer = MyUserModelSerializer(data=request.data)

        if serializer.is_valid():
       
            email = serializer.validated_data.get("email")

          
            if MyUserModel.objects.filter(email=email).exists():
                return Response({
                    "message": "User already exists"
                }, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()
            # user.last_login = timezone.now()
            # user.save(update_fields=['last_login'])

            # uid = urlsafe_base64_encode(force_bytes(user.pk))
            # verification_link = f"{settings.DOMAIN_NAME}/verify/{uid}"

            # Optionally send verification email (currently commented out)
            # send_mail(
            #     'Verify your email',
            #     f'Please click the following link to verify your email: {verification_link}',
            #     settings.EMAIL_HOST_USER,
            #     [user.email],
            #     fail_silently=False,
            # )

            return Response({
                'message': 'User registered. Check your email for verification.',
                'status' :  status.HTTP_201_CREATED
                
            }, status=status.HTTP_201_CREATED)

        # Return validation errors if serializer is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Verify Email
class VerifyEmailView(APIView):
    def get(self, request,uid):
        try:
            password  = request.GET.get('password')
            user = get_object_or_404(MyUserModel, pk=uid)
            # if user.password != password:
            #     return Response({'message': 'Email verified successfully!'}, status=status.HTTP_200_OK)


            if token_generator.check_token(user):
                user.is_verified = True
                user.save()
                return Response({'message': 'Email verified successfully!',"status" : status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Login View 
class LoginView(APIView):

    def post(self,request):

        try:

            data = request.data
            username = data.get('username')
            password = data.get('password')
            print(username)
            user = MyUserModel.objects.get(username=username)

            if not check_password(password, user.password):
                return Response({'message': 'Password is Incorrect!'}, status=status.HTTP_400_BAD_REQUEST)

            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            return Response({'message': 'SuccessFully Login!',"username": username,"status" : status.HTTP_200_OK}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
