from django.urls import path

from .views import *

urlpatterns = [
    path("", ProductListView.as_view(), name="home"),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
    path("profile/<int:pk>/", Profile.as_view(), name="profile"),
    path("product/add/", ProductAppend.as_view(), name="append"),
    path("product/about/<int:pk>/", ProductAbout.as_view(), name="about"),
    path("product/change/<int:pk>", ProductUpdate.as_view(), name="change_product"),
    path("product/buy/<int:pk>", ProductBuy.as_view(), name="buy_product"),
    path("user/purchases/", PurchasesList.as_view(), name="purchases_list"),
    path("user/return/<int:pk>", Returns.as_view(), name="return"),
]