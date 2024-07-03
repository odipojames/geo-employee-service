from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic.base import RedirectView


schema_view = get_schema_view(
    openapi.Info(
        title="GEO employee-service API",
        default_version="v1",
        description="Employee-service for GEOPAY",
        terms_of_service="https://www.geo.com/policies/terms/",
        contact=openapi.Contact(email="contact@geo.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("employees.urls")),
    path("api/v1/", include("advances.urls")),
    path("api/v1/", include("rewards.urls")),
    path(
        "api/v1/docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="api-documentation",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path(
        "",
        RedirectView.as_view(url="api/v1/docs/", permanent=False),
        name="api_documentation",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)