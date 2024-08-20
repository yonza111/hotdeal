from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/admin/', admin.site.urls),
    path("api/hotdeal/", include('hotdeal.urls')),
    path('api/accounts/', include('allauth.urls')),
    path("api/keyword_manager/", include('keyword_manager.urls')),
    path('api/discord/', include('accounts.urls')),
   
    
]
