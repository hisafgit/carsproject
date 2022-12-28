from .models import Car
from rest_framework import viewsets
from .serializers import CarListSerializer
from django_filters import rest_framework as filters


class CarFilterSet(filters.FilterSet):
    brand = filters.CharFilter(field_name="brand__name", lookup_expr='iexact')
    extcolor = filters.CharFilter(field_name="extcolor__color", lookup_expr='iexact')
    trans = filters.CharFilter(field_name='trans__transmission_type', lookup_expr='iexact')

    class Meta:
        model = Car
        fields = ['year', 'brand', 'extcolor']


class CarsFilterView(viewsets.ModelViewSet):
    """
    API endpoint that allows cars to be viewed.
    """
    queryset = Car.objects.all()
    serializer_class = CarListSerializer
    filterset_class =CarFilterSet





