"""
ViewSets for all 6 Valemis ERP Modules
Provides CRUD operations: GET, POST, PUT, DELETE
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum
from .models import (
    AssetInventory,
    LandInventory,
    LandDocument,
    LandAcquisition,
    LandCompliance,
    Litigation,
    StakeholderNew,
    StakeholderInvolvementNew,
)
from .serializers_new import (
    AssetInventorySerializer,
    AssetInventoryListSerializer,
    LandInventorySerializer,
    LandInventoryListSerializer,
    LandDocumentSerializer,
    LandAcquisitionSerializer,
    LandAcquisitionListSerializer,
    LandComplianceSerializer,
    LandComplianceListSerializer,
    LitigationSerializer,
    LitigationListSerializer,
    StakeholderSerializer,
    StakeholderListSerializer,
    StakeholderInvolvementSerializer,
)


# =============================================================================
# 1. ASSET INVENTORY VIEWSET
# =============================================================================
class AssetInventoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Asset Inventory
    
    GET /api/valemis/assets/ - List all assets
    POST /api/valemis/assets/ - Create new asset
    GET /api/valemis/assets/{id}/ - Retrieve asset
    PUT /api/valemis/assets/{id}/ - Update asset
    DELETE /api/valemis/assets/{id}/ - Delete asset
    GET /api/valemis/assets/summary/ - Get village summary
    """
    queryset = AssetInventory.objects.all()
    serializer_class = AssetInventorySerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return AssetInventoryListSerializer
        return AssetInventorySerializer

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get summary statistics per village"""
        villages = ['Desa Sorowako', 'Desa Magani', 'Desa Wewangriu', 'Desa Nikkel']
        summary = []
        for village in villages:
            assets = self.queryset.filter(village=village)
            summary.append({
                'name': village,
                'totalAssets': assets.count(),
                'totalKK': assets.count(),
                'totalArea': float(assets.aggregate(total=Sum('land_area'))['total'] or 0)
            })
        return Response(summary)


# =============================================================================
# 2. LAND INVENTORY VIEWSET
# =============================================================================
class LandInventoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Land Inventory
    
    GET /api/valemis/lands/ - List all lands
    POST /api/valemis/lands/ - Create new land
    GET /api/valemis/lands/{id}/ - Retrieve land
    PUT /api/valemis/lands/{id}/ - Update land
    DELETE /api/valemis/lands/{id}/ - Delete land
    GET /api/valemis/lands/stats/ - Get statistics
    """
    queryset = LandInventory.objects.prefetch_related('documents').all()
    serializer_class = LandInventorySerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return LandInventoryListSerializer
        return LandInventorySerializer

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get summary statistics"""
        lands = self.queryset
        total = float(lands.aggregate(total=Sum('area'))['total'] or 0)
        milik_vale = float(lands.filter(category='Vale Owned').aggregate(total=Sum('area'))['total'] or 0)
        acquired = float(lands.filter(category='Acquired').aggregate(total=Sum('area'))['total'] or 0)
        
        return Response({
            'total': round(total, 2),
            'milikVale': round(milik_vale, 2),
            'acquired': round(acquired, 2),
            'parcels': lands.count()
        })

    @action(detail=False, methods=['get'])
    def breakdown(self, request):
        """Get breakdown by category and certificate"""
        category_breakdown = []
        for category in ['Vale Owned', 'Acquired', 'IUPK', 'PPKH', 'Operational']:
            items = self.queryset.filter(category=category)
            if items.exists():
                category_breakdown.append({
                    'name': category,
                    'count': items.count(),
                    'totalArea': round(float(items.aggregate(total=Sum('area'))['total'] or 0), 2)
                })

        certificate_breakdown = []
        for cert in ['HGU', 'SHM', 'SHGB', 'Belum Sertifikat']:
            items = self.queryset.filter(certificate=cert)
            if items.exists():
                certificate_breakdown.append({
                    'name': cert,
                    'count': items.count(),
                    'totalArea': round(float(items.aggregate(total=Sum('area'))['total'] or 0), 2)
                })

        return Response({
            'categoryBreakdown': category_breakdown,
            'certificateBreakdown': certificate_breakdown
        })


# =============================================================================
# 3. LAND ACQUISITION VIEWSET
# =============================================================================
class LandAcquisitionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Land Acquisition
    
    GET /api/valemis/acquisitions/ - List all acquisitions
    POST /api/valemis/acquisitions/ - Create new acquisition
    GET /api/valemis/acquisitions/{id}/ - Retrieve acquisition
    PUT /api/valemis/acquisitions/{id}/ - Update acquisition
    DELETE /api/valemis/acquisitions/{id}/ - Delete acquisition
    GET /api/valemis/acquisitions/stats/ - Get statistics
    POST /api/valemis/acquisitions/{id}/mark_bebas/ - Mark as bebas
    """
    queryset = LandAcquisition.objects.all()
    serializer_class = LandAcquisitionSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return LandAcquisitionListSerializer
        return LandAcquisitionSerializer

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get summary statistics"""
        parcels = self.queryset
        return Response({
            'bebas': parcels.filter(status='Bebas').count(),
            'negosiasi': parcels.filter(status='Dalam Negosiasi').count(),
            'belumDiproses': parcels.filter(status='Belum Diproses').count(),
            'total': parcels.count()
        })

    @action(detail=False, methods=['get'])
    def project_summary(self, request):
        """Get summary per project"""
        projects = self.queryset.values('project').distinct()
        summary = []
        for p in projects:
            project_name = p['project']
            parcels = self.queryset.filter(project=project_name)
            bebas = parcels.filter(status='Bebas')
            total_cost = float(parcels.aggregate(total=Sum('biaya_pembebasan'))['total'] or 0)
            
            summary.append({
                'name': project_name.split(' - ')[0] if ' - ' in project_name else project_name,
                'fullName': project_name,
                'totalParcels': parcels.count(),
                'bebas': bebas.count(),
                'progress': round((bebas.count() / parcels.count() * 100) if parcels.count() > 0 else 0),
                'totalCost': total_cost
            })
        return Response(summary)

    @action(detail=True, methods=['post'])
    def mark_bebas(self, request, pk=None):
        """Mark acquisition as bebas"""
        acquisition = self.get_object()
        acquisition.status = 'Bebas'
        acquisition.jumlah_bebas = acquisition.area
        from datetime import date
        acquisition.negotiation_date = date.today().isoformat()
        acquisition.save()
        return Response(LandAcquisitionSerializer(acquisition).data)


# =============================================================================
# 4. LAND COMPLIANCE VIEWSET
# =============================================================================
class LandComplianceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Land Compliance
    
    GET /api/valemis/compliances/ - List all compliances
    POST /api/valemis/compliances/ - Create new compliance
    GET /api/valemis/compliances/{id}/ - Retrieve compliance
    PUT /api/valemis/compliances/{id}/ - Update compliance
    DELETE /api/valemis/compliances/{id}/ - Delete compliance
    GET /api/valemis/compliances/stats/ - Get statistics
    """
    queryset = LandCompliance.objects.all()
    serializer_class = LandComplianceSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return LandComplianceListSerializer
        return LandComplianceSerializer

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get compliance statistics"""
        compliances = self.queryset
        return Response({
            'compliant': compliances.filter(status='Compliant').count(),
            'expiring': compliances.filter(status='Expiring Soon').count(),
            'expired': compliances.filter(status='Expired').count(),
            'pending': compliances.filter(status='No Permit').count()
        })

    @action(detail=False, methods=['get'])
    def breakdown(self, request):
        """Get breakdown by permit type"""
        permit_types = ['IUPK', 'PPKH', 'HGU', 'SHM', 'SHGB', 'IMB', 'UKL-UPL', 'AMDAL']
        breakdown = []
        for ptype in permit_types:
            items = self.queryset.filter(permit_type=ptype)
            if items.exists():
                breakdown.append({
                    'name': ptype,
                    'total': items.count(),
                    'compliant': items.filter(status='Compliant').count(),
                    'problematic': items.filter(status__in=['Expired', 'Expiring Soon']).count()
                })
        return Response(breakdown)

    @action(detail=False, methods=['get'])
    def urgent_renewals(self, request):
        """Get urgent renewals (expiring soon or expired)"""
        urgent = self.queryset.filter(
            status__in=['Expired', 'Expiring Soon']
        ).order_by('expiry_date')[:5]
        return Response(LandComplianceListSerializer(urgent, many=True).data)


# =============================================================================
# 5. LITIGATION VIEWSET
# =============================================================================
class LitigationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Litigation/Claims
    
    GET /api/valemis/litigations/ - List all litigations
    POST /api/valemis/litigations/ - Create new litigation
    GET /api/valemis/litigations/{id}/ - Retrieve litigation
    PUT /api/valemis/litigations/{id}/ - Update litigation
    DELETE /api/valemis/litigations/{id}/ - Delete litigation
    GET /api/valemis/litigations/stats/ - Get statistics
    """
    queryset = Litigation.objects.all()
    serializer_class = LitigationSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return LitigationListSerializer
        return LitigationSerializer

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get litigation statistics"""
        litigations = self.queryset
        return Response({
            'active': litigations.filter(status='Active').count(),
            'underReview': litigations.filter(status='Under Review').count(),
            'resolved': litigations.filter(status='Resolved').count(),
            'dismissed': litigations.filter(status='Dismissed').count(),
            'total': litigations.count()
        })

    @action(detail=False, methods=['get'])
    def breakdown(self, request):
        """Get breakdown by case type"""
        case_types = ['Land Ownership', 'Boundary Dispute', 'Compensation Claim', 'Environmental Claim', 'Others']
        breakdown = []
        for ctype in case_types:
            items = self.queryset.filter(case_type=ctype)
            if items.exists():
                breakdown.append({
                    'name': ctype,
                    'total': items.count(),
                    'active': items.filter(status='Active').count(),
                    'resolved': items.filter(status='Resolved').count()
                })
        return Response(breakdown)

    @action(detail=False, methods=['get'])
    def high_priority(self, request):
        """Get high priority cases"""
        high_priority = self.queryset.filter(
            priority='High'
        ).exclude(status='Resolved')[:5]
        return Response(LitigationListSerializer(high_priority, many=True).data)


# =============================================================================
# 6. STAKEHOLDER VIEWSET
# =============================================================================
class StakeholderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Stakeholder Management
    
    GET /api/valemis/stakeholders/ - List all stakeholders
    POST /api/valemis/stakeholders/ - Create new stakeholder
    GET /api/valemis/stakeholders/{id}/ - Retrieve stakeholder
    PUT /api/valemis/stakeholders/{id}/ - Update stakeholder
    DELETE /api/valemis/stakeholders/{id}/ - Delete stakeholder
    GET /api/valemis/stakeholders/stats/ - Get statistics
    """
    queryset = StakeholderNew.objects.prefetch_related('involvements').all()
    serializer_class = StakeholderSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return StakeholderListSerializer
        return StakeholderSerializer

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get stakeholder statistics"""
        stakeholders = self.queryset
        return Response({
            'total': stakeholders.count(),
            'highInfluence': stakeholders.filter(influence__gte=4).count(),
            'highInterest': stakeholders.filter(interest__gte=4).count(),
            'activeInvolvement': stakeholders.filter(involvements__isnull=False).distinct().count()
        })

    @action(detail=False, methods=['get'])
    def matrix_data(self, request):
        """Get data for influence/interest matrix"""
        stakeholders = self.queryset
        data = []
        for sh in stakeholders:
            data.append({
                'x': sh.influence,
                'y': sh.interest,
                'label': sh.nama,
                'id': sh.id
            })
        return Response(data)


class StakeholderInvolvementViewSet(viewsets.ModelViewSet):
    """API endpoint for Stakeholder Involvements"""
    queryset = StakeholderInvolvementNew.objects.all()
    serializer_class = StakeholderInvolvementSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        stakeholder_id = self.request.query_params.get('stakeholder', None)
        if stakeholder_id:
            queryset = queryset.filter(stakeholder_id=stakeholder_id)
        return queryset
