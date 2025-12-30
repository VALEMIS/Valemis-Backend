import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# -----------------------------
# CACHE
# -----------------------------
class Cache(models.Model):
    key = models.CharField(max_length=255, primary_key=True)
    value = models.TextField()
    expiration = models.BigIntegerField()
    # tes = models.GeometryField
    class Meta:
        db_table = "cache"


# -----------------------------
# FAILED JOBS
# -----------------------------
class FailedJob(models.Model):
    uuid = models.CharField(max_length=255)
    connection = models.TextField()
    queue = models.TextField()
    payload = models.TextField()
    exception = models.TextField()
    failed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "failed_jobs"


# -----------------------------
# IDENTITAS
# -----------------------------
class Identitas(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=255, null=True, blank=True)
    alamat_1 = models.CharField(max_length=255, null=True, blank=True)
    alamat_1_desa = models.CharField(max_length=255, null=True, blank=True)
    alamat_1_kota = models.CharField(max_length=255, null=True, blank=True)
    alamat_2 = models.CharField(max_length=255, null=True, blank=True)
    alamat_2_desa = models.CharField(max_length=255, null=True, blank=True)
    alamat_2_kota = models.CharField(max_length=255, null=True, blank=True)
    pekerjaan = models.CharField(max_length=255, null=True, blank=True)
    tempat_lahir = models.CharField(max_length=255, null=True, blank=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    nik = models.CharField(max_length=50, null=True, blank=True)
    no_hp = models.CharField(max_length=50, null=True, blank=True)
    pendapatan_per_bulan = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "identitas"


# -----------------------------
# JOB BATCHES
# -----------------------------
class JobBatch(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    total_jobs = models.IntegerField()
    pending_jobs = models.IntegerField()
    failed_jobs = models.IntegerField()
    failed_job_ids = models.TextField()
    options = models.TextField(null=True, blank=True)
    cancelled_at = models.BigIntegerField(null=True, blank=True)
    created_at = models.BigIntegerField()
    finished_at = models.BigIntegerField(null=True, blank=True)

    class Meta:
        db_table = "job_batches"


# -----------------------------
# JOBS
# -----------------------------
class Job(models.Model):
    queue = models.CharField(max_length=255)
    payload = models.TextField()
    attempts = models.PositiveSmallIntegerField()
    reserved_at = models.BigIntegerField(null=True, blank=True)
    available_at = models.BigIntegerField()
    created_at = models.BigIntegerField()

    class Meta:
        db_table = "jobs"
        indexes = [
            models.Index(fields=["queue"], name="jobs_queue_index")
        ]


# -----------------------------
# KUESIONER
# -----------------------------
class Kuesioner(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    judul = models.CharField(max_length=255, null=True, blank=True)
    deskripsi = models.TextField(null=True, blank=True)
    slug = models.CharField(max_length=255, unique=True)
    aktif = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "kuesioner"


# -----------------------------
# KUESIONER PERTANYAAN GRUP
# -----------------------------
class KuesionerPertanyaanGrup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kuesioner = models.ForeignKey(
        Kuesioner,
        on_delete=models.CASCADE,
        related_name="grup_pertanyaan"
    )
    judul = models.CharField(max_length=255, null=True, blank=True)
    deskripsi = models.TextField(null=True, blank=True)
    urutan = models.IntegerField()
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "kuesioner_pertanyaan_grup"


# -----------------------------
# KUESIONER PERTANYAAN
# -----------------------------
class KuesionerPertanyaan(models.Model):
    TIPE_CHOICES = [
        ("text", "Text"),
        ("number", "Number"),
        ("radio", "Radio"),
        ("checkbox", "Checkbox"),
        ("select", "Select"),
        ("textarea", "Textarea"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kuesioner = models.ForeignKey(
        Kuesioner,
        on_delete=models.CASCADE,
        related_name="pertanyaan"
    )
    pertanyaan_grup = models.ForeignKey(
        KuesionerPertanyaanGrup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pertanyaan"
    )
    pertanyaan = models.TextField(null=True, blank=True)
    tipe = models.CharField(max_length=50, null=True, blank=True, choices=TIPE_CHOICES)
    wajib_diisi = models.BooleanField(default=False)
    urutan = models.IntegerField()
    deskripsi = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "kuesioner_pertanyaan"


# -----------------------------
# KUESIONER PERTANYAAN OPSI
# -----------------------------
class KuesionerPertanyaanOpsi(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pertanyaan = models.ForeignKey(
        KuesionerPertanyaan,
        on_delete=models.CASCADE,
        related_name="opsi"
    )
    opsi_teks = models.CharField(max_length=255, null=True, blank=True)
    opsi_nilai = models.CharField(max_length=100, null=True, blank=True)
    urutan = models.IntegerField()
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "kuesioner_pertanyaan_opsi"


# -----------------------------
# KUESIONER RESPONDEN
# -----------------------------
class KuesionerResponden(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    identitas = models.ForeignKey(
        Identitas,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="respon_kuesioner"
    )
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "kuesioner_responden"


# -----------------------------
# ASET BANGUNAN RESPONDEN
# -----------------------------
class KuesionerRespondenAsetBangunan(models.Model):
    persil_id = models.BigIntegerField()
    jenis_bangunan = models.CharField(max_length=100, null=True, blank=True)
    luas_m2 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    permanen = models.BooleanField(null=True)
    bangunan_utama = models.CharField(max_length=50, null=True, blank=True)
    material_utama = models.CharField(max_length=100, null=True, blank=True)
    sanitasi = models.BooleanField(null=True)
    listrik = models.BooleanField(null=True)
    suplai_air = models.BooleanField(null=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "kuesioner_responden_aset_bangunan"
        indexes = [
            models.Index(fields=["persil_id"], name="kues_aset_persil_idx")
        ]




# ----------------------------LIITGASI------------------------------------- 
# ----------------------------LIITGASI------------------------------------- 
# ----------------------------LIITGASI------------------------------------- 
# ----------------------------LIITGASI------------------------------------- 
# ----------------------------LIITGASI------------------------------------- 

class PolygonClaim(models.Model):
    polygon_claim_id = models.AutoField(primary_key=True)
    geom_wkt = models.TextField()
    type_poligon = models.TextField()
    sumber_data = models.TextField()

    class Meta:
        db_table = 'tbl_Polygon_claim'
        verbose_name = 'Polygon Claim'
        verbose_name_plural = 'Polygon Claims'

    def __str__(self):
        return f"Polygon Claim {self.polygon_claim_id}"

class Parcel(models.Model):
    id_parcel = models.AutoField(primary_key=True)
    nama_parcel = models.TextField()
    desa = models.TextField()
    kecamatan = models.TextField()
    kabupaten = models.TextField()
    provinsi = models.TextField()
    status_penguasaan = models.TextField()
    nomor_sertifikat = models.TextField()
    pemegang_hak = models.TextField()
    area_ha = models.FloatField()
    srid = models.IntegerField()
    polygon_claim = models.ForeignKey(PolygonClaim, on_delete=models.CASCADE, db_column='Polygon_CLaim_ID')
    sumber_data = models.TextField()

    class Meta:
        db_table = 'tbl_parcel'
        verbose_name = 'Parcel'
        verbose_name_plural = 'Parcels'

    def __str__(self):
        return self.nama_parcel

class StatusLahan(models.Model):
    pid_lahan = models.AutoField(primary_key=True)
    id_parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE)
    stage = models.TextField()
    status_lahan = models.TextField()
    tgl_inven = models.DateField()
    tgl_bebas = models.DateField(null=True, blank=True)
    penggunaan_ops = models.TextField()
    bln_thn_penggunaan = models.TextField()
    keterangan = models.TextField()
    poligon_sub_spasial = models.TextField()

    class Meta:
        db_table = 'tbl_Status Lahan'
        verbose_name = 'Status Lahan'
        verbose_name_plural = 'Status Lahan'

    def __str__(self):
        return f"Status Lahan {self.pid_lahan}"

class PenggunaanLahan(models.Model):
    id_reclaim_act = models.AutoField(primary_key=True)
    id_reclaim_area = models.IntegerField()
    tanggal = models.DateField()
    aktivitas = models.TextField()
    luas_ha = models.FloatField()
    area = models.TextField()
    survival_rate_pct = models.FloatField()
    dokumen = models.TextField()
    sub_spasial = models.TextField()

    class Meta:
        db_table = 'tbl_Penggunaan Lahan'
        verbose_name = 'Penggunaan Lahan'
        verbose_name_plural = 'Penggunaan Lahan'

    def __str__(self):
        return f"Penggunaan Lahan {self.id_reclaim_act}"

class Stakeholder(models.Model):
    sh_id = models.AutoField(primary_key=True)
    nama = models.TextField()
    tipe = models.TextField()
    kategori = models.TextField()
    alamat = models.TextField()
    kontak = models.TextField()
    srid = models.IntegerField()
    geom_wkt = models.TextField()
    interest_1_5_incase = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    influence_1_5_incase = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        db_table = 'tbl_stakeholder'
        verbose_name = 'Stakeholder'
        verbose_name_plural = 'Stakeholders'

    def __str__(self):
        return self.nama

class Claim(models.Model):
    id_claim = models.AutoField(primary_key=True)
    id_parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE)
    tanggal_mulai = models.DateField()
    jenis_claim = models.TextField()
    uraian = models.TextField()
    status = models.TextField()
    kanal = models.TextField()
    sumber = models.TextField()
    dokumen_klaim = models.TextField()

    class Meta:
        db_table = 'tbl_claim'
        verbose_name = 'Claim'
        verbose_name_plural = 'Claims'

    def __str__(self):
        return f"Claim {self.id_claim}"

class ClaimRiwayat(models.Model):
    id_claim_hist = models.AutoField(primary_key=True)
    id_claim = models.ForeignKey(Claim, on_delete=models.CASCADE)
    tanggal = models.DateField()
    status = models.TextField()
    deskripsi = models.TextField()
    petugas = models.TextField()
    dokumen = models.TextField()

    class Meta:
        db_table = 'tbl_claim_riwayat'
        verbose_name = 'Claim Riwayat'
        verbose_name_plural = 'Claim Riwayat'

    def __str__(self):
        return f"Riwayat Claim {self.id_claim_hist}"

class Komplain(models.Model):
    id_komplain = models.AutoField(primary_key=True)
    id_parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE)
    tanggal = models.DateField()
    id_pelapor_stakeholder = models.ForeignKey(Stakeholder, on_delete=models.CASCADE)
    ringkas = models.TextField()
    detail = models.TextField()
    kategori = models.TextField()
    kanal_penerimaan = models.TextField()
    tingkat_dampak_1_5 = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    prioritas_1_5 = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    status = models.TextField()
    dokumen = models.TextField()

    class Meta:
        db_table = 'tbl_komplain'
        verbose_name = 'Komplain'
        verbose_name_plural = 'Komplain'

    def __str__(self):
        return f"Komplain {self.id_komplain}"

class StakeholderInvolvement(models.Model):
    id_involvement = models.AutoField(primary_key=True)
    object_type = models.TextField()
    object_id = models.IntegerField()
    sh_id = models.ForeignKey(Stakeholder, on_delete=models.CASCADE)
    peran = models.TextField()
    sejak = models.DateField()
    hingga = models.DateField(null=True, blank=True)
    catatan = models.TextField()

    class Meta:
        db_table = 'tbl_stakeholder_involvement'
        verbose_name = 'Stakeholder Involvement'
        verbose_name_plural = 'Stakeholder Involvements'

    def __str__(self):
        return f"Involvement {self.id_involvement}"

class Mediasi(models.Model):
    id_mediasi = models.AutoField(primary_key=True)
    id_claim = models.ForeignKey(Claim, on_delete=models.CASCADE)
    tanggal_mulai = models.DateField()
    tanggal_selesai = models.DateField(null=True, blank=True)
    mediator = models.TextField()
    lokasi = models.TextField()
    hasil = models.TextField()
    ringkasan = models.TextField()
    dokumen = models.TextField()

    class Meta:
        db_table = 'tbl_mediasi'
        verbose_name = 'Mediasi'
        verbose_name_plural = 'Mediasi'

    def __str__(self):
        return f"Mediasi {self.id_mediasi}"

class MediasiSesi(models.Model):
    id_sesi = models.AutoField(primary_key=True)
    id_mediasi = models.ForeignKey(Mediasi, on_delete=models.CASCADE)
    tanggal = models.DateField()
    agenda = models.TextField()
    hasil = models.TextField()
    notulen = models.TextField()

    class Meta:
        db_table = 'tbl_mediasi_sesi'
        verbose_name = 'Mediasi Sesi'
        verbose_name_plural = 'Mediasi Sesi'

    def __str__(self):
        return f"Sesi {self.id_sesi}"

class Pidana(models.Model):
    id_pidana = models.AutoField(primary_key=True)
    id_claim = models.ForeignKey(Claim, on_delete=models.CASCADE)
    nomor_lp = models.TextField()
    pasal_diduga = models.TextField()
    instansi = models.TextField()
    status = models.TextField()
    tanggal_mulai = models.DateField()
    tanggal_akhir = models.DateField(null=True, blank=True)
    ringkasan = models.TextField()

    class Meta:
        db_table = 'tbl_pidana'
        verbose_name = 'Pidana'
        verbose_name_plural = 'Pidana'

    def __str__(self):
        return f"Pidana {self.id_pidana}"

class Perdata(models.Model):
    id_perdata = models.AutoField(primary_key=True)
    id_claim = models.ForeignKey(Claim, on_delete=models.CASCADE)
    nomor_perkara = models.TextField()
    tingkat = models.TextField()
    pengadilan = models.TextField()
    status = models.TextField()
    tanggal_mulai = models.DateField()
    tanggal_putus = models.DateField(null=True, blank=True)
    pokok_perkara = models.TextField()
    nilai_ganti_rugi = models.FloatField()

    class Meta:
        db_table = 'tbl_perdata'
        verbose_name = 'Perdata'
        verbose_name_plural = 'Perdata'

    def __str__(self):
        return f"Perdata {self.id_perdata}"

class Putusan(models.Model):
    id_putusan = models.AutoField(primary_key=True)
    case_type = models.TextField()
    id_case = models.IntegerField()
    tingkat = models.TextField()
    nomor_putusan = models.TextField()
    tanggal_putus = models.DateField()
    hasil = models.TextField()
    ringkasan = models.TextField()
    tautan_putusan = models.TextField()

    class Meta:
        db_table = 'tbl_putusan'
        verbose_name = 'Putusan'
        verbose_name_plural = 'Putusan'

    def __str__(self):
        return f"Putusan {self.nomor_putusan}"

class PerkaraTimeline(models.Model):
    id_event = models.AutoField(primary_key=True)
    case_type = models.TextField()
    id_case = models.IntegerField()
    tanggal = models.DateField()
    stage = models.TextField()
    catatan = models.TextField()
    dokumen = models.TextField()

    class Meta:
        db_table = 'tbl_perkara_timeline'
        verbose_name = 'Perkara Timeline'
        verbose_name_plural = 'Perkara Timeline'

    def __str__(self):
        return f"Event {self.id_event}"

class Bukti(models.Model):
    id_bukti = models.AutoField(primary_key=True)
    object_type = models.TextField()
    object_id = models.IntegerField()
    kategori = models.TextField()
    deskripsi = models.TextField()
    file_ref = models.TextField()

    class Meta:
        db_table = 'tbl_bukti'
        verbose_name = 'Bukti'
        verbose_name_plural = 'Bukti'

    def __str__(self):
        return f"Bukti {self.id_bukti}"

class Log(models.Model):
    id_log = models.AutoField(primary_key=True)
    object_type = models.TextField()
    object_id = models.IntegerField()
    tanggal = models.DateField()
    aktor = models.TextField()
    aksi = models.TextField()
    catatan = models.TextField()

    class Meta:
        db_table = 'tbl_log'
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'

    def __str__(self):
        return f"Log {self.id_log}"


# =============================================================================
# NEW MODELS - Valemis ERP Modules
# =============================================================================

# =============================================================================
# 1. ASSET INVENTORY MODULE - KUESIONER (Census Survey)
# =============================================================================
class AssetInventory(models.Model):
    """
    Asset Inventory / Census Survey - Complete Kuisioner Structure
    105 fields matching the Excel Kuisioner sheet exactly
    """

    # ===== A. IDENTIFIKASI RUMAH TANGGA DAN PAP =====
    kode_enumerator = models.CharField(max_length=50, null=True, blank=True, verbose_name='1. Kode Enumerator')
    id_rumah_tangga = models.CharField(max_length=50, null=True, blank=True, verbose_name='2. ID Rumah Tangga')
    tanggal = models.DateField(null=True, blank=True, verbose_name='3. Tanggal')
    kode_foto_survei = models.CharField(max_length=50, null=True, blank=True, verbose_name='4. Kode Foto Survei')
    id_unik = models.CharField(max_length=100, null=True, blank=True, verbose_name='5. ID Unik (Entitas Terdampak)')
    koordinat = models.CharField(max_length=100, null=True, blank=True, verbose_name='6. Koordinat')

    # ===== B. INFORMASI KEPALA KELUARGA =====
    nama_depan = models.CharField(max_length=100, null=True, blank=True, verbose_name='7. Nama Depan')
    nama_tengah = models.CharField(max_length=100, null=True, blank=True, verbose_name='8. Nama Tengah')
    nama_belakang = models.CharField(max_length=100, null=True, blank=True, verbose_name='9. Nama Belakang')
    nama_ayah = models.CharField(max_length=100, null=True, blank=True, verbose_name='10. Nama Ayah')
    nama_kakek = models.CharField(max_length=100, null=True, blank=True, verbose_name='11. Nama Kakek')
    nama_pasangan = models.CharField(max_length=100, null=True, blank=True, verbose_name='12. Nama Pasangan')
    nomor_telepon = models.CharField(max_length=20, null=True, blank=True, verbose_name='13. Nomor Telepon')
    nik = models.CharField(max_length=20, null=True, blank=True, verbose_name='14. NIK')
    desa = models.CharField(max_length=100, null=True, blank=True, verbose_name='15. Desa')
    kecamatan = models.CharField(max_length=100, null=True, blank=True, verbose_name='16. Kecamatan')
    kabupaten = models.CharField(max_length=100, null=True, blank=True, verbose_name='17. Kabupaten')
    provinsi = models.CharField(max_length=100, null=True, blank=True, verbose_name='18. Provinsi')
    nama_responden = models.CharField(max_length=255, null=True, blank=True, verbose_name='19. Nama Responden')
    hubungan_responden_kk = models.CharField(max_length=100, null=True, blank=True, verbose_name='20. Hubungan Responden dengan KK')
    agama = models.CharField(max_length=50, null=True, blank=True, verbose_name='22. Agama')
    agama_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Agama Lainnya')
    asal_etnis = models.CharField(max_length=100, null=True, blank=True, verbose_name='23. Asal Etnis')
    asal_etnis_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Asal Etnis Lainnya')
    bahasa = models.CharField(max_length=100, null=True, blank=True, verbose_name='24. Bahasa')
    bahasa_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Bahasa Lainnya')
    tempat_asal_kk = models.CharField(max_length=100, null=True, blank=True, verbose_name='25. Tempat Asal KK')
    tempat_asal_tentukan = models.CharField(max_length=100, null=True, blank=True, verbose_name='Tentukan Tempat Asal')
    jumlah_orang_rumah_tangga = models.IntegerField(null=True, blank=True, verbose_name='26. Jumlah Orang di Rumah Tangga')
    no_anggota = models.IntegerField(null=True, blank=True, verbose_name='No.')
    id_dampak = models.CharField(max_length=50, null=True, blank=True, verbose_name='27. ID Dampak')
    anggota_nama_depan = models.CharField(max_length=100, null=True, blank=True, verbose_name='28. Nama Depan (Anggota)')
    anggota_nama_belakang = models.CharField(max_length=100, null=True, blank=True, verbose_name='29. Nama Belakang (Anggota)')
    hubungan_kk = models.CharField(max_length=100, null=True, blank=True, verbose_name='30. Hubungan dengan KK')
    jenis_kelamin = models.CharField(max_length=20, null=True, blank=True, verbose_name='31. Jenis Kelamin')
    usia = models.IntegerField(null=True, blank=True, verbose_name='32. Usia')
    status_perkawinan = models.CharField(max_length=50, null=True, blank=True, verbose_name='33. Status Perkawinan')
    bisa_membaca_menulis = models.CharField(max_length=20, null=True, blank=True, verbose_name='34. Bisa Membaca/Menulis')
    sedang_sekolah = models.CharField(max_length=10, null=True, blank=True, verbose_name='35. Sedang Sekolah')
    lokasi_sekolah = models.CharField(max_length=50, null=True, blank=True, verbose_name='36. Lokasi Sekolah')
    pendidikan_terakhir = models.CharField(max_length=50, null=True, blank=True, verbose_name='37. Pendidikan Terakhir')
    alasan_penghentian = models.CharField(max_length=100, null=True, blank=True, verbose_name='38. Alasan Penghentian')
    alasan_penghentian_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Alasan Penghentian Lainnya')
    disabilitas = models.CharField(max_length=100, null=True, blank=True, verbose_name='39. Disabilitas')
    disabilitas_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Disabilitas Lainnya')
    kondisi_kesehatan_kronis = models.TextField(null=True, blank=True, verbose_name='40. Kondisi Kesehatan Kronis')
    kesehatan_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Kesehatan Lainnya')
    bekerja_12_bulan = models.CharField(max_length=50, null=True, blank=True, verbose_name='41. Bekerja 12 Bulan')
    pekerjaan_utama = models.CharField(max_length=100, null=True, blank=True, verbose_name='42. Pekerjaan Utama')
    pekerjaan_utama_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Pekerjaan Utama Lainnya')
    jenis_pekerjaan = models.CharField(max_length=100, null=True, blank=True, verbose_name='43. Jenis Pekerjaan')
    lokasi_pekerjaan = models.CharField(max_length=100, null=True, blank=True, verbose_name='44. Lokasi Pekerjaan')
    lokasi_pekerjaan_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Lokasi Pekerjaan Lainnya')
    jumlah_bulan_bekerja = models.IntegerField(null=True, blank=True, verbose_name='45. Jumlah Bulan Bekerja')
    penghasilan_per_bulan = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='46. Penghasilan per Bulan')
    pekerjaan_sekunder = models.CharField(max_length=100, null=True, blank=True, verbose_name='47. Pekerjaan Sekunder')
    pekerjaan_sekunder_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Pekerjaan Sekunder Lainnya')
    lokasi_pekerjaan_sekunder = models.CharField(max_length=100, null=True, blank=True, verbose_name='48. Lokasi Sekunder')
    lokasi_pekerjaan_sekunder_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Lokasi Sekunder Lainnya')
    jumlah_bulan_bekerja_sekunder = models.IntegerField(null=True, blank=True, verbose_name='49. Jumlah Bulan Sekunder')
    penghasilan_sekunder_per_bulan = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='50. Penghasilan Sekunder')
    keterampilan = models.TextField(null=True, blank=True, verbose_name='51. Keterampilan/Profesi')
    keterampilan_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Keterampilan Lainnya')
    penyakit_umum = models.TextField(null=True, blank=True, verbose_name='55. Penyakit Umum')
    tempat_pelayanan = models.CharField(max_length=100, null=True, blank=True, verbose_name='56. Tempat Pelayanan')
    kecukupan_pangan = models.CharField(max_length=50, null=True, blank=True, verbose_name='57. Kecukupan Pangan')
    defisit_pangan = models.TextField(null=True, blank=True, verbose_name='58. Defisit Pangan')
    defisit_pangan_lainnya = models.CharField(max_length=200, null=True, blank=True, verbose_name='Defisit Pangan Lainnya')
    penghasilan_tahunan = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='59. Penghasilan Tahunan')
    pengeluaran_bulanan = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='60. Pengeluaran Bulanan')
    rekening_bank = models.CharField(max_length=10, null=True, blank=True, verbose_name='61. Rekening Bank')
    tabungan = models.CharField(max_length=100, null=True, blank=True, verbose_name='62. Tabungan')
    hutang = models.CharField(max_length=100, null=True, blank=True, verbose_name='63. Hutang')
    tabungan_detail = models.CharField(max_length=100, null=True, blank=True, verbose_name='64. Tabungan Detail')
    tabungan_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Tabungan Lainnya')
    hutang_detail = models.CharField(max_length=100, null=True, blank=True, verbose_name='65. Hutang Detail')
    hutang_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Hutang Lainnya')
    alasan_hutang = models.TextField(null=True, blank=True, verbose_name='66. Alasan Hutang')
    alasan_hutang_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Alasan Hutang Lainnya')
    pernah_dampak_proyek = models.CharField(max_length=10, null=True, blank=True, verbose_name='67. Pernah Dampak Proyek')
    jenis_proyek = models.CharField(max_length=100, null=True, blank=True, verbose_name='68. Jenis Proyek')
    jenis_proyek_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Jenis Proyek Lainnya')
    luas_lahan_dibebaskan = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='69. Luas Lahan (m2)')
    pernah_pengungsi = models.CharField(max_length=10, null=True, blank=True, verbose_name='70. Pernah Pengungsi')
    punya_bisnis = models.CharField(max_length=10, null=True, blank=True, verbose_name='71. Punya Bisnis')
    lokasi_bisnis = models.CharField(max_length=100, null=True, blank=True, verbose_name='72. Lokasi Bisnis')
    lokasi_bisnis_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Lokasi Bisnis Lainnya')
    kepemilikan_bisnis = models.CharField(max_length=100, null=True, blank=True, verbose_name='73. Kepemilikan Bisnis')
    kepemilikan_bisnis_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Kepemilikan Bisnis Lainnya')
    sejak_kapan_bisnis = models.CharField(max_length=50, null=True, blank=True, verbose_name='74. Sejak Kapan Bisnis')
    jenis_bisnis = models.CharField(max_length=100, null=True, blank=True, verbose_name='75. Jenis Bisnis')
    jenis_bisnis_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Jenis Bisnis Lainnya')
    jumlah_pegawai = models.IntegerField(null=True, blank=True, verbose_name='76. Jumlah Pegawai')
    pendapatan_rata_bisnis = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='77. Pendapatan Rata Bisnis')
    deskripsi_produk_layanan = models.TextField(null=True, blank=True, verbose_name='78. Deskripsi Produk')
    tipe_rumah = models.CharField(max_length=100, null=True, blank=True, verbose_name='79. Tipe Rumah')
    tipe_rumah_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Tipe Rumah Lainnya')
    pelayanan_listrik = models.CharField(max_length=100, null=True, blank=True, verbose_name='80. Pelayanan Listrik')
    pelayanan_listrik_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Pelayanan Listrik Lainnya')
    sumber_air = models.CharField(max_length=100, null=True, blank=True, verbose_name='81. Sumber Air')
    sumber_air_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Sumber Air Lainnya')
    sanitasi = models.CharField(max_length=100, null=True, blank=True, verbose_name='82. Sanitasi')
    karakteristik_khusus = models.TextField(null=True, blank=True, verbose_name='83. Karakteristik Khusus')
    sumber_informasi = models.CharField(max_length=100, null=True, blank=True, verbose_name='88. Sumber Informasi')
    metode_komunikasi = models.CharField(max_length=100, null=True, blank=True, verbose_name='89. Metode Komunikasi')

    # ===== METADATA =====
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat pada')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Diperbarui pada')
    surveyed_by = models.CharField(max_length=100, null=True, blank=True, verbose_name='Disurvei oleh')
    notes = models.TextField(null=True, blank=True, verbose_name='Catatan')

    class Meta:
        db_table = 'asset_inventory'
        verbose_name = 'Asset Inventory (Kuisioner)'
        verbose_name_plural = 'Asset Inventories (Kuisioner)'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.kode_enumerator or self.id_rumah_tangga or 'N/A'} - {self.nama_depan or ''} {self.nama_belakang or ''}"


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
    jenis_tanah = models.CharField(max_length=100, null=True, blank=True, verbose_name='Jenis Tanah')
    terdaftar_di = models.CharField(max_length=100, null=True, blank=True, verbose_name='Terdaftar Di')
    luas_m2 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Luas (m2)')
    status_pemilik = models.CharField(max_length=100, null=True, blank=True, verbose_name='Status Pemilik')
    pemilik_sebelumnya = models.CharField(max_length=255, null=True, blank=True, verbose_name='Pemilik Sebelumnya')
    tenurial = models.CharField(max_length=10, null=True, blank=True, verbose_name='Tenurial (Y/T)')  # Y/T
    catatan_tanah = models.TextField(null=True, blank=True, verbose_name='Catatan')

    # ===== TANAMAN (Crops) Fields =====
    jenis_tanaman = models.CharField(max_length=100, null=True, blank=True, verbose_name='Jenis Tanaman')
    usia_tanaman = models.IntegerField(null=True, blank=True, verbose_name='Usia Tanaman')
    kondisi_tanaman = models.CharField(max_length=100, null=True, blank=True, verbose_name='Kondisi Tanaman')
    sumber_air_tanaman = models.CharField(max_length=100, null=True, blank=True, verbose_name='Sumber Air')
    gambar_tanaman = models.CharField(max_length=255, null=True, blank=True, verbose_name='Gambar')

    # ===== POHON (Trees) Fields =====
    jenis_pohon = models.CharField(max_length=100, null=True, blank=True, verbose_name='Jenis Pohon')
    jumlah_pohon = models.IntegerField(null=True, blank=True, verbose_name='Jumlah Pohon')
    luas_pohon = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Luas Pohon')
    produktif = models.CharField(max_length=10, null=True, blank=True, verbose_name='Produktif (Y/T)')  # Y/T
    dewasa = models.CharField(max_length=10, null=True, blank=True, verbose_name='Dewasa (Y/T)')  # Y/T
    produksi_per_tahun = models.CharField(max_length=100, null=True, blank=True, verbose_name='Produksi per Tahun')
    kondisi_pohon = models.CharField(max_length=100, null=True, blank=True, verbose_name='Kondisi Pohon')
    gambar1_pohon = models.CharField(max_length=255, null=True, blank=True, verbose_name='Gambar 1')
    gambar2_pohon = models.CharField(max_length=255, null=True, blank=True, verbose_name='Gambar 2')
    gambar3_pohon = models.CharField(max_length=255, null=True, blank=True, verbose_name='Gambar 3')

    # ===== BANGUNAN (Buildings) Fields =====
    jenis_bangunan = models.CharField(max_length=100, null=True, blank=True, verbose_name='Jenis Bangunan')
    luas_bangunan = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Luas Bangunan')
    permanen_sementara = models.CharField(max_length=50, null=True, blank=True, verbose_name='Permanen/Sementara')
    primer_sekunder = models.CharField(max_length=50, null=True, blank=True, verbose_name='Primer/Sekunder')
    bahan_utama = models.CharField(max_length=100, null=True, blank=True, verbose_name='Bahan Utama')
    sanitarian = models.CharField(max_length=100, null=True, blank=True, verbose_name='Sanitarian')
    pasokan_listrik = models.CharField(max_length=100, null=True, blank=True, verbose_name='Pasokan Listrik')
    persediaan_air = models.CharField(max_length=100, null=True, blank=True, verbose_name='Persediaan Air')
    gambar1_bangunan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Gambar 1')
    gambar2_bangunan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Gambar 2')
    gambar3_bangunan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Gambar 3')
    gambar4_bangunan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Gambar 4')

    # ===== SUMBER DAYA ALAM (Natural Resources) Fields =====
    jenis_sumber_daya_alam = models.CharField(max_length=100, null=True, blank=True, verbose_name='Jenis Sumber Daya Alam')
    produktivitas_per_tahun = models.CharField(max_length=100, null=True, blank=True, verbose_name='Produktivitas per Tahun')
    luas_sda = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Luas SDA (m2)')

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
        ('Negosiasi Tahap 1', 'Negosiasi Tahap 1'),
        ('Negosiasi Tahap 2', 'Negosiasi Tahap 2'),
        ('Negosiasi Tahap 3', 'Negosiasi Tahap 3'),
        ('Putusan Clear', 'Putusan Clear'),
        ('Putusan Pengadilan', 'Putusan Pengadilan'),
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
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Negosiasi Tahap 1')
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
        return f"{self.stakeholder.nama} - {self.object_type} ({self.role})""""
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
