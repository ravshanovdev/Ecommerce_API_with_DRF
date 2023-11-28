from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Team, Plans
from .serializer import TeamSerializer, UserSerializer, PlansSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, viewsets
from rest_framework.views import APIView
from django import http
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
import stripe
import json


# see all teams
class SeeTeamApiView(ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


# create your team
class TeamApiView(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        obj = serializer.save(created_by=self.request.user)
        obj.members.add(self.request.user)


# get user data and update user data


class UserDetailApiView(APIView):
    # @cache_page(60 * 15)
    # @vary_on_headers('Authorization')
    def get(self, request, pk):  # Renamed to retrieve
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# get your stripe
@api_view(["GET"])
def get_stripe_pub_key(request):
    pub_key = settings.STRIPE_PUB_KEY

    return Response({"pub_key": pub_key})


# get your team
@api_view(['GET'])
def get_my_team(request):
    if request.user.is_authenticated:
        team = Team.objects.filter(created_by=request.user).first()
        if team:
            serializer = TeamSerializer(team)
            return Response(serializer.data)
        else:
            return Response({"message": "Team not found"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"message": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)


# update your team's plan
@api_view(['POST'])
def update_plan(request):
    team = Team.objects.filter(members__in=[request.user]).first()
    plan = request.data['plan']

    print("plan", plan)

    if plan == "free":
        plan = Plans.objects.get(name='free')
    elif plan == "small_team":
        plan = Plans.objects.get(name='small_team')
    elif plan == "big_team":
        plan = Plans.objects.get(name='big_team')

    team.plans = plan
    team.save()

    serializer = TeamSerializer(team)

    return Response(serializer.data)


# add member in your team
@api_view(['POST'])
def add_member(request):
    email = request.data.get('email')
    team_name = request.data.get('team_name')

    try:
        user = User.objects.get(email=email)

        if team_name:
            try:
                team = Team.objects.get(name=team_name)

                team.members.add(user)

                team.save()

                return Response({"message": "Foydalanuvchi muvaffaqiyatli qo'shildi."})
            except Team.DoesNotExist:
                return Response({"error": "Team DoesNotExist."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Team Nomi Kiritilmagan"}, status=status.HTTP_404_NOT_FOUND)

    except User.DoesNotExist:

        return Response({"error": "Foydalanuvchi topilmadi."}, status=status.HTTP_404_NOT_FOUND)


class DestroyTeamApiView(DestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class SeePlansApiView(ListAPIView):
    queryset = Plans.objects.all()
    serializer_class = PlansSerializer


# bu funksiyani stripe da keltirilgan webhook ni kompda

@api_view(["POST"])
def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON in the request body"}, status=400)

    plan = data['plan']

    if plan == 'small_team':
        price_id = settings.STRIPE_PRICE_ID_SMALL_TEAM
    else:
        price_id = settings.STRIPE_PRICE_ID_BIG_TEAM

    team = Team.objects.filter(members__in=[request.user]).first()

    try:
        checkout_session = stripe.checkout.Session.create(
            client_reference_id=team.id,
            success_url="%s?session_id={CHECKOUT_SESSION_ID}" % settings.FRONTEND_WEBSITE_SUCCESS_URL,

            payment_method_types=['card'],
            mode='subscription',
            line_items=[
                {
                    'price': price_id,
                    "quantity": 1
                }
            ]

        )

        return Response({'session_id': checkout_session['id']})
    except Exception as e:
        return Response({"error": str(e)})


# bu funksiyani stripe da keltirilgan webhook ni kompda

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    webhook_key = settings.STRIPE_WEBHOOK_KEY
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', None)
    if sig_header is None:
        return HttpResponse("Missing Stripe Signature Header", status=400)

    event = None

    print("payload", payload)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_key

        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        team = Team.objects.get(pk=session.get('client_reference_id'))
        team.stripe_customer_id = session.get('customer')
        team.stripe_subscription_id = session.get('subscription')
        team.save()

    return HttpResponse(status.HTTP_200_OK)

# frontend bolsa qoshaman
# success_url="%s?session_id={CHECKOUT_SESSION_ID}" % settings.FRONTEND_WEBSITE_SUCCESS_URL,
# cancel_url="%s" % settings.FRONTEND_WEBSITE_CANCEL_URL,
