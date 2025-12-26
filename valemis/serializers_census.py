"""
Serializers for Census Survey Models
"""
from rest_framework import serializers
from .models import CensusSurvey, CensusMember, CensusQuestion


class CensusSurveySerializer(serializers.ModelSerializer):
    """Serializer for CensusSurvey model"""

    class Meta:
        model = CensusSurvey
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class CensusSurveyListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing surveys"""

    class Meta:
        model = CensusSurvey
        fields = ['id', 'q1_kode_enumerator', 'q2_id_unik', 'village', 'district',
                 'survey_date', 'created_at']


class CensusMemberSerializer(serializers.ModelSerializer):
    """Serializer for CensusMember model"""

    class Meta:
        model = CensusMember
        fields = '__all__'


class CensusQuestionSerializer(serializers.ModelSerializer):
    """Serializer for CensusQuestion model"""

    class Meta:
        model = CensusQuestion
        fields = '__all__'


class CensusSurveyDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer with members included"""
    members = CensusMemberSerializer(many=True, read_only=True)

    class Meta:
        model = CensusSurvey
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
