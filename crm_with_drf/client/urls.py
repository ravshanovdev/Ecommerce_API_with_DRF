from django.urls import path, include
from .views import CreateClientApiView, UpdateClientApiView, ClientApiView, NoteApiView, \
    NoteListModelViewSet, convert_crm_to_client
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('notes', NoteApiView, basename='notes')
router.register('see_notes', NoteListModelViewSet, basename='notes')

urlpatterns = [
    path('', ClientApiView.as_view(), ),
    path('add_client/', CreateClientApiView.as_view(), ),
    path('update_client_data/<int:pk>/', UpdateClientApiView.as_view(), ),
    path('note/', include(router.urls)),
    path('see_notes', include(router.urls)),
    path('convert_crm_to_client/', convert_crm_to_client, ),





]
