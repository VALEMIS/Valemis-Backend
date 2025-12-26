"""
Models for Census Survey (LARAP - Land Acquisition and Resettlement Action Plan)
This file contains models for socio-economic household surveys.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class CensusSurvey(models.Model):
    """
    Main Census Survey Model - Household Level Data
    Contains all 43 questions from the LARAP Census Survey Template
    """
    # Section A: Identification
    q1_kode_enumerator = models.CharField(max_length=50, verbose_name="Kode Enumerator")
    q2_id_unik = models.CharField(max_length=100, verbose_name="ID Unik (ID Entitas Terdampak)")
    q3_hubungan_responden = models.CharField(max_length=100, blank=True, null=True, verbose_name="Hubungan responden dengan KK")
    q4_identifikasi_dampak = models.CharField(max_length=100, blank=True, null=True, verbose_name="Identifikasi Dampak")
    q5_agama = models.CharField(max_length=50, blank=True, null=True, verbose_name="Agama")
    q6_asal_etnis = models.CharField(max_length=50, blank=True, null=True, verbose_name="Asal etnis")
    q7_bahasa = models.CharField(max_length=50, blank=True, null=True, verbose_name="Bahasa")
    q8_tempat_asal = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tempat Asal Kepala Keluarga")
    q9_hubungan_kk = models.CharField(max_length=100, blank=True, null=True, verbose_name="Hubungan dengan Kepala Keluarga")
    q10_jenis_kelamin = models.CharField(max_length=20, blank=True, null=True, verbose_name="Jenis kelamin")
    q11_status_perkawinan = models.CharField(max_length=50, blank=True, null=True, verbose_name="Status Perkawinan")
    q12_bisa_membaca_menulis = models.CharField(max_length=20, blank=True, null=True, verbose_name="Bisa Membaca/Menulis")
    q13_sedang_sekolah = models.CharField(max_length=10, blank=True, null=True, verbose_name="Sedang Sekolah")
    q14_lokasi_sekolah = models.CharField(max_length=50, blank=True, null=True, verbose_name="Lokasi sekolah")
    q15_pendidikan_terakhir = models.CharField(max_length=50, blank=True, null=True, verbose_name="Tingkat Pendidikan Terakhir")
    q16_alasan_berhenti = models.CharField(max_length=100, blank=True, null=True, verbose_name="Alasan berhenti sekolah")
    q17_disabilitas = models.CharField(max_length=100, blank=True, null=True, verbose_name="Disabilitas")
    q18_kondisi_kesehatan = models.TextField(blank=True, null=True, verbose_name="Kondisi Kesehatan Kronis")
    q19_bekerja_12_bulan = models.CharField(max_length=50, blank=True, null=True, verbose_name="Bekerja dalam 12 bulan terakhir")
    q20_pekerjaan_utama = models.CharField(max_length=100, blank=True, null=True, verbose_name="Pekerjaan Utama")
    q21_jenis_pekerjaan = models.CharField(max_length=100, blank=True, null=True, verbose_name="Jenis pekerjaan")
    q22_lokasi_pekerjaan = models.CharField(max_length=100, blank=True, null=True, verbose_name="Lokasi pekerjaan")
    q23_keterampilan = models.TextField(blank=True, null=True, verbose_name="Keterampilan/profesi (15+ tahun)")
    q24_penyakit_umum = models.TextField(blank=True, null=True, verbose_name="Dua penyakit paling umum")
    q25_tempat_pelayanan = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tempat pelayanan kesehatan")
    q26_kecukupan_pangan = models.CharField(max_length=50, blank=True, null=True, verbose_name="Kecukupan pangan")
    q27_defisit_pangan = models.TextField(blank=True, null=True, verbose_name="Cara menutupi defisit pangan")
    q28_penghasilan_tahunan = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="Penghasilan tahunan")
    q31_pengeluaran_bulanan = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="Pengeluaran bulanan")
    q32_rekening_bank = models.CharField(max_length=10, blank=True, null=True, verbose_name="Punya rekening bank")
    q33_tabungan = models.CharField(max_length=100, blank=True, null=True, verbose_name="Jenis tabungan")
    q34_hutang = models.CharField(max_length=100, blank=True, null=True, verbose_name="Jenis hutang")
    q35_alasan_hutang = models.TextField(blank=True, null=True, verbose_name="Alasan hutang")
    q36_jenis_proyek = models.CharField(max_length=100, blank=True, null=True, verbose_name="Jenis Proyek")
    q37_lokasi_bisnis = models.CharField(max_length=100, blank=True, null=True, verbose_name="Lokasi bisnis")
    q38_kepemilikan_bisnis = models.CharField(max_length=100, blank=True, null=True, verbose_name="Kepemilikan bisnis")
    q39_jenis_bisnis = models.CharField(max_length=100, blank=True, null=True, verbose_name="Jenis bisnis")
    q40_tipe_rumah = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tipe rumah")
    q41_pelayanan_listrik = models.CharField(max_length=100, blank=True, null=True, verbose_name="Pelayanan Listrik")
    q42_sumber_air = models.CharField(max_length=100, blank=True, null=True, verbose_name="Sumber Air Minum")
    q43_sanitasi = models.CharField(max_length=100, blank=True, null=True, verbose_name="Sanitasi")
    q44_karakteristik_khusus = models.TextField(blank=True, null=True, verbose_name="Karakteristik khusus")
    q45_pembagian_kerja = models.CharField(max_length=50, blank=True, null=True, verbose_name="Pembagian kerja laki-perempuan")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat pada")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Diperbarui pada")
    surveyed_by = models.CharField(max_length=100, blank=True, null=True, verbose_name="Disurvei oleh")
    survey_date = models.DateField(blank=True, null=True, verbose_name="Tanggal survei")
    coordinates = models.CharField(max_length=100, blank=True, null=True, verbose_name="Koordinat")
    village = models.CharField(max_length=100, blank=True, null=True, verbose_name="Desa")
    district = models.CharField(max_length=100, blank=True, null=True, verbose_name="Kecamatan")
    regency = models.CharField(max_length=100, blank=True, null=True, verbose_name="Kabupaten")
    province = models.CharField(max_length=100, blank=True, null=True, verbose_name="Provinsi")
    notes = models.TextField(blank=True, null=True, verbose_name="Catatan")

    class Meta:
        db_table = 'census_survey'
        verbose_name = "Census Survey"
        verbose_name_plural = "Census Surveys"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.q1_kode_enumerator} - {self.q2_id_unik}"


class CensusMember(models.Model):
    """
    Individual household members (for questions at individual level)
    Links to main CensusSurvey
    """
    GENDER_CHOICES = [
        ('1', 'Laki-laki'),
        ('2', 'Perempuan'),
        ('97', 'Lainnya'),
    ]

    RELATIONSHIP_CHOICES = [
        ('1', 'Kepala Keluarga'),
        ('2', 'Pasangan'),
        ('3', 'Anak Laki-laki / Anak Perempuan'),
        ('4', 'Menantu Laki-laki / Menantu Perempuan'),
        ('5', 'Cucu Laki-laki / Cucu Perempuan'),
        ('6', 'Ayah / Ibu'),
        ('7', 'Mertua'),
        ('8', 'Saudara Laki-laki / Saudara Perempuan'),
        ('9', 'Ipar Laki-laki / Ipar Perempuan'),
        ('10', 'Kerabat lain'),
        ('11', 'Sepupu'),
        ('12', 'Bukan kerabat lain'),
    ]

    # Link to household survey
    household = models.ForeignKey(CensusSurvey, on_delete=models.CASCADE, related_name='members', verbose_name="Rumah Tangga")

    # Member information
    nama_depan = models.CharField(max_length=100, verbose_name="Nama Depan")
    nama_tengah = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nama Tengah")
    nama_belakang = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nama Belakang")
    hubungan_kk = models.CharField(max_length=50, choices=RELATIONSHIP_CHOICES, verbose_name="Hubungan dengan KK")
    jenis_kelamin = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Jenis kelamin")
    usia = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(150)], verbose_name="Usia")
    status_perkawinan = models.CharField(max_length=50, blank=True, null=True, verbose_name="Status Perkawinan")
    bisa_membaca_menulis = models.CharField(max_length=20, blank=True, null=True, verbose_name="Bisa Membaca/Menulis")
    sedang_sekolah = models.CharField(max_length=10, blank=True, null=True, verbose_name="Sedang Sekolah")
    lokasi_sekolah = models.CharField(max_length=50, blank=True, null=True, verbose_name="Lokasi sekolah")
    pendidikan_terakhir = models.CharField(max_length=50, blank=True, null=True, verbose_name="Pendidikan Terakhir")
    alasan_berhenti = models.CharField(max_length=100, blank=True, null=True, verbose_name="Alasan berhenti sekolah")
    disabilitas = models.CharField(max_length=100, blank=True, null=True, verbose_name="Disabilitas")
    kondisi_kesehatan = models.TextField(blank=True, null=True, verbose_name="Kondisi Kesehatan Kronis")
    bekerja_12_bulan = models.CharField(max_length=50, blank=True, null=True, verbose_name="Bekerja dalam 12 bulan")
    pekerjaan_utama = models.CharField(max_length=100, blank=True, null=True, verbose_name="Pekerjaan Utama")
    jenis_pekerjaan = models.CharField(max_length=100, blank=True, null=True, verbose_name="Jenis pekerjaan")
    lokasi_pekerjaan = models.CharField(max_length=100, blank=True, null=True, verbose_name="Lokasi pekerjaan")
    keterampilan = models.TextField(blank=True, null=True, verbose_name="Keterampilan/profesi")

    class Meta:
        db_table = 'census_member'
        verbose_name = "Census Member"
        verbose_name_plural = "Census Members"
        ordering = ['household', 'id']

    def __str__(self):
        return f"{self.nama_depan} {self.nama_belakang} - {self.household.q2_id_unik}"


class CensusQuestion(models.Model):
    """
    Master list of questions with their dropdown options
    """
    question_number = models.IntegerField(unique=True, verbose_name="Nomor Soal")
    question_text = models.TextField(verbose_name="Pertanyaan")
    field_name = models.CharField(max_length=100, unique=True, verbose_name="Nama Field")
    category = models.CharField(max_length=100, blank=True, null=True, verbose_name="Kategori")
    options = models.JSONField(default=list, verbose_name="Opsi Jawaban")
    is_required = models.BooleanField(default=False, verbose_name="Wajib Diisi")
    validation_type = models.CharField(max_length=50, blank=True, null=True,
                                       choices=[('text', 'Text'), ('number', 'Number'),
                                              ('date', 'Date'), ('email', 'Email')],
                                       verbose_name="Tipe Validasi")

    class Meta:
        db_table = 'census_question'
        verbose_name = "Census Question"
        verbose_name_plural = "Census Questions"
        ordering = ['question_number']

    def __str__(self):
        return f"{self.question_number}. {self.question_text[:50]}"
