from rest_framework import serializers
from .models import  *
class UserSerializer(serializers.ModelSerializer):   
    class Meta:
        username=serializers.CharField(max_length=65,min_length=6)
       # is_email_confirmed=serializers.BooleanField(default=False)
        model=User
        fields=('id','username','email','otp','phone') 
class RegisterSerializer(serializers.ModelSerializer):
            class Meta:
              model=User
              fields=('id','username','email','password','phone')
              extra_kwargs={'password':{'write_only':True}} 
            def create (self,validated_data):
               user=  User.objects.create_user(validated_data['username'],validated_data['email'],validated_data['password']) 
               return user 

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)    


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields ='__all__'
    
    def init(self, *args, **kwargs):
        super(ProfileSerializer, self).init(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method=='POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

class departmentSerializer(serializers.ModelSerializer):
        class Meta:
            model = department
            fields ='__all__'

class ProductSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = '__all__' 


# class cartSerializer(serializers.ModelSerializer):
#         class Meta:
#             model =cart
#             fields ='__all__' 

class offerSerializer(serializers.ModelSerializer):
        class Meta:
            model =offers
            fields ='__all__' 




### new


class CartItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"

class CartSerializer(serializers.ModelSerializer):
    cartitems = serializers.SerializerMethodField(method_name="get_cart_items", read_only=True)
    class Meta:
        model = Cart
        fields = "__all__"

    def get_cart_items(self,obj):
        cart_items = obj.cartitems.all()
        serializer = CartItemsSerializer(cart_items,many=True)
        return serializer.data








# class OrderItemsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = "__all__"

# class OrderSerializer(serializers.ModelSerializer):
#     orderItems = serializers.SerializerMethodField(method_name="get_order_items", read_only=True)
#     class Meta:
#         model = Order
#         fields = "__all__"

#     def get_order_items(self,obj):
#         order_items = obj.orderitems.all()
#         serializer = OrderItemsSerializer(order_items,many=True)
#         return serializer.data 


# class catrproSerializer(serializers.ModelSerializer):
#      class Meta:
#         model = catrpro
#         fields = "__all__"


# class CartSerializer(serializers.ModelSerializer):
#     user= serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#     products = catrproSerializer(many=True , read_only=True)

#     class Meta:
#         model = Cart
#         fields = "__all__"



# class CartItemSerializer(serializers.ModelSerializer):
#     product = ProductSerializer(many=False)
#     sub_total = serializers.SerializerMethodField( method_name="total")
#     class Meta:
#         model= OrderItem
#         fields = ["id", "orders", "product", "quantity", "sub_total"]
        
    
#     def total(self, cartitem:OrderItem):
#         return cartitem.quantity * cartitem.product.price
    

# class AddCartItemSerializer(serializers.ModelSerializer):
#     product_id = serializers.UUIDField()
    
#     def validate_product_id(self, value):
#         if not Product.objects.filter(pk=value).exists():
#             raise serializers.ValidationError("There is no product associated with the given ID")
        
#         return value
    
#     def save(self, **kwargs):
#         cart_id = self.context["cart_id"]
#         product_id = self.validated_data["product_id"] 
#         quantity = self.validated_data["quantity"] 
        
#         try:
#             cartitem = OrderItem.objects.get(product_id=product_id, cart_id=cart_id)
#             cartitem.quantity += quantity
#             cartitem.save()
            
#             self.instance = cartitem
            
        
#         except:
            
#             self.instance = OrderItem.objects.create(cart_id=cart_id, **self.validated_data)
            
#         return self.instance
         

#     class Meta:
#         model = OrderItem
#         fields = ["id", "product_id", "quantity"]






# class CartSerializer(serializers.ModelSerializer):
#     id = serializers.UUIDField(read_only=True)
#     items = CartItemSerializer(many=True, read_only=True)
#     grand_total = serializers.SerializerMethodField(method_name='main_total')
    
#     class Meta:
#         model = cart
#         fields = ["id", "items", "grand_total"]
        
    
    
#     def main_total(self, cart: cart):
#         items = cart.items.all()
#         total = sum([item.quantity * item.product.price for item in items])
#         return total
        