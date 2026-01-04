"""
API Views for Census Survey LARAP
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from .models_census_larap import CensusKepalaKeluarga, CensusIndividu
from .serializers_census_larap import (
    CensusKepalaKeluargaSerializer,
    CensusKepalaKeluargaListSerializer,
    CensusIndividuSerializer,
    CensusIndividuListSerializer
)


class CensusKepalaKeluargaViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Census Kepala Keluarga (Household Head)
    
    Endpoints:
    - GET /api/census-kepala-keluarga/ - List all households
    - POST /api/census-kepala-keluarga/ - Create new household (with nested individuals)
    - GET /api/census-kepala-keluarga/{id}/ - Retrieve household detail
    - PUT /api/census-kepala-keluarga/{id}/ - Update household
    - PATCH /api/census-kepala-keluarga/{id}/ - Partial update household
    - DELETE /api/census-kepala-keluarga/{id}/ - Delete household (cascades to individuals)
    - POST /api/census-kepala-keluarga/{id}/add-individu/ - Add individual to household
    """
    
    queryset = CensusKepalaKeluarga.objects.all().prefetch_related('anggota_keluarga')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CensusKepalaKeluargaListSerializer
        return CensusKepalaKeluargaSerializer
    
    def get_queryset(self):
        """Filter by query parameters"""
        queryset = super().get_queryset()
        
        # Filter by desa
        desa = self.request.query_params.get('desa', None)
        if desa:
            queryset = queryset.filter(desa=desa)
        
        # Filter by id_project
        id_project = self.request.query_params.get('id_project', None)
        if id_project:
            queryset = queryset.filter(id_project=id_project)
        
        # Search by name or NIK
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(nama_depan__icontains=search) |
                Q(nama_tengah__icontains=search) |
                Q(nama_belakang__icontains=search) |
                Q(nik__icontains=search) |
                Q(id_rumah_tangga__icontains=search)
            )
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def add_individu(self, request, pk=None):
        """
        Add an individual to an existing household
        POST /api/census-kepala-keluarga/{id}/add-individu/
        """
        kepala_keluarga = self.get_object()
        
        serializer = CensusIndividuSerializer(data=request.data)
        if serializer.is_valid():
            # Get the next no_urut
            last_individu = kepala_keluarga.anggota_keluarga.order_by('-no_urut').first()
            next_no_urut = (last_individu.no_urut + 1) if last_individu else 1
            
            serializer.save(
                kepala_keluarga=kepala_keluarga,
                no_urut=next_no_urut
            )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Get summary statistics
        GET /api/census-kepala-keluarga/summary/
        """
        from django.db.models import Count, Sum
        
        total_households = self.get_queryset().count()
        total_individuals = CensusIndividu.objects.filter(
            kepala_keluarga__in=self.get_queryset()
        ).count()
        
        # Summary by desa
        by_desa = self.get_queryset().values('desa').annotate(
            total=Count('id'),
            total_people=Sum('jumlah_orang_rumah_tangga')
        ).order_by('-total')
        
        return Response({
            'total_households': total_households,
            'total_individuals': total_individuals,
            'by_desa': list(by_desa)
        })


class CensusIndividuViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Census Individu (Individual Family Members)
    
    Endpoints:
    - GET /api/census-individu/ - List all individuals
    - POST /api/census-individu/ - Create new individual
    - GET /api/census-individu/{id}/ - Retrieve individual detail
    - PUT /api/census-individu/{id}/ - Update individual
    - PATCH /api/census-individu/{id}/ - Partial update individual
    - DELETE /api/census-individu/{id}/ - Delete individual
    """
    
    queryset = CensusIndividu.objects.all().select_related('kepala_keluarga')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CensusIndividuListSerializer
        return CensusIndividuSerializer
    
    def get_queryset(self):
        """Filter by query parameters"""
        queryset = super().get_queryset()
        
        # Filter by kepala_keluarga
        kepala_keluarga_id = self.request.query_params.get('kepala_keluarga', None)
        if kepala_keluarga_id:
            queryset = queryset.filter(kepala_keluarga_id=kepala_keluarga_id)
        
        # Filter by id_rumah_tangga
        id_rumah_tangga = self.request.query_params.get('id_rumah_tangga', None)
        if id_rumah_tangga:
            queryset = queryset.filter(id_rumah_tangga=id_rumah_tangga)
        
        # Search by name or NIK
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(nama_depan__icontains=search) |
                Q(nama_belakang__icontains=search) |
                Q(nik__icontains=search)
            )
        
        return queryset
