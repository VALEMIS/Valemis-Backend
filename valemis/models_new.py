"""
Models for all 6 Valemis ERP Modules
- Asset Inventory
- Land Inventory
- Land Acquisition
- Land Compliance
- Litigation (Litigasi/Claim)
- Stakeholder Management
"""

from django.db import models
from decimal import Decimal


# =============================================================================
# 1. ASSET INVENTORY MODULE
# =============================================================================
class AssetInventory(models.Model):
    """Asset inventory for land and property assets per village"""
    code = models.CharField(max_length=50, unique=True, db_index=True)
    owner_name = models.CharField(max_length=255)
    village = models.CharField(max_length=255)
    land_area = models.DecimalField(max_digits=12, decimal_places=2)  # m²
    building_area = models.DecimalField(max_digits=12, decimal_places=2)  # m²
    certificate_status = models.CharField(max_length=50)  # SHM, SHGB, Girik, Belum Sertifikat
    lat = models.DecimalField(max_digits=10, decimal_places=6)
    lng = models.DecimalField(max_digits=10, decimal_places=6)

    # Extended fields - Identitas Kepala Keluarga
    nama_depan = models.CharField(max_length=100, null=True, blank=True)
    nama_tengah = models.CharField(max_length=100, null=True, blank=True)
    nama_belakang = models.CharField(max_length=100, null=True, blank=True)
    nama_ayah = models.CharField(max_length=100, null=True, blank=True)
    nama_kakek = models.CharField(max_length=100, null=True, blank=True)
    nama_pasangan = models.CharField(max_length=100, null=True, blank=True)
    nomor_telepon = models.CharField(max_length=20, null=True, blank=True)
    nik = models.CharField(max_length=20, null=True, blank=True)
    kecamatan = models.CharField(max_length=100, null=True, blank=True)
    kabupaten = models.CharField(max_length=100, null=True, blank=True)
    provinsi = models.CharField(max_length=100, null=True, blank=True)
    nama_responden = models.CharField(max_length=255, null=True, blank=True)
    hubungan_responden = models.CharField(max_length=100, null=True, blank=True)

    # Identifikasi Rumah Tangga dan PAP
    kode_enumerator = models.CharField(max_length=50, null=True, blank=True)
    tanggal_survei = models.DateField(null=True, blank=True)
    kode_foto_survei = models.CharField(max_length=50, null=True, blank=True)
    id_unik = models.CharField(max_length=100, null=True, blank=True)

    # Additional Census Survey Fields
    agama = models.CharField(max_length=50, null=True, blank=True)
    agama_lainnya = models.CharField(max_length=100, null=True, blank=True)
    asal_etnis = models.CharField(max_length=50, null=True, blank=True)
    asal_etnis_lainnya = models.CharField(max_length=100, null=True, blank=True)
    bahasa = models.CharField(max_length=50, null=True, blank=True)
    bahasa_lainnya = models.CharField(max_length=100, null=True, blank=True)
    tempat_asal_kk_tentukan = models.CharField(max_length=100, null=True, blank=True)
    jumlah_orang_rumah_tangga = models.IntegerField(null=True, blank=True)
    identifikasi_dampak = models.CharField(max_length=100, null=True, blank=True)
    jenis_kelamin = models.CharField(max_length=20, null=True, blank=True)
    usia = models.IntegerField(null=True, blank=True)
    status_perkawinan = models.CharField(max_length=50, null=True, blank=True)
    pendidikan_terakhir = models.CharField(max_length=50, null=True, blank=True)
    bekerja_12_bulan = models.CharField(max_length=50, null=True, blank=True)
    pekerjaan_utama = models.CharField(max_length=100, null=True, blank=True)
    pekerjaan_utama_lainnya = models.CharField(max_length=100, null=True, blank=True)
    jenis_pekerjaan = models.CharField(max_length=100, null=True, blank=True)
    lokasi_pekerjaan_lainnya = models.CharField(max_length=100, null=True, blank=True)
    jumlah_bulan_bekerja = models.IntegerField(null=True, blank=True)
    penghasilan_per_bulan = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    pekerjaan_sekunder = models.CharField(max_length=100, null=True, blank=True)
    pekerjaan_sekunder_lainnya = models.CharField(max_length=100, null=True, blank=True)
    lokasi_pekerjaan_sekunder = models.CharField(max_length=100, null=True, blank=True)
    lokasi_pekerjaan_sekunder_lainnya = models.CharField(max_length=100, null=True, blank=True)
    jumlah_bulan_bekerja_sekunder = models.IntegerField(null=True, blank=True)
    penghasilan_sekunder_per_bulan = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    keterampilan_lainnya = models.CharField(max_length=100, null=True, blank=True)
    disabilitas = models.CharField(max_length=100, null=True, blank=True)
    defisit_pangan_lainnya = models.CharField(max_length=200, null=True, blank=True)
    penghasilan_tahunan = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    pengeluaran_bulanan = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    tabungan_lainnya = models.CharField(max_length=100, null=True, blank=True)
    hutang_lainnya = models.CharField(max_length=100, null=True, blank=True)
    pernah_dampak_proyek = models.CharField(max_length=10, null=True, blank=True)
    jenis_proyek_lain = models.CharField(max_length=100, null=True, blank=True)
    luas_lahan_dibebaskan = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    pernah_pengungsi = models.CharField(max_length=10, null=True, blank=True)
    punya_bisnis = models.CharField(max_length=10, null=True, blank=True)
    lokasi_bisnis_lainnya = models.CharField(max_length=100, null=True, blank=True)
    kepemilikan_bisnis_lainnya = models.CharField(max_length=100, null=True, blank=True)
    sejak_kapan_bisnis = models.CharField(max_length=50, null=True, blank=True)
    jenis_bisnis_lainnya = models.CharField(max_length=100, null=True, blank=True)
    jumlah_pegawai = models.IntegerField(null=True, blank=True)
    pendapatan_rata_bisnis = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    deskripsi_produk_layanan = models.TextField(null=True, blank=True)
    tipe_rumah = models.CharField(max_length=100, null=True, blank=True)
    tipe_rumah_lainnya = models.CharField(max_length=100, null=True, blank=True)
    sumber_air = models.CharField(max_length=100, null=True, blank=True)
    sumber_air_lainnya = models.CharField(max_length=100, null=True, blank=True)
    pelayanan_listrik = models.CharField(max_length=100, null=True, blank=True)
    pelayanan_listrik_lainnya = models.CharField(max_length=100, null=True, blank=True)
    rekening_bank = models.CharField(max_length=10, null=True, blank=True)
    karakteristik_krt = models.TextField(null=True, blank=True)
    kecukupan_pangan = models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'asset_inventory'
        verbose_name = 'Asset Inventory'
        verbose_name_plural = 'Asset Inventories'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.owner_name}"

    @property
    def coordinates(self):
        return f"{self.lat}, {self.lng}"


