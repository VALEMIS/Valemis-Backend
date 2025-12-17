"""
URL configuration for Valemis API
"""
from django.urls import path, include
from rest_framework import routers
from .views_api import (
    AssetInventoryViewSet,
    LandInventoryViewSet,
    LandAcquisitionViewSet,
    LandComplianceViewSet,
    LitigationViewSet,
    StakeholderViewSet,
    StakeholderInvolvementViewSet,
)

# Create router and register viewsets
router = routers.DefaultRouter()

# Register all module viewsets
router.register(r'assets', AssetInventoryViewSet, basename='asset')
router.register(r'lands', LandInventoryViewSet, basename='land')
router.register(r'acquisitions', LandAcquisitionViewSet, basename='acquisition')
router.register(r'compliances', LandComplianceViewSet, basename='compliance')
router.register(r'litigations', LitigationViewSet, basename='litigation')
router.register(r'stakeholders', StakeholderViewSet, basename='stakeholder')
router.register(r'stakeholder-involvements', StakeholderInvolvementViewSet, basename='stakeholder-involvement')

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
