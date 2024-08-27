# Importing the models module from Django to create database models
from django.db import models

# Importing the User model from Django's built-in authentication system
from django.contrib.auth.models import User

# Model to log user login attempts
class UserLoginLog(models.Model):
    # Foreign key to the User model, represents the user who attempted to log in
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Stores the username used during the login attempt
    username = models.CharField(max_length=150)
    
    # Boolean field to indicate whether the login attempt was successful
    success = models.BooleanField(default=False)
    
    # Timestamp of the login attempt, automatically set to the current date and time when the record is created
    timestamp = models.DateTimeField(auto_now_add=True)

    # String representation of the model instance, useful for debugging and logging
    def __str__(self):
        return f"Login attempt by {self.username} at {self.timestamp} - {'Success' if self.success else 'Failure'}"

# Model representing a product in the system
class Product(models.Model):
    # Name of the product
    name = models.CharField(max_length=255)
    
    # Price of the product, stored as a decimal with up to 10 digits and 2 decimal places
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Foreign key to the User model, represents the user who created or is associated with the product
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # String representation of the model instance, returns the name of the product
    def __str__(self):
        return self.name

# Model representing a sale of a product
class Sale(models.Model):
    # Foreign key to the Product model, represents the product being sold
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    # Foreign key to the User model, represents the user who made the sale
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Timestamp of when the sale was made, automatically set to the current date and time when the record is created
    sale_date = models.DateTimeField(auto_now_add=True)
