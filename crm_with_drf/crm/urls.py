from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CrmModelApiView, CreateCrmModelsApiView, UpdateCrmModelApiView, DetailCrmModelApiView


# router = DefaultRouter()
# router.register(r'create_crm_model', CreateCrmModelsApiView, basename='crm_models')
# router.register(r'see_crm_models', CrmModelApiView, basename='crm_models')
# urlpatterns = router.urls


urlpatterns = [
    path('', CrmModelApiView.as_view(), ),
    path('create_model/', CreateCrmModelsApiView.as_view(), ),
    path('update_model/<int:pk>/', UpdateCrmModelApiView.as_view(), ),
    path('detail_crm_model/<int:pk>/', DetailCrmModelApiView.as_view(), ),

]

