from django.shortcuts import render,get_object_or_404

# Create your views here.
from rest_framework.generics import GenericAPIView
from .serializers import *
#from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from rest_framework import viewsets,generics,permissions
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token 
# Create your views here.
from knox.models import AuthToken
from knox.views import LoginView as knoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import authentication_classes,permission_classes,api_view
from rest_framework.permissions import IsAuthenticated,IsAdminUser
# from .models import EmalconfirmationToken
# from .utils import send_confirmation_email

from .serializers import ChangePasswordSerializer
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response({'success':'True','message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'success':'False','error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class registerapi(generics.GenericAPIView):
    serializer_class=RegisterSerializer
    def post(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user= serializer.save()
        return Response({'success':'True',
            'status':200,'msg':'created success',
            'data':serializer.data,
            #'token':AuthToken.objects.create(user)[1]
             
        })

class loginapi(knoxLoginView):
    permission_classes = (permissions.AllowAny,)
    def post (self,request,format=None):
         
         serializer=AuthTokenSerializer(data=request.data)
         #serializer.is_valid(raise_exception=False)
        
         if serializer.is_valid():
            user=serializer.validated_data['user']
            login(request,user)
            super(loginapi,self).post(request,format=None)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'success':'True',
                'status':200,'msg':'login success',
                'data':request.data,
                'token':  token.key
                
             })
         else:         
                 return Response({'success':'False','status':400,'error':'There is wrong in Username or password, Please review your data and try again'})
                
         

 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.delete()
            return Response({'success':'True','status':200,'data':'null','message': 'Successfully logged out.'})
        except Exception as e:
            return Response({'success':'False','status':400,'error': str(e)})

 
class UserSerializerlist(APIView ):
  
     def get(self,request):
         users=User.objects.all()
         data=UserSerializer(users,many=True).data
         return Response(data)
    

class UserINFO(APIView): 
     
     def get(self,request,id):
         try:
             users=User.objects.get(id=id)
         except User.DoesNotExist:
             return Response({'success':'False','status':404,'errors':serializer.errors,'msg':'not found'} )
         serializer=UserSerializer(users)
        
         return Response({'success':'True','status':200,'data':serializer.data,'msg':'created success'})
       
 
     def put(self,request,id):
           try:
             users=User.objects.get(id=id)
           except User.DoesNotExist:
             return Response({'success':'False','status':404,'errors':serializer.errors,'msg':'id not found'} )
           serializer=UserSerializer(users,data=request.data)
          
           if serializer.is_valid():
                 serializer.save()
             
                 return Response({'success':'True','status':200,'data':serializer.data,'msg':'Updated successfully'} )
          
        
           return Response({'success':'False','status':404,'errors':serializer.errors,'msg':'Updated failed'} )
          
     def delete(self,request,id):
          try:
             user=User.objects.get(id=id)
          except User.DoesNotExist:
             return Response({'status':404,'errors':serializer.errors,'msg':'id not found'} )
         
          user.delete()
          return Response({'status':200,'msg':'deleted is done'} )





from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import generate_otp, send_otp_email
from .models import *

class LoginWithOTP(APIView):
    def post(self, request):
        email = request.data.get('email', '')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'success':'False','error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        otp = generate_otp()
        user.otp = otp
        user.save()

        send_otp_email(email, otp)
        # send_otp_phone(phone_number, otp)

        return Response({'success':'True','message': 'OTP has been sent to your email.'}, status=status.HTTP_200_OK)


# accounts/views.py

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class ValidateOTP(APIView):
    def post(self, request):
        email = request.data.get('email', '')
        otp = request.data.get('otp', '')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'success':'False','error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if user.otp == otp:
            user.otp = None  # Reset the OTP field after successful validation
            user.save()

            # Authenticate the user and create or get an authentication token
            token, _ = Token.objects.get_or_create(user=user)

            return Response({'success':'True','token': token.key} , status=status.HTTP_200_OK)
        else:
            return Response({'success':'False','error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileSerializerlist(APIView):
    def get(self, request):
        profiles = UserProfile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response({
            'status':200,'msg':'success',
            'data':serializer.data
             
        })
class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = UserProfile.objects.all()
    #permission_classes = [IsAuthenticated]  

class adddepart(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        serializer = departmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
            'status':200,'msg':'created success',
            'data':serializer.data
             
        })
        return Response({
            'status':400,'msg':'failed created',
            'data':serializer.data,
            'errors':serializer.errors
             
        })

class departmentSerializerlist(APIView):
    def get(self, request):
        departments = department.objects.all()
        serializer = departmentSerializer(departments, many=True)
        return Response({
            'status':200,'msg':'success',
            'data':serializer.data
             
        })
    

class departdetails(APIView):
     permission_classes = [IsAdminUser]
     def put(self,request,id):
           try:
             departments=department.objects.get(id=id)
           except department.DoesNotExist:
             return Response({'status':404,'errors':serializer.errors,'msg':'id not found'} )
           serializer=departmentSerializer(departments,data=request.data)
          
           if serializer.is_valid():
                 serializer.save()
             
                 return Response({'status':200,'msg':'Updated successfully'} )
          
        
           return Response({'status':404,'errors':serializer.errors,'msg':'Updated failed'} )
      
     def delete(self,request,id):
          try:
             depart=department.objects.get(id=id)
          except department.DoesNotExist:
             return Response({'status':404,'errors':serializer.errors,'msg':'id not found'} )
        
          depart.delete()
          return Response({'status':200,'msg':'deleted is done'} )

class departmentINFO(APIView): 
     
     def get(self,request,id):
         try:
             departments=department.objects.get(id=id)
         except department.DoesNotExist:
             return Response({'status':404,'errors':serializer.errors,'msg':'not found'} )
         serializer=departmentSerializer(departments)
        
         return Response({'status':200,'data':serializer.data,'msg':'created success'})
     
    
class addproduct(APIView):
      permission_classes = [IsAdminUser]
      def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
            'status':200,'msg':'created success',
            'data':serializer.data
             
        })
        return Response({
            'status':400,'msg':'failed created',
            'data':serializer.data,
            'errors':serializer.errors
             
        })
            
  
