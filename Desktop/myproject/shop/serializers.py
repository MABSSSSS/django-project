# Importing the serializers module from the Django REST framework to create serializers for models
from rest_framework import serializers

# Importing the Product and Sale models from the current application's models
from .models import Product, Sale

# Importing the User model from Django's built-in authentication system
from django.contrib.auth.models import User

# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    # Meta class to define which model and fields to serialize
    class Meta:
        model = User  # Specifies the User model as the model to be serialized
        fields = ['id', 'username', 'password']  # Fields to be included in the serialized output
        extra_kwargs = {'password': {'write_only': True}}  # Ensure the password is write-only (not returned in GET requests)

    # Overriding the create method to handle user creation, including password hashing
    def create(self, validated_data):
        # Create a new user with the provided validated data and hash the password
        user = User.objects.create_user(**validated_data)
        return user

# Serializer for the Product model
class ProductSerializer(serializers.ModelSerializer):
    # Meta class to define which model and fields to serialize
    class Meta:
        model = Product  # Specifies the Product model as the model to be serialized
        fields = ['id', 'name', 'price', 'user']  # Fields to be included in the serialized output

# Serializer for the Sale model
class SaleSerializer(serializers.ModelSerializer):
    # Meta class to define which model and fields to serialize
    class Meta:
        model = Sale  # Specifies the Sale model as the model to be serialized
        fields = ['id', 'product', 'user', 'sale_date']  # Fields to be included in the serialized output
        read_only_fields = ['sale_date']  # Make the sale_date field read-only (can't be modified through the serializer)
