from django_filters.rest_framework import FilterSet
from vaccine.models import Vaccine


class VaccineFilter(FilterSet):
    class Meta:
        model = Vaccine
        fields = {
            'price': ['gt', 'lt']
        }