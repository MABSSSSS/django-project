# Importing necessary functions and classes for user authentication and session management
from django.contrib.auth import authenticate, get_user_model, login

# Importing Django REST framework modules for building API views, handling permissions, and returning HTTP responses
from rest_framework import generics, permissions, status  # generics for generic class-based views, permissions for access control, status for HTTP status codes
from rest_framework.response import Response  # To return HTTP responses with data
from rest_framework.views import APIView  # Base class for creating custom API views

# Importing Django's CSRF exemption decorator to allow non-HTML forms like JSON to make POST requests
from django.views.decorators.csrf import csrf_exempt

# Importing a permission class to allow access to any user, authenticated or not
from rest_framework.permissions import AllowAny

# Importing the models from the current app to interact with the database
from .models import Product, Sale

# Importing serializers to convert complex data types to Python datatypes for rendering as JSON
from .serializers import UserSerializer, ProductSerializer, SaleSerializer

# Importing decorators to apply view-level decorators like csrf_exempt to class-based views
from django.utils.decorators import method_decorator

# Importing a shortcut function to get an object from the database or return a 404 error if it doesn't exist
from django.shortcuts import get_object_or_404

# Importing utilities for adding Swagger documentation to views
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi  # For defining schema elements like parameters and responses

# Importing a timezone utility to handle time and date operations
from django.utils import timezone

# Importing a custom model from the shop app to log user login attempts
from shop.models import UserLoginLog

# Getting the user model that is currently active in the Django project (e.g., a custom user model or the default User model)
User = get_user_model()

# -----------------------
# User Views
# -----------------------

# This view handles the creation of new users using a generic CreateAPIView.
# It allows any user (authenticated or not) to create a new account.
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()  # Queryset containing all User instances
    serializer_class = UserSerializer  # Serializer used to handle User data
    permission_classes = [AllowAny]  # Allows any user to access this view

# This view handles user login. It accepts POST requests containing
# a username and password, authenticates the user, logs them in,
# and returns a response indicating the success or failure of the login attempt.
@method_decorator(csrf_exempt, name='dispatch')
class UserLoginView(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            },
            required=['username', 'password'],
        ),
        responses={200: 'Login successful', 400: 'Invalid credentials'}
    )
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to authenticate and log in a user.

        - Extracts the username and password from the request data.
        - Authenticates the user using the provided credentials.
        - Logs the login attempt in the UserLoginLog model, whether successful or not.
        - If the credentials are valid, logs the user in and returns a success message.
        - If the credentials are invalid, returns an error message.

        :param request: The HTTP request object containing user credentials.
        :return: A Response object with a success message or an error message.
        """
        # Extract username and password from request data
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is None:
            # Log failed login attempt
            UserLoginLog.objects.create(username=username, success=False, timestamp=timezone.now())
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Log successful login attempt
        UserLoginLog.objects.create(user=user, username=username, success=True, timestamp=timezone.now())
        
        # Log the user in
        login(request, user)
        
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)


# -----------------------
# Product Views
# -----------------------

# This view handles listing all products and creating new products.
# It uses a generic ListCreateAPIView which provides GET and POST methods.
class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()  # Queryset containing all Product instances
    serializer_class = ProductSerializer  # Serializer used to handle Product data
    permission_classes = [AllowAny]  # Allows any user to access this view


# This view handles retrieving, updating, and deleting individual products.
# It uses an APIView to provide custom behavior for GET, PUT, and DELETE requests.
class ProductDetailView(APIView):
    permission_classes = [AllowAny]  # Allows any user to access this view

    def get(self, request, pk, *args, **kwargs):
        """
        Handle GET requests to retrieve a specific product.

        - Retrieves the product by its primary key (pk).
        - Serializes the product data and returns it in the response.

        :param request: The HTTP request object.
        :param pk: The primary key of the product to retrieve.
        :return: A Response object containing the serialized product data.
        """
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        """
        Handle PUT requests to update a specific product.

        - Retrieves the product by its primary key (pk).
        - Updates the product with the data provided in the request.
        - Serializes the updated product data and returns it in the response.

        :param request: The HTTP request object.
        :param pk: The primary key of the product to update.
        :return: A Response object containing the serialized product data or validation errors.
        """
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """
        Handle DELETE requests to delete a specific product.

        - Retrieves the product by its primary key (pk).
        - Deletes the product from the database.
        - Returns a success message in the response.

        :param request: The HTTP request object.
        :param pk: The primary key of the product to delete.
        :return: A Response object containing a success message.
        """
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({"message": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# -----------------------
# Sale Views
# -----------------------

# This view handles creating new sales using a generic CreateAPIView.
# It allows any user to create a sale, associating a product with a user.
class SaleCreateView(generics.CreateAPIView):
    queryset = Sale.objects.all()  # Queryset containing all Sale instances
    serializer_class = SaleSerializer  # Serializer used to handle Sale data
    permission_classes = [AllowAny]  # Allows any user to access this view


# This view handles retrieving the details of a specific sale.
# It provides a GET method to return the serialized sale data.
class SaleDetailView(APIView):
    permission_classes = [AllowAny]  # Allows any user to access this view

    def get(self, request, pk, *args, **kwargs):
        """
        Handle GET requests to retrieve a specific sale.

        - Retrieves the sale by its primary key (pk).
        - Serializes the sale data and returns it in the response.

        :param request: The HTTP request object.
        :param pk: The primary key of the sale to retrieve.
        :return: A Response object containing the serialized sale data.
        """
        sale = get_object_or_404(Sale, pk=pk)
        serializer = SaleSerializer(sale)
        return Response(serializer.data, status=status.HTTP_200_OK)
