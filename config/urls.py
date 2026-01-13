"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import path, include

# Swagger (drf-spectacular)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # =====================
    # ADMIN
    # =====================
    path('admin/', admin.site.urls),

    # =====================
    # DRF AUTH (browser test uchun)
    # =====================
    path('api-auth/', include('rest_framework.urls')),

    # =====================
    # LOYALTY API
    # =====================
    path('api/loyalty/', include('loyalty.urls')),

    # =====================
    # SWAGGER / OPENAPI
    # =====================
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
]
