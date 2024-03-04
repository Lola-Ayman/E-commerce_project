from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.db import models
from shortuuid.django_fields import ShortUUIDField
class User(AbstractUser):
    id = ShortUUIDField(primary_key=True,max_length=20,length=10,prefix="rest",alphabet="abcdefhgigklmnoqz93801 ", unique=True)
    phone =models.CharField(max_length=11,null=False,default='null')
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)  # Add the otp field here

    # Add custom fields here, if needed

    def __str__(self):
        return self.username
    def profilefun(self):
       profile,created=UserProfile.objects.get_or_create(user=self)
       return profile



class UserProfile(models.Model):
    id=ShortUUIDField(primary_key=True,max_length=20,length=10,prefix="pro",alphabet="abcdefhgigklm93801")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=1000)
    bio = models.CharField(max_length=100)
    image = models.ImageField(upload_to="user_images", default="default.jpg")
    verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.full_name == "" or self.full_name == None:
            self.full_name = self.user.username
        super(UserProfile, self).save(*args, **kwargs)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
        instance.profilefun().save()
   

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

class department(models.Model):
    name= models.CharField(null=False,max_length=50)
    image=models.ImageField(upload_to="departments")




class Product(models.Model):
    name= models.CharField(null=False,max_length=50)
    image=models.ImageField(upload_to="products")
    price=models.FloatField(null=False)
    amount=models.IntegerField(null=False)
    depart=models.ForeignKey(department,on_delete=models.CASCADE,related_name='depart')




class offers(models.Model):
      offer=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='offr')
      the_price_after_discount=models.FloatField()



# class catrpro(models.Model):
#     name= models.CharField(null=False,max_length=50)
#     price=models.FloatField(null=False)
#     amount=models.IntegerField(null=False)
#     #depart=models.ForeignKey(department,on_delete=models.CASCADE,related_name='depart')


# class Cart(models.Model):
#     products = models.ManyToManyField(Product)
#     user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

#     def __str__(self):
#         return self.id




# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, related_name ='items', on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
#     cart = models.ForeignKey(Cart, null=True, on_delete=models.CASCADE,related_name='cartitems')
#     name = models.CharField(max_length=200, default="", blank=False)
#     quantity = models.IntegerField( default=1 )
#     price = models.DecimalField( max_digits=7, decimal_places=2,blank=False )



class CartStatus(models.TextChoices):
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'

class PaymentStatus(models.TextChoices):
    PAID = 'Paid'
    UNPAID = 'Unpaid' 



######## new code cart 
      
class Cart(models.Model):
    payment_status = models.CharField(max_length=30, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    status = models.CharField(max_length=60, choices=CartStatus.choices, default=CartStatus.PROCESSING)
    #id = ShortUUIDField(primary_key=True,max_length=20,length=10,prefix="lola",alphabet="abcdefhgigklmnoqz91471 ", unique=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    createAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
    
    




class CartItem(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    cart = models.ForeignKey(Cart, null=True, on_delete=models.CASCADE,related_name='cartitems')
    name = models.CharField(max_length=200, default="", blank=False)
    quantity = models.IntegerField( default=1 )
    price = models.DecimalField( max_digits=7, decimal_places=2,blank=False )
    

    def __str__(self):
        return self.name



















# class OrderStatus(models.TextChoices):
#     PROCESSING = 'Processing'
#     SHIPPED = 'Shipped'
#     DELIVERED = 'Delivered'

# class PaymentStatus(models.TextChoices):
#     PAID = 'Paid'
#     UNPAID = 'Unpaid' 

# class PaymentMode(models.TextChoices):
#     COD = 'COD'
#     CARD = 'CARD' 

# class Order(models.Model):
#     city = models.CharField(max_length=400, default="", blank=False)
#     zip_code = models.CharField(max_length=100, default="", blank=False)
#     street = models.CharField(max_length=500, default="", blank=False)
#     state = models.CharField(max_length=100, default="", blank=False)
#     country = models.CharField(max_length=100, default="", blank=False)
#     phone_no = models.CharField(max_length=100, default="", blank=False)
#     total_amount = models.IntegerField( default=0 )
#     payment_status = models.CharField(max_length=30, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
#     payment_mode = models.CharField(max_length=30, choices=PaymentMode.choices, default=PaymentMode.COD)
#     status = models.CharField(max_length=60, choices=OrderStatus.choices, default=OrderStatus.PROCESSING)
#     user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
#     createAt = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return str(self.id)
    

# class OrderItem(models.Model):
#     product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
#     order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE,related_name='orderitems')
#     name = models.CharField(max_length=200, default="", blank=False)
#     quantity = models.IntegerField( default=1 )
#     price = models.DecimalField( max_digits=7, decimal_places=2,blank=True  )

#     def __str__(self):
#         return self.name