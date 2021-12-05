from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import NaturalPersonViewSet, LegalEntityViewSet, DepartmentViewSet


app_name = 'limb'
router = DefaultRouter()
router.register('natural_persons', NaturalPersonViewSet, 'natural_persons')
router.register('legal_entity', LegalEntityViewSet, 'legal_entity')
router.register('department', DepartmentViewSet, 'department')


urlpatterns = [
    path('api/', include(router.urls))
]
