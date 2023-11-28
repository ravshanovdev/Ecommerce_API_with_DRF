from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Client, Note
from .serializer import ClientSerializer, NoteSerializer
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from django.contrib.auth.models import User
from team.models import Team
# Create your views here.
from rest_framework.response import Response
from crm.models import CrmModel
from rest_framework.decorators import api_view
from rest_framework import status, response
from rest_framework.views import APIView
from django import http
from rest_framework.pagination import PageNumberPagination
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

class ClientPagination(PageNumberPagination):
    page_size = 10


class ClientApiView(ListAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    pagination_class = ClientPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ['name', 'contact_person', 'email']


class CreateClientApiView(CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get_queryset(self):

        if self.request.user.is_authenticated:
            return self.queryset.filter(created_by=self.request.user.id)
        else:
            return self.queryset.objects.none()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class UpdateClientApiView(RetrieveUpdateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class NoteApiView(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()

    def get_queryset(self):
        team = Team.objects.filter(members__in=[self.request.user.id]).first()
        client_id = self.request.GET.get('client_id')

        return self.queryset.filter(team=team).filter(client_id=client_id)

    def perform_create(self, serializer):
        team = Team.objects.filter(members__in=[self.request.user.id]).first()

        # Check if 'client' key exists in the request data
        client_id = self.request.data.get('client_id')

        if self.request.user.is_authenticated:
            serializer.save(team=team, created_by=self.request.user, client_id=client_id)
        else:
            return Response('You must login.')


class NoteListModelViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def list(self, request, *args, **kwargs):
        # Customize list behavior here if needed
        return super().list(request, *args, **kwargs)


@api_view(['POST'])
def convert_crm_to_client(request):
    team = Team.objects.filter(members__in=[request.user.id]).first()
    crm_id = request.data.get('crm_id')

    if crm_id is None:
        return Response({"error": "crm_id missing in the request data"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        crm = CrmModel.objects.get(team=team, pk=crm_id)

    except CrmModel.DoesNotExist:
        return Response({"error": "bunday ID ga ega CrmModel aniqlanmadi"}, status=status.HTTP_404_NOT_FOUND)

    client = Client.objects.create(team=team, name=crm.company, contact_person=crm.contact_person,
                                   email=crm.email, phone=crm.phone, web_site=crm.web_site,
                                   created_by=request.user)
    return Response({"message": "CrmModel successfully converted to Client. "})





