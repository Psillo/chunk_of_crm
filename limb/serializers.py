from rest_framework import serializers

from .models import NaturalPerson, LegalEntity, Department


class NaturalPersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = NaturalPerson
        fields = ['uid', 'phone_number', 'additional_phone_numbers', 'name',
                  'surname', 'patronymic', 'creation_date', 'change_date',
                  'status_change_date', 'status', 'client_type', 'email',
                  'gender', 'time_zone', 'social_networks']


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ['uid', 'name', 'parent_department']


class DepartmentSerializerForLegalEntity(serializers.ModelSerializer):
    natural_person = NaturalPersonSerializer(read_only=True, many=True)

    class Meta:
        model = Department
        fields = ['uid', 'name', 'parent_department', 'natural_person']


class LegalEntitySerializer(serializers.ModelSerializer):
    departments = DepartmentSerializerForLegalEntity(read_only=True, many=True)

    class Meta:
        model = LegalEntity
        fields = ['uid', 'creation_date', 'change_date', 'name',
                  'abbreviation', 'inn', 'kpp', 'departments']
