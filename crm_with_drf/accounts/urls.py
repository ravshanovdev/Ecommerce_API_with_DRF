from django.urls import path
from .views import RegistrationApiView, SeeAllUser

urlpatterns = [
    path('register/', RegistrationApiView.as_view(), ),
    path('see_all_user/', SeeAllUser.as_view(), ),



]