class AssetInventoryDetail(models.Model):
    """
    Asset Inventory Detail - matching Excel 'Inventaris Aset' sheet
    Stores 5 types of assets: Tanah, Tanaman, Pohon, Bangunan, Sumber Daya Alam
    """
    ASSET_TYPE_CHOICES = [
        ('Tanah', 'Tanah'),
        ('Tanaman', 'Tanaman'),
        ('Pohon', 'Pohon'),
        ('Bangunan', 'Bangunan'),
        ('Sumber Daya Alam', 'Sumber Daya Alam'),
    ]

    # Link to main Asset Inventory
    asset_inventory = models.ForeignKey(
        AssetInventory,
        on_delete=models.CASCADE,
        related_name='asset_details',
        null=True,
        blank=True
    )

    # Household number from Excel
    rumah_tangga_no = models.CharField(max_length=50, null=True, blank=True)
    id_aset = models.CharField(max_length=50, null=True, blank=True)

    # Asset Type - one of 5 types
    asset_type = models.CharField(max_length=50, choices=ASSET_TYPE_CHOICES)

    # ===== TANAH (Land) Fields =====
    jenis_tanah = models.CharField(max_length=100, null=True, blank=True)
    terdaftar_di = models.CharField(max_length=100, null=True, blank=True)
    luas_m2 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status_pemilik = models.CharField(max_length=100, null=True, blank=True)
    pemilik_sebelumnya = models.CharField(max_length=255, null=True, blank=True)
    tenurial = models.CharField(max_length=10, null=True, blank=True)  # Y/T
    catatan_tanah = models.TextField(null=True, blank=True)

    # ===== TANAMAN (Crops) Fields =====
    jenis_tanaman = models.CharField(max_length=100, null=True, blank=True)
    usia_tanaman = models.IntegerField(null=True, blank=True)
    kondisi_tanaman = models.CharField(max_length=100, null=True, blank=True)
    sumber_air_tanaman = models.CharField(max_length=100, null=True, blank=True)
    gambar_tanaman = models.CharField(max_length=255, null=True, blank=True)

    # ===== POHON (Trees) Fields =====
    jenis_pohon = models.CharField(max_length=100, null=True, blank=True)
    jumlah_pohon = models.IntegerField(null=True, blank=True)
    luas_pohon = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    produktif = models.CharField(max_length=10, null=True, blank=True)  # Y/T
    dewasa = models.CharField(max_length=10, null=True, blank=True)  # Y/T
    produksi_per_tahun = models.CharField(max_length=100, null=True, blank=True)
    kondisi_pohon = models.CharField(max_length=100, null=True, blank=True)
    gambar1_pohon = models.CharField(max_length=255, null=True, blank=True)
    gambar2_pohon = models.CharField(max_length=255, null=True, blank=True)
    gambar3_pohon = models.CharField(max_length=255, null=True, blank=True)

    # ===== BANGUNAN (Buildings) Fields =====
    jenis_bangunan = models.CharField(max_length=100, null=True, blank=True)
    luas_bangunan = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    permanen_sementara = models.CharField(max_length=50, null=True, blank=True)
    primer_sekunder = models.CharField(max_length=50, null=True, blank=True)
    bahan_utama = models.CharField(max_length=100, null=True, blank=True)
    sanitarian = models.CharField(max_length=100, null=True, blank=True)
    pasokan_listrik = models.CharField(max_length=100, null=True, blank=True)
    persediaan_air = models.CharField(max_length=100, null=True, blank=True)
    gambar1_bangunan = models.CharField(max_length=255, null=True, blank=True)
    gambar2_bangunan = models.CharField(max_length=255, null=True, blank=True)
    gambar3_bangunan = models.CharField(max_length=255, null=True, blank=True)
    gambar4_bangunan = models.CharField(max_length=255, null=True, blank=True)

    # ===== SUMBER DAYA ALAM (Natural Resources) Fields =====
    jenis_sumber_daya_alam = models.CharField(max_length=100, null=True, blank=True)
    produktivitas_per_tahun = models.CharField(max_length=100, null=True, blank=True)
    luas_sda = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'asset_inventory_detail'
        verbose_name = 'Asset Inventory Detail'
        verbose_name_plural = 'Asset Inventory Details'
        ordering = ['asset_type', 'id']

    def __str__(self):
        return f"{self.asset_type} - {self.rumah_tangga_no or self.id_aset}"


