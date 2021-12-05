from rest_framework import viewsets, mixins
from django.db.models import Prefetch

from .serializers import (NaturalPersonSerializer, LegalEntitySerializer,
                          DepartmentSerializer)
from .models import NaturalPerson, LegalEntity, Department


class NaturalPersonViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = NaturalPerson.objects.all()
    serializer_class = NaturalPersonSerializer


class LegalEntityViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = LegalEntity.objects.all().prefetch_related(
        Prefetch(
            'departments',
            queryset=Department.objects.prefetch_related('natural_person')
        )
    )  # Неплохо сокращает кол-во запросов
    serializer_class = LegalEntitySerializer


class DepartmentViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
