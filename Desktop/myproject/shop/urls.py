# Importing the path function from Django for URL routing
from django.urls import path

# Importing views from the current application for handling requests
from .views import UserCreateView, UserLoginView, ProductListView, ProductDetailView, SaleCreateView, SaleDetailView

# Importing permissions from the Django REST framework to handle access control
from rest_framework import permissions

# Importing the schema view generator from drf_yasg for generating API documentation
from drf_yasg.views import get_schema_view

# Importing openapi module from drf_yasg to define API metadata
from drf_yasg import openapi

# Defining the URL patterns for the application
urlpatterns = [
    # URL pattern for creating a new user
    path('users/create/', UserCreateView.as_view(), name='user-create'),

    # URL pattern for user login
    path('users/login/', UserLoginView.as_view(), name='user-login'),

    # URL pattern for listing all products
    path('products/', ProductListView.as_view(), name='product-list'),

    # URL pattern for retrieving, updating, or deleting a specific product by its primary key (id)
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    # URL pattern for creating a new sale
    path('sales/', SaleCreateView.as_view(), name='sale-create'),

    # URL pattern for retrieving, updating, or deleting a specific sale by its primary key (id)
    path('sales/<int:pk>/', SaleDetailView.as_view(), name='sale-detail'),
]
