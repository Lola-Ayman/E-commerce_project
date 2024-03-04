from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(User)
admin.site.register(Product)
admin.site.register(department)
#admin.site.register(Cart)