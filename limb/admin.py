from django.contrib import admin
from django.db.models import Count

from . import models


@admin.register(models.NaturalPerson)
class NaturalPersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'phone_number', 'additional_phone_numbers',
                    'name', 'surname', 'patronymic', 'creation_date',
                    'change_date', 'status_change_date', 'status',
                    'client_type', 'email', 'gender', 'time_zone',
                    'social_networks')


@admin.register(models.LegalEntity)
class LegalEntityAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'creation_date', 'change_date', 'name',
                    'abbreviation', 'inn', 'kpp')


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'name', 'parent_department',
                    'natural_person_count')
    filter_horizontal = ('legal_entity', 'natural_person')

    @admin.display(description='Кол-во физ. лиц (клиентов)')
    def natural_person_count(self, obj):
        return obj.natural_person_count

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            natural_person_count=Count("natural_person")
        )
        return queryset
