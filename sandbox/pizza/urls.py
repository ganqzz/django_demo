from django.urls import path

from . import views

app_name = 'pizza'  # application namespace

urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.list_order, name='list'),
    path('order/', views.order, name='order'),
    path('order_pizza/', views.order_pizza, name='order-pizza'),
    path('order/<int:pk>/', views.detail, name='detail'),
    path('order/<int:pk>/delete/', views.delete, name='delete'),
]
