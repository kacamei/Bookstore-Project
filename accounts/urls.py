from django.urls import path

from accounts import views



urlpatterns = [
    
    path('register',views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('index', views.index, name='index'),
    path('cart/', views.cart, name="cart"),
    path('check/', views.check, name='check'),
    path('SECONDPAGE', views.SECONDPAGE, name='SECONDPAGE'),
    
    path('update_item/', views.updateItem, name="update_item"),

    path('search/', views.SearchPage, name='search_result'),
    path('upload/', views.upload,name='upload'),
    path('apply/', views.coupon_apply, name='apply'),
    
	
]
