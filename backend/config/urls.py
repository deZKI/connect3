from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import routers
from rest_framework import permissions

from apps.users.api.views import TeammateListView, UsersListView, SpeakersListView

schema_view = get_schema_view(
    openapi.Info(
        title="Connect3 Swagger",
        default_version='v1',
        description="Документация к api Connect3",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
router = routers.DefaultRouter()
router.register(r'teammates', TeammateListView, basename='teammates')
router.register(r'users', UsersListView, basename='users')
router.register(r'speakers', SpeakersListView, basename='speakers')
urlpatterns = [

    path('api/swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
