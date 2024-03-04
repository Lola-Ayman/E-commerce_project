"""
URL configuration for e_commerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin 
from django.urls import path,include 
from drf_yasg import openapi 
from drf_yasg.views import get_schema_view 
from app1 import views 
from rest_framework.routers import DefaultRouter 
#from app1.views import CartViewSet
router=DefaultRouter() 
#router.register(r'carts', CartViewSet)
# router.register('cart',views.CartViewSet,basename='cart') 
# router.register('cartitem',views.CartItemViewSet,basename='cartitem') 
schema_view = get_schema_view( 
    openapi.Info( 
        title="Shopping API", 
        default_version="v1", 
        description="Graduation API v1", 
        terms_of_service="", 
    ), 
    public=True, 
) 
 
urlpatterns = [ 
    path('admin/', admin.site.urls), 
    path('',include('app1.urls')), 
    #path('cart',include(router.urls)) , 
    path( 
        "", 
        schema_view.with_ui("swagger", cache_timeout=0), 
        name="v1-schema-swagger-ui", 
    ), 
    path( 
        "", 
        schema_view.with_ui("redoc", cache_timeout=0), 
        name="schema-redoc", 
    ), 
] 
from django.conf.urls.static import static 
from django.conf import settings 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
