from django.contrib import admin
from django.urls import path, include 
from .views import *

urlpatterns = [
    path('', index_page, name='index_page_url'),
    path('men/', men_page, name='men_url'),
    path('detail/<int:pk>/comment/<int:id>/delete/', comment_delete, name="comment_delete_url"),
    path('detail/<int:pk>/comment/<int:id>/', comment_update, name='comment_update_url'),
    path('detail/<int:pk>/', get_detail, name='get_detail_url'),
    path('product/<str:slug>/', get_product, name='get_product_url'),
    path('women/', women_page, name='women_url'),

]