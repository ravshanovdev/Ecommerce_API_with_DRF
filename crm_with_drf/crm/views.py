from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from .models import CrmModel
from .serializer import CrmModelSerializer
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers


class CrmModelPagination(PageNumberPagination):
    page_size = 2


class CrmModelApiView(ListAPIView):
    serializer_class = CrmModelSerializer
    queryset = CrmModel.objects.all()
    pagination_class = CrmModelPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ['id', 'company', 'contact_person', 'email']


class CreateCrmModelsApiView(CreateAPIView):
    queryset = CrmModel.objects.all()
    serializer_class = CrmModelSerializer

    def get_queryset(self):

        if self.request.user.is_authenticated:
            return self.queryset.filter(created_by=self.request.user.id)
        else:
            return self.queryset.objects.none()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class UpdateCrmModelApiView(RetrieveUpdateAPIView):
    queryset = CrmModel.objects.all()
    serializer_class = CrmModelSerializer

    def perform_update(self, serializer):
        obj = self.get_object()

        member_id = self.request.data['assigned_to']

        if member_id:
            user = User.objects.get(pk=member_id)
            serializer.save(assigned_to=user)
        else:
            serializer.save()


class DetailCrmModelApiView(RetrieveUpdateAPIView):

    queryset = CrmModel.objects.all()
    serializer_class = CrmModelSerializer
