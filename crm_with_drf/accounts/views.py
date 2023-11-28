from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from client.serializer import UserSerializer


class RegistrationApiView(APIView):

    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        email = request.data["email"]
        user = User(username=username, email=email)
        user.set_password(password)

        user.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "status": "success",
                "user_id": user.id,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        )


class SeeAllUser(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer





