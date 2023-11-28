
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/crm/', include('crm.urls')),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/token/', include('djoser.urls.authtoken')),
    path('api/v1/team/', include('team.urls')),
    path('api/v1/clients/', include('client.urls')),

    

]