# =============================================================================
# 2. LAND INVENTORY MODULE
# =============================================================================
class LandInventory(models.Model):
    """Land inventory for Vale-owned and managed lands"""
    CATEGORY_CHOICES = [
        ('Vale Owned', 'Milik Vale'),
        ('Acquired', 'Acquired/Diakuisisi'),
        ('IUPK', 'IUPK'),
        ('PPKH', 'PPKH'),
        ('Operational', 'Operasional'),
    ]
    
    CERTIFICATE_CHOICES = [
        ('HGU', 'HGU'),
        ('SHM', 'SHM'),
        ('SHGB', 'SHGB'),
        ('Belum Sertifikat', 'Belum Sertifikat'),
    ]
    
    code = models.CharField(max_length=50, unique=True, db_index=True)
    location_name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    area = models.DecimalField(max_digits=12, decimal_places=2)  # in Hectares
    certificate = models.CharField(max_length=50, choices=CERTIFICATE_CHOICES)
    certificate_no = models.CharField(max_length=100, null=True, blank=True)
    lat = models.DecimalField(max_digits=10, decimal_places=6)
    lng = models.DecimalField(max_digits=10, decimal_places=6)
    acquisition_year = models.IntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'land_inventory'
        verbose_name = 'Land Inventory'
        verbose_name_plural = 'Land Inventories'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.location_name}"

    @property
    def coordinates(self):
        return f"{self.lat}, {self.lng}"


