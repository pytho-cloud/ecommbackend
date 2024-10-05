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
from .models import MyUserModel ,UserAddressModelData ,UserAddressModel
from .serializer import MyUserModelSerializer  ,MyUserModelSerializerData ,UserDataSerilizer ,UserAddressSerializer 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator as token_generator
from .models import ImageModel
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import datetime
from bson import ObjectId


client = MongoClient("localhost" ,27017)
db = client["data"]

collection = db["data"]

collection_user = db["user"]




# Create your views here.



    
class ProductAPIView(APIView):


    def get(self,request,pk=None):
        print("this is api is working0--------" )


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
                item["_id"] = str(item["_id"]) 

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
       
        
        


#Home Page Items Api 

class HomeProductView(APIView):

   

    def get(self, request):

        queryset =list(collection.find().limit(3))
        print("this is api is working" )
        for item in queryset:
            item["_id"] =  str(item["_id"])

        response_data = {
                "products": queryset,
                
            }
        
        return Response(response_data,status=status.HTTP_200_OK)
        

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
            print(username,"data is coming ")
            user = MyUserModel.objects.get(email=username)

            if not check_password(password, user.password):
                return Response({'message': 'Password is Incorrect!'}, status=status.HTTP_400_BAD_REQUEST)

            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            return Response({'message': 'SuccessFully Login!',"username": user.name ,"email" : user.email,"status" : status.HTTP_200_OK}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)




class UserDataApiView(APIView):

    def get(self, request):
        try:
            
            print(request.query_params)
            username = request.query_params.get('username')
            email = request.query_params.get('email')
            print(username ,email,"---------------------data")
            if not username or not email:
                return Response({'error': 'Missing username or email'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = MyUserModel.objects.filter( email=email,name=username).first()
            print(user,"-------")
            if user is not None:
                user_serialier = MyUserModelSerializerData(user)
                print(user_serialier.data,"ssss")
           
                return Response({'data': 'Successfully Logged In!', "username": username, "data": user_serialier.data}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


    def post(self, request):
            try:
                # Extract the relevant fields to identify the user
                name = request.data.get('name')
                email = request.data.get('email')
                print(request.data,"ddddddddddddd")
                # print(name ,"user is coming ")

                if not name or not email:
                    return Response({'error': 'Missing username or email'}, status=status.HTTP_400_BAD_REQUEST)

                # Fetch the existing user
                user = MyUserModel.objects.filter(name=name, email=email).first()
                print(user,"my user")
                if user == None :
                    print("-----nonor")
                if user:
                    print("user is not nonw")
                    userdata_serializer = UserDataSerilizer(user, data=request.data, partial=True)  
                   
                  
                    if userdata_serializer.is_valid():
                        userdata_serializer.save()  # Save the updated user data
                        return Response({
                            'message': 'User data updated successfully',
                            'data': userdata_serializer.data
                        }, status=status.HTTP_200_OK)
                    else:
                        # Return validation errors if any
                        return Response({
                            'errors': userdata_serializer.errors
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # Return error if user does not exist
                    return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            







class UserDataForAddressApiView(APIView):

    def get(self, request):
        try:
            
            
            address = request.query_params.get('address')
            email = request.query_params.get('email')
            print("this is email " , email)
            if not email:
                return Response({'error': 'Missing username or email'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = UserAddressModelData.objects.filter(user_email = email)

            if user is not None:
                user_serialier = UserAddressSerializer(user,many=True)
                print(user_serialier.data,"this is mydata after serialized ")
           
                return Response({'data': 'Successfully Logged In!', "data": user_serialier.data}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


    def post(self, request):
        try:
            print("This is my data:", request.data)
            
            address = request.data.get('address')
            email = request.data.get('email')
        
            if not email:
                return Response({'error': 'Missing email'}, status=status.HTTP_400_BAD_REQUEST)

          
            user_address = UserAddressModelData(user_email=email, address=address)
            user_address.save() 
            return Response({
                "message": "Address successfully added."
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self, request):
            try:
                email = request.data.get('email')
                id = request.data.get('id')

                if not email or not id:
                    return Response({'error': 'Missing email or id'}, status=status.HTTP_400_BAD_REQUEST)

                # Filter and delete the address for the user
                user_address = UserAddressModelData.objects.filter( id= id,user_email=email)

                if user_address.exists():
                    user_address.delete()
                    return Response({"message": "Address successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({'error': 'Address not found for this user'}, status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class SaveWishListView(APIView):

    def get(self, request,pk):
     
        data = list(collection_user.find({"username": pk}))
        for item in data:
            item['_id'] = str(item['_id']) 
        
        return Response({"data": data}, status=status.HTTP_200_OK) 

    def post(self, request):
        data = request.data
        try:
            collection_user.insert_one(data)
            return Response({"status" :status.HTTP_201_CREATED})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self, request, pk):
        try:
            result = collection_user.delete_one({"_id": ObjectId(pk)})
            
            return Response({"status": status.HTTP_200_OK, "message": "Deleted successfully."})
            
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)