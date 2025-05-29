from django.http import HttpResponseRedirect
from django.urls import path, include
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Shopping & Pantry API",
      default_version='v1',
      description="API for managing users, shopping lists, and pantry items",
      terms_of_service="https://www.example.com/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

def root_redirect(request):
    return HttpResponseRedirect('/swagger/')  # Redirect root to Swagger docs

urlpatterns = [
    path('', root_redirect),  # Redirect root URL to /swagger/
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