class LandDocument(models.Model):
    """Documents associated with land inventory"""
    land = models.ForeignKey(
        LandInventory, 
        on_delete=models.CASCADE, 
        related_name='documents'
    )
    file_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'land_document'
        verbose_name = 'Land Document'
        verbose_name_plural = 'Land Documents'

    def __str__(self):
        return f"{self.land.code} - {self.file_name}"


# =============================================================================
# 3. LAND ACQUISITION MODULE (Pembebasan Lahan)
# =============================================================================
class LandAcquisition(models.Model):
    """Land acquisition/pembebasan lahan per project"""
    STATUS_CHOICES = [
        ('Bebas', 'Bebas'),
        ('Dalam Negosiasi', 'Dalam Negosiasi'),
        ('Belum Diproses', 'Belum Diproses'),
    ]
    
    code = models.CharField(max_length=50, unique=True, db_index=True)
    project = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    village = models.CharField(max_length=255)
    area = models.DecimalField(max_digits=12, decimal_places=2)  # in m²
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Belum Diproses')
    jumlah_bebas = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # m²
    biaya_pembebasan = models.DecimalField(max_digits=18, decimal_places=2, default=0)  # Rupiah
    negotiation_date = models.CharField(max_length=20, default='-')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'land_acquisition'
        verbose_name = 'Land Acquisition'
        verbose_name_plural = 'Land Acquisitions'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.owner_name} ({self.project})"


