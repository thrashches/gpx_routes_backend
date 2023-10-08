from django.urls import re_path, path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions



urlpatterns = []


schema_view = get_schema_view(
    openapi.Info(
        title="GPX API",
        default_version="v1",
        description="GPX API Swagger & redoc documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@admin.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[path("api/v1/", include("api.v1.urls"))],
)

urlpatterns += [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]