class productSerializerlist(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({
            'status':200,'msg':'success',
            'data':serializer.data
             
        })
    
   
class productdetails(APIView):
     permission_classes = [IsAdminUser]
     def put(self,request,id):
           try:
             products=Product.objects.get(id=id)
           except Product.DoesNotExist:
             return Response({'status':404,'errors':serializer.errors,'msg':'id not found'} )
           serializer=ProductSerializer(products,data=request.data)
          
           if serializer.is_valid():
                 serializer.save()
             
                 return Response({'status':200,'msg':'Updated successfully'} )
          
        
           return Response({'status':404,'errors':serializer.errors,'msg':'Updated failed'} )
     
     def delete(self,request,id):
          try:
             product=Product.objects.get(id=id)
          except Product.DoesNotExist:
             return Response({'status':404,'errors':serializer.errors,'msg':'id not found'} )
        
          product.delete()
          return Response({'status':200,'msg':'deleted is done'} )


class productINFO(APIView): 
     
     def get(self,request,id):
         try:
             products=Product.objects.get(id=id)
         except department.DoesNotExist:
             return Response({'status':404,'errors':serializer.errors,'msg':'not found'} )
         serializer=ProductSerializer(products)
        
         return Response({'status':200,'data':serializer.data,'msg':'created success'})
     

     
             


class OfferSerializerlist(APIView):
    def get(self, request):
        Offers = offers.objects.all()
        serializer = offerSerializer(Offers, many=True)
        return Response({
            'status':200,'msg':'success',
            'data':serializer.data
             
        })

    def post(self, request):
        serializer = offerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
            'status':200,'msg':'created success',
            'data':serializer.data
             
        })
        return Response({
            'status':400,'msg':'failed created',
            'data':serializer.data,
            'errors':serializer.errors
             
        })


class OfferINFO(APIView): 
     
     def get(self,request,id):
         try:
             Offers=offers.objects.get(id=id)
         except offers.DoesNotExist:
             return Response({'status':404,'errors':serializer.errors,'msg':'not found'} )
         serializer=offerSerializer(Offers)
        
         return Response({'status':200,'data':serializer.data,'msg':'created success'})
     


     def put(self,request,id):
           try:
             Offers=offers.objects.get(id=id)
           except offers.DoesNotExist:
             return Response({'status':404,'errors':serializer.errors,'msg':'id not found'} )
           serializer=offerSerializer(Offers,data=request.data)
          
           if serializer.is_valid():
                 serializer.save()
             
                 return Response({'status':200,'msg':'Updated successfully'} )
          
        
           return Response({'status':404,'errors':serializer.errors,'msg':'Updated failed'} )
          
     def delete(self,request,id):
          try:
             offer=offers.objects.get(id=id)
          except department.DoesNotExist:
             return Response({'status':404,'errors':serializer.errors,'msg':'id not found'} )
        
          offer.delete()
          return Response({'status':200,'msg':'deleted is done'} )
             





