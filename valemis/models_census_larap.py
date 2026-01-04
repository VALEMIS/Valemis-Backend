"""
Census Survey LARAP Models
Two main models:
1. CensusKepalaKeluarga - Household head responses
2. CensusIndividu - Individual family member responses

Following CSV schema with CharField for dropdowns (no enums) to support "Lainnya" values.
"""

from django.db import models
from decimal import Decimal


def generate_asset_id():
    """Generate unique asset ID in format ASSET-XXXXX"""
    from django.db.models import Max
    
    # Get the highest existing ID
    last_kk = CensusKepalaKeluarga.objects.aggregate(Max('id'))['id__max']
    last_ind = CensusIndividu.objects.aggregate(Max('id'))['id__max']
    
    # Get the maximum ID from both tables
    max_id = max(last_kk or 0, last_ind or 0)
    
    # Generate new ID
    new_id = max_id + 1
    return f"ASSET-{new_id:05d}"


class CensusKepalaKeluarga(models.Model):
    """
    Census Survey - Kuesioner Respons Kepala Keluarga
    Main household data with head of household information
    """
    
    # Auto-generated identifiers
    id_asset = models.CharField(max_length=20, unique=True, db_index=True, editable=False)
    id_project = models.CharField(max_length=50, blank=True, null=True)
    
    # A. Identifikasi Rumah Tangga dan PAP
    kode_enumerator = models.CharField(max_length=50, blank=True, null=True)
    id_rumah_tangga = models.CharField(max_length=50, blank=True, null=True, db_index=True)
    tanggal = models.DateField(blank=True, null=True)
    kode_foto_survei = models.CharField(max_length=50, blank=True, null=True)
    entitas_terdampak = models.CharField(max_length=100, blank=True, null=True)  # 1-4 or text
    koordinat = models.CharField(max_length=100, blank=True, null=True)
    
    # B. Informasi Kepala Keluarga
    nama_depan = models.CharField(max_length=100, blank=True, null=True)
    nama_tengah = models.CharField(max_length=100, blank=True, null=True)
    nama_belakang = models.CharField(max_length=100, blank=True, null=True)
    nama_ayah = models.CharField(max_length=100, blank=True, null=True)
    nama_kakek = models.CharField(max_length=100, blank=True, null=True)
    nama_pasangan = models.CharField(max_length=100, blank=True, null=True)
    nomor_telepon = models.CharField(max_length=20, blank=True, null=True)
    nik = models.CharField(max_length=20, blank=True, null=True)
    
    # Alamat
    desa = models.CharField(max_length=100, blank=True, null=True)
    kecamatan = models.CharField(max_length=100, blank=True, null=True)
    kabupaten = models.CharField(max_length=100, blank=True, null=True)
    provinsi = models.CharField(max_length=100, blank=True, null=True)
    
    nama_responden = models.CharField(max_length=255, blank=True, null=True)
    hubungan_responden = models.CharField(max_length=200, blank=True, null=True)
    
    # C. Profil Dampak
    identifikasi_dampak = models.CharField(max_length=200, blank=True, null=True)
    identifikasi_dampak_lainnya = models.TextField(blank=True, null=True)
    
    # D. Profil Sosial Rumah Tangga
    agama = models.CharField(max_length=200, blank=True, null=True)
    agama_lainnya = models.CharField(max_length=200, blank=True, null=True)
    asal_etnis = models.CharField(max_length=200, blank=True, null=True)
    asal_etnis_lainnya = models.CharField(max_length=200, blank=True, null=True)
    bahasa = models.CharField(max_length=200, blank=True, null=True)
    bahasa_lainnya = models.CharField(max_length=200, blank=True, null=True)
    tempat_asal_kk = models.CharField(max_length=200, blank=True, null=True)
    tempat_asal_kk_tentukan = models.CharField(max_length=200, blank=True, null=True)
    jumlah_orang_rumah_tangga = models.IntegerField(blank=True, null=True)
    
    # E. Demografi Rumah Tangga (Kepala Keluarga)
    jenis_kelamin = models.CharField(max_length=200, blank=True, null=True)
    tanggal_lahir = models.DateField(blank=True, null=True)
    usia = models.IntegerField(blank=True, null=True)
    status_perkawinan = models.CharField(max_length=200, blank=True, null=True)
    bisa_membaca_menulis = models.CharField(max_length=200, blank=True, null=True)
    sedang_sekolah = models.CharField(max_length=200, blank=True, null=True)
    sekolah_dimana = models.CharField(max_length=200, blank=True, null=True)
    pendidikan_terakhir = models.CharField(max_length=200, blank=True, null=True)
    alasan_penghentian = models.CharField(max_length=200, blank=True, null=True)
    alasan_penghentian_lainnya = models.TextField(blank=True, null=True)
    disabilitas = models.CharField(max_length=200, blank=True, null=True)
    disabilitas_lainnya = models.TextField(blank=True, null=True)
    kondisi_kesehatan_kronis = models.CharField(max_length=200, blank=True, null=True)
    kondisi_kesehatan_kronis_lainnya = models.TextField(blank=True, null=True)
    
    # F. Pekerjaan, Keterampilan, dan Tanah (Kepala Keluarga)
    bekerja_12_bulan = models.CharField(max_length=200, blank=True, null=True)
    pekerjaan_utama = models.CharField(max_length=200, blank=True, null=True)
    pekerjaan_utama_lainnya = models.CharField(max_length=200, blank=True, null=True)
    jenis_pekerjaan_utama = models.CharField(max_length=200, blank=True, null=True)
    lokasi_pekerjaan_utama = models.CharField(max_length=200, blank=True, null=True)
    lokasi_pekerjaan_utama_lainnya = models.CharField(max_length=200, blank=True, null=True)
    jumlah_bulan_bekerja = models.IntegerField(blank=True, null=True)
    penghasilan_per_bulan = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    
    pekerjaan_sekunder = models.CharField(max_length=200, blank=True, null=True)
    pekerjaan_sekunder_lainnya = models.CharField(max_length=200, blank=True, null=True)
    lokasi_pekerjaan_sekunder = models.CharField(max_length=200, blank=True, null=True)
    lokasi_pekerjaan_sekunder_lainnya = models.CharField(max_length=200, blank=True, null=True)
    jumlah_bulan_bekerja_sekunder = models.IntegerField(blank=True, null=True)
    penghasilan_sekunder_per_bulan = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    
    keterampilan = models.CharField(max_length=200, blank=True, null=True)
    keterampilan_lainnya = models.CharField(max_length=200, blank=True, null=True)
    
    # G. Kesehatan (Rumah Tangga)
    penyakit_umum_anak = models.TextField(blank=True, null=True)
    penyakit_umum_remaja = models.TextField(blank=True, null=True)
    penyakit_umum_dewasa = models.TextField(blank=True, null=True)
    penyakit_umum_lansia = models.TextField(blank=True, null=True)
    tempat_pelayanan_kesehatan = models.CharField(max_length=200, blank=True, null=True)
    tempat_pelayanan_kesehatan_lainnya = models.CharField(max_length=200, blank=True, null=True)
    
    # H. Kecukupan Pangan (Rumah Tangga)
    kecukupan_pangan = models.CharField(max_length=200, blank=True, null=True)
    defisit_pangan_cara_menutupi = models.TextField(blank=True, null=True)
    defisit_pangan_lainnya = models.CharField(max_length=200, blank=True, null=True)
    
    # I. Pendapatan, Pengeluaran dan Utang Rumah Tangga
    # Pendapatan (3 entries)
    pendapatan_1_pertanian = models.CharField(max_length=200, blank=True, null=True)
    pendapatan_1_sumber = models.CharField(max_length=200, blank=True, null=True)
    pendapatan_1_sumber_lainnya = models.CharField(max_length=200, blank=True, null=True)
    pendapatan_1_primer_sekunder = models.CharField(max_length=200, blank=True, null=True)
    pendapatan_1_jumlah = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    
    pendapatan_2_pertanian = models.CharField(max_length=200, blank=True, null=True)
    pendapatan_2_sumber = models.CharField(max_length=200, blank=True, null=True)
    pendapatan_2_sumber_lainnya = models.CharField(max_length=200, blank=True, null=True)
    pendapatan_2_primer_sekunder = models.CharField(max_length=200, blank=True, null=True)
    pendapatan_2_jumlah = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    
    pendapatan_3_pertanian = models.CharField(max_length=200, blank=True, null=True)
    pendapatan_3_sumber = models.CharField(max_length=200, blank=True, null=True)
    pendapatan_3_sumber_lainnya = models.CharField(max_length=200, blank=True, null=True)
    pendapatan_3_primer_sekunder = models.CharField(max_length=200, blank=True, null=True)
    pendapatan_3_jumlah = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    
    penghasilan_tahunan_total = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    
    # Pengeluaran (3 entries)
    pengeluaran_1_item = models.CharField(max_length=200, blank=True, null=True)
    pengeluaran_1_item_lainnya = models.CharField(max_length=200, blank=True, null=True)
    pengeluaran_1_frekuensi = models.IntegerField(blank=True, null=True)
    pengeluaran_1_jumlah = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    
    pengeluaran_2_item = models.CharField(max_length=200, blank=True, null=True)
    pengeluaran_2_item_lainnya = models.CharField(max_length=200, blank=True, null=True)
    pengeluaran_2_frekuensi = models.IntegerField(blank=True, null=True)
    pengeluaran_2_jumlah = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    
    pengeluaran_3_item = models.CharField(max_length=200, blank=True, null=True)
    pengeluaran_3_item_lainnya = models.CharField(max_length=200, blank=True, null=True)
    pengeluaran_3_frekuensi = models.IntegerField(blank=True, null=True)
    pengeluaran_3_jumlah = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    
    pengeluaran_bulanan_total = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    
    # Tabungan & Hutang
    rekening_bank = models.CharField(max_length=200, blank=True, null=True)
    punya_tabungan = models.CharField(max_length=200, blank=True, null=True)
    punya_hutang = models.CharField(max_length=200, blank=True, null=True)
    jenis_tabungan = models.CharField(max_length=200, blank=True, null=True)
    jenis_tabungan_lainnya = models.CharField(max_length=200, blank=True, null=True)
    jenis_hutang = models.CharField(max_length=200, blank=True, null=True)
    jenis_hutang_lainnya = models.CharField(max_length=200, blank=True, null=True)
    alasan_hutang = models.CharField(max_length=200, blank=True, null=True)
    alasan_hutang_lainnya = models.CharField(max_length=200, blank=True, null=True)
    
    # J. Dampak Pembebasan Lahan
    pernah_terdampak_proyek = models.CharField(max_length=200, blank=True, null=True)
    jenis_proyek_sebelumnya = models.CharField(max_length=200, blank=True, null=True)
    jenis_proyek_lainnya = models.CharField(max_length=200, blank=True, null=True)
    luas_lahan_dibebaskan = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    pernah_pengungsi = models.CharField(max_length=200, blank=True, null=True)
    
    # K. Usaha Komersial atau Bisnis
    punya_bisnis = models.CharField(max_length=200, blank=True, null=True)
    lokasi_bisnis = models.CharField(max_length=200, blank=True, null=True)
    lokasi_bisnis_lainnya = models.CharField(max_length=200, blank=True, null=True)
    kepemilikan_bisnis = models.CharField(max_length=200, blank=True, null=True)
    kepemilikan_bisnis_lainnya = models.CharField(max_length=200, blank=True, null=True)
    sejak_kapan_bisnis = models.CharField(max_length=100, blank=True, null=True)
    jenis_bisnis = models.CharField(max_length=200, blank=True, null=True)
    jenis_bisnis_lainnya = models.CharField(max_length=200, blank=True, null=True)
    jumlah_pegawai = models.IntegerField(blank=True, null=True)
    pendapatan_bisnis_per_bulan = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    deskripsi_produk_layanan = models.TextField(blank=True, null=True)
    
    # L. Struktur Tempat Tinggal
    tipe_rumah = models.CharField(max_length=200, blank=True, null=True)
    tipe_rumah_lainnya = models.CharField(max_length=200, blank=True, null=True)
    luas_rumah = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    pelayanan_listrik = models.CharField(max_length=200, blank=True, null=True)
    pelayanan_listrik_lainnya = models.CharField(max_length=200, blank=True, null=True)
    sumber_air = models.CharField(max_length=200, blank=True, null=True)
    sumber_air_lainnya = models.CharField(max_length=200, blank=True, null=True)
    sanitasi = models.CharField(max_length=200, blank=True, null=True)
    
    # M. Kerentanan
    karakteristik_kerentanan = models.TextField(blank=True, null=True)
    
    # N. Komunikasi dan Informasi
    sumber_informasi = models.CharField(max_length=200, blank=True, null=True)
    metode_komunikasi = models.CharField(max_length=200, blank=True, null=True)
    
    # O. Tanah
    nib = models.CharField(max_length=100, blank=True, null=True)
    letak_tanah = models.CharField(max_length=200, blank=True, null=True)
    status_tanah = models.CharField(max_length=200, blank=True, null=True)
    surat_bukti_tanah = models.CharField(max_length=200, blank=True, null=True)
    luas_tanah = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    tahun_kelola_lahan = models.IntegerField(blank=True, null=True)
    asal_usul_perolehan = models.CharField(max_length=200, blank=True, null=True)
    biaya_perolehan = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    batas_utara = models.CharField(max_length=200, blank=True, null=True)
    batas_selatan = models.CharField(max_length=200, blank=True, null=True)
    batas_timur = models.CharField(max_length=200, blank=True, null=True)
    batas_barat = models.CharField(max_length=200, blank=True, null=True)
    
    # P. Ruang Atas dan Bawah
    hm_sarusun = models.CharField(max_length=200, blank=True, null=True)
    luas_ruang = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    
    # Q. Tanaman (jumlah untuk setiap jenis)
    tanaman_merica = models.IntegerField(blank=True, null=True, default=0)
    tanaman_alpukat = models.IntegerField(blank=True, null=True, default=0)
    tanaman_aren = models.IntegerField(blank=True, null=True, default=0)
    tanaman_belimbing = models.IntegerField(blank=True, null=True, default=0)
    tanaman_belukar = models.IntegerField(blank=True, null=True, default=0)
    tanaman_bonglai = models.IntegerField(blank=True, null=True, default=0)
    tanaman_buah_naga = models.IntegerField(blank=True, null=True, default=0)
    tanaman_cabai = models.IntegerField(blank=True, null=True, default=0)
    tanaman_cempedak = models.IntegerField(blank=True, null=True, default=0)
    tanaman_cengkeh = models.IntegerField(blank=True, null=True, default=0)
    tanaman_cokelat = models.IntegerField(blank=True, null=True, default=0)
    tanaman_durian = models.IntegerField(blank=True, null=True, default=0)
    tanaman_jahe_merah = models.IntegerField(blank=True, null=True, default=0)
    tanaman_jambu = models.IntegerField(blank=True, null=True, default=0)
    tanaman_jambu_air = models.IntegerField(blank=True, null=True, default=0)
    tanaman_jambu_batu = models.IntegerField(blank=True, null=True, default=0)
    tanaman_jambu_biji = models.IntegerField(blank=True, null=True, default=0)
    tanaman_jati_putih = models.IntegerField(blank=True, null=True, default=0)
    tanaman_jengkol = models.IntegerField(blank=True, null=True, default=0)
    tanaman_jeruk = models.IntegerField(blank=True, null=True, default=0)
    tanaman_jeruk_nipis = models.IntegerField(blank=True, null=True, default=0)
    tanaman_kapuk = models.IntegerField(blank=True, null=True, default=0)
    tanaman_kecombrang = models.IntegerField(blank=True, null=True, default=0)
    tanaman_kelapa = models.IntegerField(blank=True, null=True, default=0)
    tanaman_kelapa_sawit = models.IntegerField(blank=True, null=True, default=0)
    tanaman_kelor = models.IntegerField(blank=True, null=True, default=0)
    tanaman_kopi = models.IntegerField(blank=True, null=True, default=0)
    tanaman_kunyit = models.IntegerField(blank=True, null=True, default=0)
    tanaman_kunyit_hitam = models.IntegerField(blank=True, null=True, default=0)
    tanaman_langsat = models.IntegerField(blank=True, null=True, default=0)
    tanaman_lengkuas = models.IntegerField(blank=True, null=True, default=0)
    tanaman_mangga = models.IntegerField(blank=True, null=True, default=0)
    tanaman_nanas = models.IntegerField(blank=True, null=True, default=0)
    tanaman_nangka = models.IntegerField(blank=True, null=True, default=0)
    tanaman_nilam = models.IntegerField(blank=True, null=True, default=0)
    tanaman_pepaya = models.IntegerField(blank=True, null=True, default=0)
    tanaman_pinang = models.IntegerField(blank=True, null=True, default=0)
    tanaman_rambutan = models.IntegerField(blank=True, null=True, default=0)
    tanaman_serai = models.IntegerField(blank=True, null=True, default=0)
    tanaman_singkong = models.IntegerField(blank=True, null=True, default=0)
    tanaman_sirsak = models.IntegerField(blank=True, null=True, default=0)
    tanaman_sukun = models.IntegerField(blank=True, null=True, default=0)
    tanaman_talas = models.IntegerField(blank=True, null=True, default=0)
    tanaman_ubi = models.IntegerField(blank=True, null=True, default=0)
    
    # R. Lainnya
    benda_lain_tanah = models.TextField(blank=True, null=True)
    pembebanan_hak_tanah = models.TextField(blank=True, null=True)
    perkiraan_dampak = models.TextField(blank=True, null=True)
    keterangan = models.TextField(blank=True, null=True)
    fungsi_kawasan = models.CharField(max_length=200, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'census_kepala_keluarga'
        verbose_name = 'Census Kepala Keluarga'
        verbose_name_plural = 'Census Kepala Keluarga'
        ordering = ['-created_at']
    
    def __str__(self):
        nama_lengkap = ' '.join(filter(None, [self.nama_depan, self.nama_tengah, self.nama_belakang]))
        return f"{self.id_asset} - {nama_lengkap or 'N/A'}"
    
    def save(self, *args, **kwargs):
        if not self.id_asset:
            self.id_asset = generate_asset_id()
        super().save(*args, **kwargs)


class CensusIndividu(models.Model):
    """
    Census Survey - Kuesioner Respons Individu
    Individual family member data linked to household head
    """
    
    # Auto-generated identifiers
    id_asset = models.CharField(max_length=20, db_index=True, editable=False)
    id_project = models.CharField(max_length=50, blank=True, null=True)
    
    # Foreign key to Kepala Keluarga
    kepala_keluarga = models.ForeignKey(
        CensusKepalaKeluarga,
        on_delete=models.CASCADE,
        related_name='anggota_keluarga'
    )
    
    # E. Demografi Rumah Tangga (Individu)
    no_urut = models.IntegerField(blank=True, null=True)
    id_rumah_tangga = models.CharField(max_length=50, blank=True, null=True)
    nama_depan = models.CharField(max_length=100, blank=True, null=True)
    nama_belakang = models.CharField(max_length=100, blank=True, null=True)
    nik = models.CharField(max_length=20, blank=True, null=True)
    hubungan_dengan_kk = models.CharField(max_length=200, blank=True, null=True)
    jenis_kelamin = models.CharField(max_length=200, blank=True, null=True)
    tanggal_lahir = models.DateField(blank=True, null=True)
    usia = models.IntegerField(blank=True, null=True)
    alamat = models.TextField(blank=True, null=True)
    status_perkawinan = models.CharField(max_length=200, blank=True, null=True)
    bisa_membaca_menulis = models.CharField(max_length=200, blank=True, null=True)
    sedang_sekolah = models.CharField(max_length=200, blank=True, null=True)
    sekolah_dimana = models.CharField(max_length=200, blank=True, null=True)
    pendidikan_terakhir = models.CharField(max_length=200, blank=True, null=True)
    alasan_penghentian = models.CharField(max_length=200, blank=True, null=True)
    alasan_penghentian_lainnya = models.TextField(blank=True, null=True)
    disabilitas = models.CharField(max_length=200, blank=True, null=True)
    disabilitas_lainnya = models.TextField(blank=True, null=True)
    kondisi_kesehatan_kronis = models.CharField(max_length=200, blank=True, null=True)
    kondisi_kesehatan_kronis_lainnya = models.TextField(blank=True, null=True)
    nomor_telepon = models.CharField(max_length=20, blank=True, null=True)
    
    # F. Pekerjaan, Keterampilan, dan Tanah (Individu)
    bekerja_12_bulan = models.CharField(max_length=200, blank=True, null=True)
    pekerjaan_utama = models.CharField(max_length=200, blank=True, null=True)
    pekerjaan_utama_lainnya = models.CharField(max_length=200, blank=True, null=True)
    jenis_pekerjaan_utama = models.CharField(max_length=200, blank=True, null=True)
    lokasi_pekerjaan_utama = models.CharField(max_length=200, blank=True, null=True)
    lokasi_pekerjaan_utama_lainnya = models.CharField(max_length=200, blank=True, null=True)
    jumlah_bulan_bekerja = models.IntegerField(blank=True, null=True)
    penghasilan_per_bulan = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    
    pekerjaan_sekunder = models.CharField(max_length=200, blank=True, null=True)
    pekerjaan_sekunder_lainnya = models.CharField(max_length=200, blank=True, null=True)
    lokasi_pekerjaan_sekunder = models.CharField(max_length=200, blank=True, null=True)
    lokasi_pekerjaan_sekunder_lainnya = models.CharField(max_length=200, blank=True, null=True)
    jumlah_bulan_bekerja_sekunder = models.IntegerField(blank=True, null=True)
    penghasilan_sekunder_per_bulan = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    
    keterampilan = models.CharField(max_length=200, blank=True, null=True)
    keterampilan_lainnya = models.CharField(max_length=200, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'census_individu'
        verbose_name = 'Census Individu'
        verbose_name_plural = 'Census Individu'
        ordering = ['kepala_keluarga', 'no_urut']
    
    def __str__(self):
        nama_lengkap = ' '.join(filter(None, [self.nama_depan, self.nama_belakang]))
        return f"{self.id_asset} - {nama_lengkap or 'N/A'} ({self.hubungan_dengan_kk})"
    
    def save(self, *args, **kwargs):
        if not self.id_asset and self.kepala_keluarga:
            self.id_asset = self.kepala_keluarga.id_asset
        if not self.id_rumah_tangga and self.kepala_keluarga:
            self.id_rumah_tangga = self.kepala_keluarga.id_rumah_tangga
        super().save(*args, **kwargs)
