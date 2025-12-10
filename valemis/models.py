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