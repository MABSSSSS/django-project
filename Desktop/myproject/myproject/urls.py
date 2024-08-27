# Importing the admin module from Django, which provides an interface to manage models
from django.contrib import admin

# Importing path and include for URL configuration
from django.urls import path, include

# Importing the schema view generator and get_schema function from api_docs for API documentation
from api_docs import schema_view
from api_docs import get_schema

# Importing permissions from the Django REST framework to handle access control
from rest_framework import permissions

# Creating a schema view that allows unrestricted access (anyone can access the API documentation)
schema_view = get_schema(permission_classes=(permissions.AllowAny,))

# Creating a schema view restricted to admin users only (only admins can access the API documentation)
admin_schema_view = get_schema(permission_classes=(permissions.IsAdminUser,))

# Defining the URL patterns for the project
urlpatterns = [
    # URL pattern for the admin interface
    path('admin/', admin.site.urls),

    # URL pattern that includes URLs from the shop application
    path('api/', include('shop.urls')),

    # URL pattern for the Swagger UI view of the API documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # URL pattern for the ReDoc view of the API documentation
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
