from django.urls import path
from .views import *
from . import views

urlpatterns=[
    path('auth/getallUser/',UserSerializerlist.as_view(),name='get'),
    path("auth/detailsUser/<str:id>/",UserINFO.as_view()),
    path('auth/register/',registerapi.as_view(),name='register'),
    path('auth/login/',loginapi.as_view(),name='login'),
    path('auth/logout/',user_logout,name='logout'),
    path('auth/change_password/', change_password, name='change_password'),
    path('auth/login-with-otp/', LoginWithOTP.as_view(), name='login-with-otp'),
    path('auth/validate-otp/', ValidateOTP.as_view(), name='validate-otp'),
    path("profile/<str:pk>/", views.ProfileDetail.as_view()),
    path('listprofile/',ProfileSerializerlist.as_view()), 
    path('depart/getallDepart/', departmentSerializerlist.as_view()),
    path('depart/postDepart/', adddepart.as_view()),
    path('depart/detailsDepart/<int:id>/', departdetails.as_view()),
    #path('product/postproduct/',postProduct, name='postproduct'),
    path('depart/getDepart/<int:id>/', departmentINFO.as_view()),
    path('product/getallProduct/', productSerializerlist.as_view()),
    path('product/getProduct/<int:id>/', productINFO.as_view()),
    path('product/detailsProduct/<int:id>/', productdetails.as_view()),
    path('product/postProduct/', addproduct.as_view()),
    #path('AddCart/', cartSerializerlist.as_view()),
    path('offer/getallOffers/', OfferSerializerlist.as_view()),
    path('offer/detailsOffers/<int:id>/', OfferINFO.as_view()),
    # path('orders/new/', views.new_order,name='new_order'), 
    # path('orders/', views.get_orders,name='get_orders'), 
    # path('orders/<str:pk>/', views.get_order,name='get_order'), 

    #  path('orders/<str:pk>/process/', views.process_order,name='process_order'), 
    #  path('orders/<str:pk>/delete/', views.delete_order,name='delete_order'), 

    path('carts/new/', views.new_cart,name='new_cart'), 
    path('carts/', views.get_carts,name='get_carts'), 
    path('carts/<int:pk>/', views.get_cart,name='get_cart'), 
    path('carts/<int:pk>/cartitems/', views.put_cart,name='put_cartitems'), 
    path('carts/<str:pk>/process/', views. process_cart,name='process_cart'),      
]
