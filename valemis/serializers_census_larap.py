"""
Serializers for Census Survey LARAP Models
"""

from rest_framework import serializers
from .models_census_larap import CensusKepalaKeluarga, CensusIndividu


class CensusIndividuSerializer(serializers.ModelSerializer):
    """Serializer for individual family members"""
    
    class Meta:
        model = CensusIndividu
        fields = '__all__'
        read_only_fields = ['id', 'id_asset', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate 'Lainnya' fields"""
        # Check if alasan_penghentian is "Lainnya" and requires text
        if data.get('alasan_penghentian') == '97' and not data.get('alasan_penghentian_lainnya'):
            raise serializers.ValidationError({
                'alasan_penghentian_lainnya': 'Harap sebutkan alasan penghentian lainnya'
            })
        
        # Check if disabilitas is "Lainnya" and requires text
        if data.get('disabilitas') == '7' and not data.get('disabilitas_lainnya'):
            raise serializers.ValidationError({
                'disabilitas_lainnya': 'Harap sebutkan disabilitas lainnya'
            })
        
        # Check if kondisi_kesehatan_kronis is "Lainnya" and requires text
        if data.get('kondisi_kesehatan_kronis') == '97' and not data.get('kondisi_kesehatan_kronis_lainnya'):
            raise serializers.ValidationError({
                'kondisi_kesehatan_kronis_lainnya': 'Harap sebutkan kondisi kesehatan kronis lainnya'
            })
        
        return data


class CensusKepalaKeluargaSerializer(serializers.ModelSerializer):
    """Serializer for household head with nested individuals"""
    
    anggota_keluarga = CensusIndividuSerializer(many=True, read_only=True)
    anggota_keluarga_data = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = CensusKepalaKeluarga
        fields = '__all__'
        read_only_fields = ['id', 'id_asset', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate 'Lainnya' fields for all dropdowns"""
        
        # Agama
        if data.get('agama') == '97' and not data.get('agama_lainnya'):
            raise serializers.ValidationError({
                'agama_lainnya': 'Harap sebutkan agama lainnya'
            })
        
        # Asal Etnis
        if data.get('asal_etnis') == 'Lainnya' and not data.get('asal_etnis_lainnya'):
            raise serializers.ValidationError({
                'asal_etnis_lainnya': 'Harap sebutkan asal etnis lainnya'
            })
        
        # Bahasa
        if data.get('bahasa') == 'Lainnya' and not data.get('bahasa_lainnya'):
            raise serializers.ValidationError({
                'bahasa_lainnya': 'Harap sebutkan bahasa lainnya'
            })
        
        # Tempat Asal KK
        if data.get('tempat_asal_kk') and data.get('tempat_asal_kk') != 'Desa yang Sama':
            if not data.get('tempat_asal_kk_tentukan'):
                raise serializers.ValidationError({
                    'tempat_asal_kk_tentukan': 'Harap tentukan tempat asal'
                })
        
        # Identifikasi Dampak
        if data.get('identifikasi_dampak') == 'Lainnya' and not data.get('identifikasi_dampak_lainnya'):
            raise serializers.ValidationError({
                'identifikasi_dampak_lainnya': 'Harap sebutkan identifikasi dampak lainnya'
            })
        
        # Alasan Penghentian
        if data.get('alasan_penghentian') == '97' and not data.get('alasan_penghentian_lainnya'):
            raise serializers.ValidationError({
                'alasan_penghentian_lainnya': 'Harap sebutkan alasan penghentian lainnya'
            })
        
        # Disabilitas
        if data.get('disabilitas') == '7' and not data.get('disabilitas_lainnya'):
            raise serializers.ValidationError({
                'disabilitas_lainnya': 'Harap sebutkan disabilitas lainnya'
            })
        
        # Kondisi Kesehatan Kronis
        if data.get('kondisi_kesehatan_kronis') == '97' and not data.get('kondisi_kesehatan_kronis_lainnya'):
            raise serializers.ValidationError({
                'kondisi_kesehatan_kronis_lainnya': 'Harap sebutkan kondisi kesehatan kronis lainnya'
            })
        
        return data
    
    def create(self, validated_data):
        """Create household head with nested individuals"""
        anggota_data = validated_data.pop('anggota_keluarga_data', [])
        
        # Create household head
        kepala_keluarga = CensusKepalaKeluarga.objects.create(**validated_data)
        
        # Create individuals
        for idx, anggota in enumerate(anggota_data, start=1):
            anggota['no_urut'] = idx
            CensusIndividu.objects.create(
                kepala_keluarga=kepala_keluarga,
                **anggota
            )
        
        return kepala_keluarga
    
    def update(self, instance, validated_data):
        """Update household head and optionally update individuals"""
        anggota_data = validated_data.pop('anggota_keluarga_data', None)
        
        # Update household head fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # If anggota_data is provided, replace all individuals
        if anggota_data is not None:
            instance.anggota_keluarga.all().delete()
            for idx, anggota in enumerate(anggota_data, start=1):
                anggota['no_urut'] = idx
                CensusIndividu.objects.create(
                    kepala_keluarga=instance,
                    **anggota
                )
        
        return instance


class CensusKepalaKeluargaListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list view"""
    
    nama_lengkap = serializers.SerializerMethodField()
    jumlah_anggota = serializers.SerializerMethodField()
    
    class Meta:
        model = CensusKepalaKeluarga
        fields = [
            'id', 'id_asset', 'id_project', 'id_rumah_tangga',
            'nama_lengkap', 'desa', 'kecamatan', 'kabupaten',
            'koordinat', 'nik', 'nomor_telepon',
            'jumlah_orang_rumah_tangga', 'jumlah_anggota',
            'pekerjaan_utama', 'created_at', 'updated_at'
        ]
    
    def get_nama_lengkap(self, obj):
        return ' '.join(filter(None, [obj.nama_depan, obj.nama_tengah, obj.nama_belakang]))
    
    def get_jumlah_anggota(self, obj):
        return obj.anggota_keluarga.count()


class CensusIndividuListSerializer(serializers.ModelSerializer):
    """Simplified serializer for individual list view"""
    
    nama_lengkap = serializers.SerializerMethodField()
    nama_kepala_keluarga = serializers.SerializerMethodField()
    
    class Meta:
        model = CensusIndividu
        fields = [
            'id', 'id_asset', 'id_rumah_tangga', 'no_urut',
            'nama_lengkap', 'nama_kepala_keluarga', 'hubungan_dengan_kk',
            'jenis_kelamin', 'usia', 'pekerjaan_utama',
            'created_at', 'updated_at'
        ]
    
    def get_nama_lengkap(self, obj):
        return ' '.join(filter(None, [obj.nama_depan, obj.nama_belakang]))
    
    def get_nama_kepala_keluarga(self, obj):
        if obj.kepala_keluarga:
            return ' '.join(filter(None, [
                obj.kepala_keluarga.nama_depan,
                obj.kepala_keluarga.nama_tengah,
                obj.kepala_keluarga.nama_belakang
            ]))
        return None
