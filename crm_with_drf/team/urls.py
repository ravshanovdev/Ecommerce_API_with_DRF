from django.urls import path, include
from .views import TeamApiView, get_my_team, add_member, SeeTeamApiView, UserDetailApiView, \
    DestroyTeamApiView, SeePlansApiView, update_plan, get_stripe_pub_key, create_checkout_session, stripe_webhook
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'add_team', TeamApiView, basename='AddTeam')
# router.register(r'see_team', SeeTeamApiView, basename='SeeTeam')
# urlpatterns = router.urls


urlpatterns = [
    path('', include(router.urls), ),
    # path('add_team/', TeamCreateApiView.as_view(), ),
    path('user_detail/<int:pk>/', UserDetailApiView.as_view(), name='user_detail'),
    path('my_team/', get_my_team, ),
    path('add_member/', add_member, ),
    path('see_team/', SeeTeamApiView.as_view(), ),
    path("destroy_team/<int:pk>/", DestroyTeamApiView.as_view(), ),
    # path('create_plans/', CreatePlanApiView.as_view(), ),
    path('see_plans/', SeePlansApiView.as_view(), ),
    path('update_plan/', update_plan, ),
    path('stripe/get_stripe_pub_key/', get_stripe_pub_key, name='get_stripe_pub_key'),
    path('stripe/create_checkout_session/', create_checkout_session, name='create_checkout_session'),
    path('stripe/webhook/', stripe_webhook, name='stripe_webhook'),







]

