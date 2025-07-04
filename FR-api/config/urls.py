"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

# urlpatterns = [
#     path('api/users/', include('users.urls')),
#     path('api/employees/', include('employees.urls')),
#     path('api/persons/', include('persons_of_interest.urls')),
#     path('api/identified/', include('identified.urls')),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/employees/', include('employees.urls')),
    path('api/poi/', include('persons_of_interest.urls')),
    # path('api/identified/', include('identified.urls')),
    path('api/suspected/', include('suspected.urls')),
    # path('api/ai/', include('ai_sync.urls')),
    path('api/zones/', include('zones.urls')),
    path('api/cameras/', include('cameras.urls')),


    # OpenAPI schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Swagger UI
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # ReDoc (optional alternative to Swagger)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)