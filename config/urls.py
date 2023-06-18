from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

swagger_url_patterns = [
    path("", include("apps.clinic.urls")),
]

swagger_schema_view_standard = get_schema_view(
    openapi.Info(
        title="Clinics API",
        default_version="v1",
        description="Clinics API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="shah.shah.22.2001@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    patterns=swagger_url_patterns,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("apps.clinic.urls")),
    re_path(
        r"^swagger/$",
        swagger_schema_view_standard.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)