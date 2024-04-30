from django.db import models
from django_filters import rest_framework as filters
from core.models import User

class StudentFilter(filters.FilterSet):
    username = filters.CharFilter(method='filter_by_name')

    class Meta:
        model = User
        fields = ['username']

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(
            models.Q(username__icontains=value) |
            models.Q(first_name__icontains=value) |
            models.Q(last_name__icontains=value)
        )

