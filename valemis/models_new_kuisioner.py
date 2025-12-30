"""
ASSET INVENTORY - KUESIONER MODEL
105 Fields from Kuisioner Sheet - Census Survey Structure
"""

from django.db import models

class AssetInventory(models.Model):
    """
    Asset Inventory / Census Survey - Complete Kuisioner Structure
    105 fields matching the Excel Kuisioner sheet exactly
    """

    # ===== A. IDENTIFIKASI RUMAH TANGGA DAN PAP =====
    # Col 1: 1. Kode Enumerator
    kode_enumerator = models.CharField(max_length=50, null=True, blank=True, verbose_name='1. Kode Enumerator')

    # Col 2: 2. ID Rumah Tangga
    id_rumah_tangga = models.CharField(max_length=50, null=True, blank=True, verbose_name='2. ID Rumah Tangga')

    # Col 3: 3. Tanggal (DD/MM/YYYY)
    tanggal = models.DateField(null=True, blank=True, verbose_name='3. Tanggal')

    # Col 4: 4. Kode Foto Survei
    kode_foto_survei = models.CharField(max_length=50, null=True, blank=True, verbose_name='4. Kode Foto Survei')

    # Col 5: 5. ID Unik (ID Entitas Terdampak) Dalam Rumah Tangga
    id_unik = models.CharField(max_length=100, null=True, blank=True, verbose_name='5. ID Unik (ID Entitas Terdampak)')

    # Col 6: 6. Koordinat
    koordinat = models.CharField(max_length=100, null=True, blank=True, verbose_name='6. Koordinat')

    # ===== B. INFORMASI KEPALA KELUARGA =====
    # Col 7: 7. Nama Depan
    nama_depan = models.CharField(max_length=100, null=True, blank=True, verbose_name='7. Nama Depan')

    # Col 8: 8. Nama Tengah
    nama_tengah = models.CharField(max_length=100, null=True, blank=True, verbose_name='8. Nama Tengah')

    # Col 9: 9. Nama Belakang
    nama_belakang = models.CharField(max_length=100, null=True, blank=True, verbose_name='9. Nama Belakang')

    # Col 10: 10. Nama Ayah
    nama_ayah = models.CharField(max_length=100, null=True, blank=True, verbose_name='10. Nama Ayah')

    # Col 11: 11. Nama Kakek
    nama_kakek = models.CharField(max_length=100, null=True, blank=True, verbose_name='11. Nama Kakek')

    # Col 12: 12. Nama Pasangan
    nama_pasangan = models.CharField(max_length=100, null=True, blank=True, verbose_name='12. Nama Pasangan')

    # Col 13: 13. Nomor Telepon
    nomor_telepon = models.CharField(max_length=20, null=True, blank=True, verbose_name='13. Nomor Telepon')

    # Col 14: 14. NIK
    nik = models.CharField(max_length=20, null=True, blank=True, verbose_name='14. NIK')

    # Col 15: 15. Desa
    desa = models.CharField(max_length=100, null=True, blank=True, verbose_name='15. Desa')

    # Col 16: 16. Kecamatan
    kecamatan = models.CharField(max_length=100, null=True, blank=True, verbose_name='16. Kecamatan')

    # Col 17: 17. Kabupaten
    kabupaten = models.CharField(max_length=100, null=True, blank=True, verbose_name='17. Kabupaten')

    # Col 18: 18. Provinsi
    provinsi = models.CharField(max_length=100, null=True, blank=True, verbose_name='18. Provinsi')

    # Col 19: 19. Nama Responden jika Berbeda dengan Kepala Keluarga (KK)
    nama_responden = models.CharField(max_length=255, null=True, blank=True, verbose_name='19. Nama Responden')

    # Col 20: 20. Hubungan responden dengan kepala keluarga
    hubungan_responden_kk = models.CharField(max_length=100, null=True, blank=True,
                                             verbose_name='20. Hubungan Responden dengan KK')

    # Col 23: 22. Agama
    agama = models.CharField(max_length=50, null=True, blank=True, verbose_name='22. Agama')

    # Col 24: Lainnya (Agama)
    agama_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Agama Lainnya')

    # Col 25: 23. Asal etnis
    asal_etnis = models.CharField(max_length=100, null=True, blank=True, verbose_name='23. Asal Etnis')

    # Col 26: Lainnya (Asal etnis)
    asal_etnis_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Asal Etnis Lainnya')

    # Col 27: 24. Bahasa
    bahasa = models.CharField(max_length=100, null=True, blank=True, verbose_name='24. Bahasa')

    # Col 28: Lainnya (Bahasa)
    bahasa_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Bahasa Lainnya')

    # Col 29: 25. Tempat Asal Kepala Rumah Tangga
    tempat_asal_kk = models.CharField(max_length=100, null=True, blank=True,
                                     verbose_name='25. Tempat Asal Kepala Rumah Tangga')

    # Col 30: Tentukan (Tempat Asal)
    tempat_asal_tentukan = models.CharField(max_length=100, null=True, blank=True, verbose_name='Tentukan Tempat Asal')

    # Col 31: 26. Berapa banyak orang yang tinggal di rumah tangga
    jumlah_orang_rumah_tangga = models.IntegerField(null=True, blank=True,
                                                     verbose_name='26. Jumlah Orang di Rumah Tangga')

    # Col 32: No. (untuk anggota rumah tangga)
    no_anggota = models.IntegerField(null=True, blank=True, verbose_name='No.')

    # Col 33: 27. ID Dampak
    id_dampak = models.CharField(max_length=50, null=True, blank=True, verbose_name='27. ID Dampak')

    # Col 34: 28. Nama Depan (anggota)
    anggota_nama_depan = models.CharField(max_length=100, null=True, blank=True, verbose_name='28. Nama Depan')

    # Col 35: 29. Nama Belakang (anggota)
    anggota_nama_belakang = models.CharField(max_length=100, null=True, blank=True, verbose_name='29. Nama Belakang')

    # Col 36: 30. Hubungan dengan Kepala Keluarga
    hubungan_kk = models.CharField(max_length=100, null=True, blank=True, verbose_name='30. Hubungan dengan KK')

    # Col 37: 31. Jenis kelamin
    jenis_kelamin = models.CharField(max_length=20, null=True, blank=True, verbose_name='31. Jenis Kelamin')

    # Col 38: 32. Usia
    usia = models.IntegerField(null=True, blank=True, verbose_name='32. Usia')

    # Col 39: 33. Status Perkawinan
    status_perkawinan = models.CharField(max_length=50, null=True, blank=True, verbose_name='33. Status Perkawinan')

    # Col 40: 34. Bisa Membaca/Menulis atau Keduanya
    bisa_membaca_menulis = models.CharField(max_length=20, null=True, blank=True, verbose_name='34. Bisa Membaca/Menulis')

    # Col 41: 35. Sedang Sekolah
    sedang_sekolah = models.CharField(max_length=10, null=True, blank=True, verbose_name='35. Sedang Sekolah')

    # Col 42: 36. Jika sedang sekolah, di mana
    lokasi_sekolah = models.CharField(max_length=50, null=True, blank=True, verbose_name='36. Lokasi Sekolah')

    # Col 43: 37. Tingkat Pendidikan Terakhir selesai
    pendidikan_terakhir = models.CharField(max_length=50, null=True, blank=True, verbose_name='37. Pendidikan Terakhir')

    # Col 44: 38. Alasan penghentian
    alasan_penghentian = models.CharField(max_length=100, null=True, blank=True, verbose_name='38. Alasan Penghentian')

    # Col 45: Lainnya (Alasan penghentian)
    alasan_penghentian_lainnya = models.CharField(max_length=100, null=True, blank=True,
                                                   verbose_name='Alasan Penghentian Lainnya')

    # Col 46: 39. Disabilitas
    disabilitas = models.CharField(max_length=100, null=True, blank=True, verbose_name='39. Disabilitas')

    # Col 47: Lainnya (Disabilitas)
    disabilitas_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Disabilitas Lainnya')

    # Col 48: 40. Kondisi Kesehatan Kronis
    kondisi_kesehatan_kronis = models.TextField(null=True, blank=True, verbose_name='40. Kondisi Kesehatan Kronis')

    # Col 49: Lainnya (Kesehatan)
    kesehatan_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Kesehatan Lainnya')

    # Col 50: 41. Apakah Anda bekerja dalam 12 bulan terakhir
    bekerja_12_bulan = models.CharField(max_length=50, null=True, blank=True, verbose_name='41. Bekerja 12 Bulan')

    # Col 51: 42. Pekerjaan Utama
    pekerjaan_utama = models.CharField(max_length=100, null=True, blank=True, verbose_name='42. Pekerjaan Utama')

    # Col 52: Lainnya (Pekerjaan Utama)
    pekerjaan_utama_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Pekerjaan Utama Lainnya')

    # Col 53: 43. Jenis pekerjaan untuk pekerjaan utama
    jenis_pekerjaan = models.CharField(max_length=100, null=True, blank=True, verbose_name='43. Jenis Pekerjaan')

    # Col 54: 44. Lokasi pekerjaan utama
    lokasi_pekerjaan = models.CharField(max_length=100, null=True, blank=True, verbose_name='44. Lokasi Pekerjaan')

    # Col 55: Lainnya (Lokasi pekerjaan)
    lokasi_pekerjaan_lainnya = models.CharField(max_length=100, null=True, blank=True,
                                                verbose_name='Lokasi Pekerjaan Lainnya')

    # Col 56: 45. Jumlah bulan bekerja dalam setahun
    jumlah_bulan_bekerja = models.IntegerField(null=True, blank=True, verbose_name='45. Jumlah Bulan Bekerja')

    # Col 57: 46. Rata-rata Penghasilan Kegiatan ini per bulan (LAK)
    penghasilan_per_bulan = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True,
                                                 verbose_name='46. Penghasilan per Bulan')

    # Col 58: 47. Pekerjaan Sekunder
    pekerjaan_sekunder = models.CharField(max_length=100, null=True, blank=True, verbose_name='47. Pekerjaan Sekunder')

    # Col 59: Lainnya (Pekerjaan Sekunder)
    pekerjaan_sekunder_lainnya = models.CharField(max_length=100, null=True, blank=True,
                                                  verbose_name='Pekerjaan Sekunder Lainnya')

    # Col 60: 48. Lokasi pekerjaan sekunder
    lokasi_pekerjaan_sekunder = models.CharField(max_length=100, null=True, blank=True,
                                                 verbose_name='48. Lokasi Pekerjaan Sekunder')

    # Col 61: Lainnya (Lokasi pekerjaan sekunder)
    lokasi_pekerjaan_sekunder_lainnya = models.CharField(max_length=100, null=True, blank=True,
                                                         verbose_name='Lokasi Sekunder Lainnya')

    # Col 62: 49. Jumlah bulan bekerja dalam setahun (sekunder)
    jumlah_bulan_bekerja_sekunder = models.IntegerField(null=True, blank=True,
                                                        verbose_name='49. Jumlah Bulan Bekerja Sekunder')

    # Col 63: 50. Perkiraan Penghasilan dari pekerjaan sekunder (LAK per bulan)
    penghasilan_sekunder_per_bulan = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True,
                                                          verbose_name='50. Penghasilan Sekunder per Bulan')

    # Col 64: 51. Keterampilan dan/atau profesi
    keterampilan = models.TextField(null=True, blank=True, verbose_name='51. Keterampilan/Profesi')

    # Col 65: Lainnya (Keterampilan)
    keterampilan_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Keterampilan Lainnya')

    # Col 66: 55. Apa DUA penyakit paling umum
    penyakit_umum = models.TextField(null=True, blank=True, verbose_name='55. Penyakit Umum')

    # Col 82: 56. Dari tempat berikut, yang Anda gunakan dengan LEBIH BANYAK FREKUENSI
    tempat_pelayanan = models.CharField(max_length=100, null=True, blank=True, verbose_name='56. Tempat Pelayanan')

    # Col 83: 57. Kecukupan pangan dari produksi pertanian sendiri
    kecukupan_pangan = models.CharField(max_length=50, null=True, blank=True, verbose_name='57. Kecukupan Pangan')

    # Col 84: 58. Jika rumah tangga Anda mengalami kekurangan pangan
    defisit_pangan = models.TextField(null=True, blank=True, verbose_name='58. Defisit Pangan')

    # Col 85: Lainnya (Defisit pangan)
    defisit_pangan_lainnya = models.CharField(max_length=200, null=True, blank=True, verbose_name='Defisit Pangan Lainnya')

    # Col 86: 59. Berapa banyak penghasilan yang diperoleh keluarga Anda tahun lalu
    penghasilan_tahunan = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True,
                                               verbose_name='59. Penghasilan Tahunan')

    # Col 102: 60. Berapa pengeluaran bulanan Anda
    pengeluaran_bulanan = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True,
                                               verbose_name='60. Pengeluaran Bulanan')

    # Col 115: 61. Apakah ada anggota rumah tangga yang mempunyai rekening bank
    rekening_bank = models.CharField(max_length=10, null=True, blank=True, verbose_name='61. Punya Rekening Bank')

    # Col 116: 62. Apakah rumah tangga anda mempunyai tabungan
    tabungan = models.CharField(max_length=100, null=True, blank=True, verbose_name='62. Punya Tabungan')

    # Col 117: 63. Apakah rumah tangga anda mempunyai hutang
    hutang = models.CharField(max_length=100, null=True, blank=True, verbose_name='63. Punya Hutang')

    # Col 118: 64. Apakah rumah tangga mempunyai tabungan (detail)
    tabungan_detail = models.CharField(max_length=100, null=True, blank=True, verbose_name='64. Tabungan Detail')

    # Col 119: Lainnya (Tabungan)
    tabungan_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Tabungan Lainnya')

    # Col 120: 65. Jika rumah tangga mempunyai hutang
    hutang_detail = models.CharField(max_length=100, null=True, blank=True, verbose_name='65. Hutang Detail')

    # Col 121: Lainnya (Hutang)
    hutang_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Hutang Lainnya')

    # Col 122: 66. Kalau berhutang tolong jelaskan alasannya
    alasan_hutang = models.TextField(null=True, blank=True, verbose_name='66. Alasan Hutang')

    # Col 123: Lainnya (Alasan hutang)
    alasan_hutang_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Alasan Hutang Lainnya')

    # Col 124: 67. Apakah Anda pernah terkena dampak proyek pembebasan lahan lainnya sebelumnya
    pernah_dampak_proyek = models.CharField(max_length=10, null=True, blank=True, verbose_name='67. Pernah Dampak Proyek')

    # Col 125: 68. Jika Ya, Jenis Proyek
    jenis_proyek = models.CharField(max_length=100, null=True, blank=True, verbose_name='68. Jenis Proyek')

    # Col 126: Lainnya (Jenis proyek)
    jenis_proyek_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Jenis Proyek Lainnya')

    # Col 127: 69. Jika ya, berapa luas lahan yang dibebaskan (m2)
    luas_lahan_dibebaskan = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                                verbose_name='69. Luas Lahan Dibebaskan (m2)')

    # Col 128: 70. Apakah Anda pernah menjadi pengungsi internal sebelumnya
    pernah_pengungsi = models.CharField(max_length=10, null=True, blank=True, verbose_name='70. Pernah Pengungsi')

    # Col 129: 71. Apakah Anda mempunyai bisnis
    punya_bisnis = models.CharField(max_length=10, null=True, blank=True, verbose_name='71. Punya Bisnis')

    # Col 130: 72. Lokasi usaha
    lokasi_bisnis = models.CharField(max_length=100, null=True, blank=True, verbose_name='72. Lokasi Bisnis')

    # Col 131: Lainnya (Lokasi usaha)
    lokasi_bisnis_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Lokasi Bisnis Lainnya')

    # Col 132: 73. Kepemilikan bisnis
    kepemilikan_bisnis = models.CharField(max_length=100, null=True, blank=True, verbose_name='73. Kepemilikan Bisnis')

    # Col 133: Lainnya (Kepemilikan bisnis)
    kepemilikan_bisnis_lainnya = models.CharField(max_length=100, null=True, blank=True,
                                                  verbose_name='Kepemilikan Bisnis Lainnya')

    # Col 134: 74. Sejak kapan usaha ini aktif
    sejak_kapan_bisnis = models.CharField(max_length=50, null=True, blank=True, verbose_name='74. Sejak Kapan Bisnis')

    # Col 135: 75. Jenis usaha
    jenis_bisnis = models.CharField(max_length=100, null=True, blank=True, verbose_name='75. Jenis Bisnis')

    # Col 136: Lainnya (Jenis usaha)
    jenis_bisnis_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Jenis Bisnis Lainnya')

    # Col 137: 76. Jumlah pegawai
    jumlah_pegawai = models.IntegerField(null=True, blank=True, verbose_name='76. Jumlah Pegawai')

    # Col 138: 77. Pendapatan rata-rata/bulan (LAK)
    pendapatan_rata_bisnis = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True,
                                                  verbose_name='77. Pendapatan Rata-rata Bisnis')

    # Col 139: 78. Deskripsi Produk dan Layanan
    deskripsi_produk_layanan = models.TextField(null=True, blank=True, verbose_name='78. Deskripsi Produk')

    # Col 140: 79. Tipe rumah
    tipe_rumah = models.CharField(max_length=100, null=True, blank=True, verbose_name='79. Tipe Rumah')

    # Col 141: Lainnya (Tipe rumah)
    tipe_rumah_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Tipe Rumah Lainnya')

    # Col 142: 80. Pelayanan Listrik
    pelayanan_listrik = models.CharField(max_length=100, null=True, blank=True, verbose_name='80. Pelayanan Listrik')

    # Col 143: Lainnya (Pelayanan listrik)
    pelayanan_listrik_lainnya = models.CharField(max_length=100, null=True, blank=True,
                                                verbose_name='Pelayanan Listrik Lainnya')

    # Col 144: 81. Sumber Air Konsumsi
    sumber_air = models.CharField(max_length=100, null=True, blank=True, verbose_name='81. Sumber Air')

    # Col 145: Lainnya (Sumber air)
    sumber_air_lainnya = models.CharField(max_length=100, null=True, blank=True, verbose_name='Sumber Air Lainnya')

    # Col 146: 82. Sanitasi
    sanitasi = models.CharField(max_length=100, null=True, blank=True, verbose_name='82. Sanitasi')

    # Col 147: 83. Apakah kepala rumah tangga mempunyai salah satu karakteristik berikut
    karakteristik_khusus = models.TextField(null=True, blank=True, verbose_name='83. Karakteristik Khusus')

    # Col 150: 88. Apa sumber informasi utama bagi rumah tangga Anda
    sumber_informasi = models.CharField(max_length=100, null=True, blank=True, verbose_name='88. Sumber Informasi')

    # Col 151: 89. Apa metode terbaik untuk berkomunikasi
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