######## new
     
@api_view(['GET'])
def get_carts(request):
    carts = Cart.objects.all()
    serializer = CartSerializer(carts,many=True)
    return Response({'status':200,'data':serializer.data,'msg':'get success'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request,pk):
    cart =get_object_or_404(Cart, id=pk)

    serializer = CartSerializer(cart,many=False)
    return Response({'status':200,'data':serializer.data,'msg':'get success'})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def put_cart(self,request,pk):
           try:
             cart=Cart.objects.get(id=pk)
           except cart.DoesNotExist:
             return Response({'status':404,'errors':serializer.errors,'msg':'id not found'} )
           serializer=CartSerializer(Cart,data=request.data)
          
           if serializer.is_valid():
                 serializer.save()
             
                 return Response({'status':200,'msg':'Updated successfully'} )
          
        
           return Response({'status':404,'errors':serializer.errors,'msg':'Updated failed'} )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def put_cart(request,pk):
    cart =get_object_or_404(Cart, id=pk)
    cart.save()
    serializer = CartSerializer(cart,many=False)
    return Response({'status':200,'msg':'Updated successfully','data':serializer.data})



@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsAdminUser])
def process_cart(request,pk):
    cart =get_object_or_404(Cart, id=pk)
    cart.status = request.data['status']
    cart.save()
     
    serializer = CartSerializer(cart,many=False)
    return Response({'data':serializer.data})



# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def delete_order(request,pk):
#     order =get_object_or_404(Order, id=pk) 
#     order.delete()
      
#     return Response({'details': "order is deleted"})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_cart(request):
    user = request.user 
    data = request.data
    cart_items = data['cart_Items']

    if cart_items and len(cart_items) == 0:
       return Response({'status':404,'errors':serializer.errors,'msg':'no items in the cart'})
    else:
        cart = Cart.objects.create(
            user = user,
        )
        for i in cart_items:
            product = Product.objects.get(id=i['product'])
            item = CartItem.objects.create(
                product= product,
                cart = cart,
                name = product.name,
                quantity = i['quantity'],
                price = i['price'],
                
            )
            product.save()
        serializer = CartSerializer(cart,many=False)
        alaa=serializer.data
        return Response({'status':200,'data':alaa,'msg':'created success'})






















# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_orders(request):
#     orders = Order.objects.all()
#     serializer = OrderSerializer(orders,many=True)
#     return Response({'orders':serializer.data})

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_order(request,pk):
#     order =get_object_or_404(Order, id=pk)

#     serializer = OrderSerializer(order,many=False)
#     return Response({'order':serializer.data})


# @api_view(['PUT'])
# @permission_classes([IsAuthenticated,IsAdminUser])
# def process_order(request,pk):
#     order =get_object_or_404(Order, id=pk)
#     order.status = request.data['status']
#     order.save()
     
#     serializer = OrderSerializer(order,many=False)
#     return Response({'order':serializer.data})


# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def delete_order(request,pk):
#     order =get_object_or_404(Order, id=pk) 
#     order.delete()
      
#     return Response({'details': "order is deleted"})




# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def new_order(request):
#     user = request.user 
#     data = request.data
#     order_items = data['order_Items']

#     if order_items and len(order_items) == 0:
#        return Response({'error': 'No order recieved'},status=status.HTTP_400_BAD_REQUEST)
#     else:
#         total_amount = sum( item['price']* item['quantity'] for item in order_items)
#         order = Order.objects.create(
#             user = user,
#             city = data['city'],
#             zip_code = data['zip_code'],
#             street = data['street'],
#             phone_no = data['phone_no'],
#             country = data['country'],
#             total_amount = total_amount,
#         )
#         for i in order_items:
#             product = Product.objects.get(id=i['product'])
#             item = OrderItem.objects.create(
#                 product= product,
#                 order = order,
#                 name = product.name,
#                 quantity = i['quantity'],
#                 price = i['price']
#             )
            
#             product.save()
#         serializer = OrderSerializer(order,many=False)
#         return Response(serializer.data)