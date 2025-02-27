from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from notifications.routing import websocket_urlpatterns
from users import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Sales & Trading API",
        default_version='v1',
        description="Документация API для системы продаж и трейдинга",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # JWT Authentication
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # API routes
    path("api/users/", include("users.urls")),
    path("api/products/", include("products.urls")),
    path("api/trading/", include("trading.urls")),
    path("api/analytics/", include("analytics.urls")),

    # Swagger documentation
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("swagger.json/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
]

urlpatterns += websocket_urlpatterns