# =============================================================================
# 4. LAND COMPLIANCE MODULE
# =============================================================================
class LandCompliance(models.Model):
    """Land compliance and permit tracking"""
    PERMIT_TYPE_CHOICES = [
        ('IUPK', 'IUPK'),
        ('PPKH', 'PPKH'),
        ('HGU', 'HGU'),
        ('SHM', 'SHM'),
        ('SHGB', 'SHGB'),
        ('IMB', 'IMB'),
        ('UKL-UPL', 'UKL-UPL'),
        ('AMDAL', 'AMDAL'),
    ]
    
    STATUS_CHOICES = [
        ('Compliant', 'Compliant'),
        ('Expiring Soon', 'Expiring Soon'),
        ('Expired', 'Expired'),
        ('No Permit', 'No Permit'),
    ]
    
    land_code = models.CharField(max_length=50, db_index=True)
    location_name = models.CharField(max_length=255)
    permit_type = models.CharField(max_length=50, choices=PERMIT_TYPE_CHOICES)
    permit_number = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True)
    
    # Relationship to Land Inventory (optional)
    land_inventory = models.ForeignKey(
        LandInventory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='compliances'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'land_compliance'
        verbose_name = 'Land Compliance'
        verbose_name_plural = 'Land Compliances'
        ordering = ['land_code', 'permit_type']

    def __str__(self):
        return f"{self.land_code} - {self.permit_type} ({self.permit_number})"

    @property
    def days_remaining(self):
        if not self.expiry_date:
            return None
        from datetime import date
        delta = self.expiry_date - date.today()
        return delta.days


# =============================================================================
# 5. LITIGATION MODULE (Litigasi/Claim)
# =============================================================================
class Litigation(models.Model):
    """Land litigation and claim cases"""
    CASE_TYPE_CHOICES = [
        ('Land Ownership', 'Kepemilikan Lahan'),
        ('Boundary Dispute', 'Sengketa Batas'),
        ('Compensation Claim', 'Klaim Kompensasi'),
        ('Environmental Claim', 'Klaim Lingkungan'),
        ('Others', 'Lainnya'),
    ]
    
    STATUS_CHOICES = [
        ('Active', 'Aktif'),
        ('Under Review', 'Dalam Proses'),
        ('Resolved', 'Selesai'),
        ('Dismissed', 'Ditolak'),
    ]
    
    PRIORITY_CHOICES = [
        ('High', 'Tinggi'),
        ('Medium', 'Sedang'),
        ('Low', 'Rendah'),
    ]
    
    case_code = models.CharField(max_length=50, unique=True, db_index=True)
    land_code = models.CharField(max_length=50, db_index=True)
    case_type = models.CharField(max_length=100, choices=CASE_TYPE_CHOICES)
    claimant = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Active')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    
    # Relationship to Land Inventory (optional)
    land_inventory = models.ForeignKey(
        LandInventory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='litigations'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'litigation'
        verbose_name = 'Litigation'
        verbose_name_plural = 'Litigations'
        ordering = ['-start_date', 'case_code']

    def __str__(self):
        return f"{self.case_code} - {self.claimant}"


# =============================================================================
# 6. STAKEHOLDER MANAGEMENT MODULE
# =============================================================================
class StakeholderNew(models.Model):
    """Stakeholder management with influence/interest matrix"""
    TYPE_CHOICES = [
        ('Perusahaan', 'Perusahaan'),
        ('Pemerintah', 'Pemerintah'),
        ('Masyarakat', 'Masyarakat'),
        ('NGO', 'NGO'),
        ('Media', 'Media'),
        ('Akademisi', 'Akademisi'),
        ('Lainnya', 'Lainnya'),
    ]
    
    CATEGORY_CHOICES = [
        ('Primary', 'Primary'),
        ('Secondary', 'Secondary'),
        ('Tertiary', 'Tertiary'),
    ]
    
    sh_id = models.CharField(max_length=20, unique=True, db_index=True)
    nama = models.CharField(max_length=255)
    tipe = models.CharField(max_length=50, choices=TYPE_CHOICES)
    kategori = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    alamat = models.TextField()
    kontak = models.CharField(max_length=100)
    interest = models.IntegerField(default=1)  # 1-5 scale
    influence = models.IntegerField(default=1)  # 1-5 scale
    
    # Geospatial (optional)
    lat = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stakeholder_new'
        verbose_name = 'Stakeholder'
        verbose_name_plural = 'Stakeholders'
        ordering = ['sh_id']

    def __str__(self):
        return f"{self.sh_id} - {self.nama}"


class StakeholderInvolvementNew(models.Model):
    """Stakeholder involvement in projects/cases"""
    ROLE_CHOICES = [
        ('Pemilik', 'Pemilik'),
        ('Penggugat', 'Penggugat'),
        ('Saksi', 'Saksi'),
        ('Mediator', 'Mediator'),
        ('Konsultan', 'Konsultan'),
        ('Lainnya', 'Lainnya'),
    ]
    
    stakeholder = models.ForeignKey(
        StakeholderNew, 
        on_delete=models.CASCADE, 
        related_name='involvements'
    )
    object_type = models.CharField(max_length=50)  # e.g., 'litigation', 'acquisition'
    object_id = models.IntegerField()
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'stakeholder_involvement_new'
        verbose_name = 'Stakeholder Involvement'
        verbose_name_plural = 'Stakeholder Involvements'

    def __str__(self):
        return f"{self.stakeholder.nama} - {self.object_type} ({self.role})"
