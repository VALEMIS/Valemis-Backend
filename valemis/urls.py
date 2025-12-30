"""
URL configuration for Valemis API
"""
from django.urls import path, include
from rest_framework import routers
from django.apps import apps
from .views import *
from .views_api import (
    AssetInventoryViewSet,
    AssetInventoryDetailViewSet,
    LandInventoryViewSet,
    LandAcquisitionViewSet,
    LandComplianceViewSet,
    LitigationViewSet,
    StakeholderViewSet,
    StakeholderInvolvementViewSet,
)
from .views_census import (
    CensusSurveyViewSet,
    CensusMemberViewSet,
    CensusQuestionViewSet,
)

# Create router and register viewsets
router = routers.DefaultRouter()
app_models = apps.get_app_config("valemis").get_models()

for model in app_models:
    name = model.__name__.lower()
    router.register(name, generate_viewset(model.__name__))
# Register all module viewsets
router.register(r'assets', AssetInventoryViewSet, basename='asset')
router.register(r'asset-details', AssetInventoryDetailViewSet, basename='asset-detail')
router.register(r'lands', LandInventoryViewSet, basename='land')
router.register(r'acquisitions', LandAcquisitionViewSet, basename='acquisition')
router.register(r'compliances', LandComplianceViewSet, basename='compliance')
router.register(r'litigations', LitigationViewSet, basename='litigation')
router.register(r'stakeholders', StakeholderViewSet, basename='stakeholder')
router.register(r'stakeholder-involvements', StakeholderInvolvementViewSet, basename='stakeholder-involvement')
# Register census survey viewsets
router.register(r'census', CensusSurveyViewSet, basename='census')
router.register(r'census-members', CensusMemberViewSet, basename='census-member')
router.register(r'questions', CensusQuestionViewSet, basename='question')

urlpatterns = [
    path("", include(router.urls)),
]

# Try to import analyze endpoint (requires geopandas)
try:
    from .views import api_analyze, tes
    urlpatterns += [
        path("analyze/", api_analyze, name="analyze"),
        path("tes/", tes, name="tes"),
    ]
except ImportError:
    pass  # geopandas not available, skip these endpoints
