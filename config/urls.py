"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Swagger (drf-spectacular)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # =====================
    # ADMIN PANEL
    # =====================
    path('admin/', admin.site.urls),

    # =====================
    # AUTH (REGISTER / LOGIN / JWT)
    # =====================
    path('api/auth/', include('accounts.urls')),

    # =====================
    # LOYALTY MODULE API
    # =====================
    path('api/loyalty/', include('loyalty.urls')),

    # =====================
    # SWAGGER / OPENAPI
    # =====================
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

# =====================
# STATIC FILES (ADMIN CSS)
# =====================
# FAQAT LOCALDA (DEBUG=True) ishlatiladi
# Render’da collectstatic orqali serve bo‘ladi

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
