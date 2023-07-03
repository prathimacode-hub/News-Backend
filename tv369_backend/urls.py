from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg import openapi

from accounts.views import (
    UserDetailsView,
    LogoutViewWithCookieSupport as Logout,
    get_token_verify_view,
    ListAllUserView
)


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema

schema_view = get_schema_view(
    openapi.Info(
        title="tv369 APIs",
        default_version='v1'
    ),
    public=True,
    generator_class=BothHttpAndHttpsSchemaGenerator,
)

api_urlpatterns = [
    path('auth/user/', UserDetailsView.as_view()),
    path('auth/logout/', Logout.as_view()),
    path('auth/token/verify/', get_token_verify_view().as_view()),

    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('accounts/users/', ListAllUserView.as_view()),
    path('news/', include("news.urls"))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_urlpatterns)),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0)),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
