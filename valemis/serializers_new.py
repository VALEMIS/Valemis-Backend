"""
Serializers for all 6 Valemis ERP Modules
"""

from rest_framework import serializers
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


# =============================================================================
# 1. ASSET INVENTORY SERIALIZERS
# =============================================================================
class AssetInventorySerializer(serializers.ModelSerializer):
    coordinates = serializers.ReadOnlyField()
    
    class Meta:
        model = AssetInventory
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class AssetInventoryListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list view"""
    coordinates = serializers.ReadOnlyField()
    
    class Meta:
        model = AssetInventory
        fields = [
            'id', 'code', 'owner_name', 'village', 'land_area', 
            'building_area', 'certificate_status', 'coordinates', 'lat', 'lng'
        ]


# =============================================================================
# 2. LAND INVENTORY SERIALIZERS
# =============================================================================
class LandDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandDocument
        fields = ['id', 'file_name', 'created_at']
        read_only_fields = ['id', 'created_at']


class LandInventorySerializer(serializers.ModelSerializer):
    documents = LandDocumentSerializer(many=True, read_only=True)
    documents_list = serializers.ListField(
        child=serializers.CharField(), 
        write_only=True, 
        required=False
    )
    coordinates = serializers.ReadOnlyField()
    
    class Meta:
        model = LandInventory
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        documents_list = validated_data.pop('documents_list', [])
        land = LandInventory.objects.create(**validated_data)
        for doc_name in documents_list:
            LandDocument.objects.create(land=land, file_name=doc_name)
        return land

    def update(self, instance, validated_data):
        documents_list = validated_data.pop('documents_list', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if documents_list is not None:
            instance.documents.all().delete()
            for doc_name in documents_list:
                LandDocument.objects.create(land=instance, file_name=doc_name)
        
        return instance


class LandInventoryListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list view"""
    documents = serializers.SerializerMethodField()
    coordinates = serializers.ReadOnlyField()
    
    class Meta:
        model = LandInventory
        fields = [
            'id', 'code', 'location_name', 'category', 'area',
            'certificate', 'certificate_no', 'coordinates', 'lat', 'lng',
            'acquisition_year', 'documents'
        ]

    def get_documents(self, obj):
        return [doc.file_name for doc in obj.documents.all()]


# =============================================================================
# 3. LAND ACQUISITION SERIALIZERS
# =============================================================================
class LandAcquisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandAcquisition
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class LandAcquisitionListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list view"""
    class Meta:
        model = LandAcquisition
        fields = [
            'id', 'code', 'project', 'owner_name', 'village', 'area',
            'status', 'jumlah_bebas', 'biaya_pembebasan', 'negotiation_date'
        ]


# =============================================================================
# 4. LAND COMPLIANCE SERIALIZERS
# =============================================================================
class LandComplianceSerializer(serializers.ModelSerializer):
    days_remaining = serializers.ReadOnlyField()
    
    class Meta:
        model = LandCompliance
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class LandComplianceListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list view"""
    days_remaining = serializers.ReadOnlyField()
    
    class Meta:
        model = LandCompliance
        fields = [
            'id', 'land_code', 'location_name', 'permit_type', 'permit_number',
            'issue_date', 'expiry_date', 'days_remaining', 'status', 'notes'
        ]


# =============================================================================
# 5. LITIGATION SERIALIZERS
# =============================================================================
class LitigationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Litigation
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class LitigationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list view"""
    class Meta:
        model = Litigation
        fields = [
            'id', 'case_code', 'land_code', 'case_type', 'claimant',
            'description', 'start_date', 'status', 'priority'
        ]


# =============================================================================
# 6. STAKEHOLDER SERIALIZERS
# =============================================================================
class StakeholderInvolvementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StakeholderInvolvementNew
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class StakeholderSerializer(serializers.ModelSerializer):
    involvements = StakeholderInvolvementSerializer(many=True, read_only=True)
    
    class Meta:
        model = StakeholderNew
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class StakeholderListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list view"""
    class Meta:
        model = StakeholderNew
        fields = [
            'id', 'sh_id', 'nama', 'tipe', 'kategori', 'alamat',
            'kontak', 'interest', 'influence'
        ]
