"""
Django management command to import census data from CSV to database.

Usage:
    python manage.py import_census_csv <csv_file_path> [--dry-run] [--batch-size=100]

Example:
    python manage.py import_census_csv "/path/to/kepala_keluarga_isii (1).csv"
    python manage.py import_census_csv "/path/to/kepala_keluarga_isii (1).csv" --dry-run
"""

import csv
from decimal import Decimal, InvalidOperation
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from valemis.models_census_larap import CensusKepalaKeluarga


class Command(BaseCommand):
    help = 'Import census data from CSV file to census_kepala_keluarga table'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Path to the CSV file to import'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Validate data without saving to database'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='Number of records to process in each batch (default: 100)'
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        dry_run = options['dry_run']
        batch_size = options['batch_size']

        self.stdout.write(self.style.SUCCESS(f'\n{"="*60}'))
        self.stdout.write(self.style.SUCCESS('Census Data Import Script'))
        self.stdout.write(self.style.SUCCESS(f'{"="*60}\n'))
        self.stdout.write(f'CSV File: {csv_file}')
        self.stdout.write(f'Dry Run: {dry_run}')
        self.stdout.write(f'Batch Size: {batch_size}\n')

        # Statistics
        stats = {
            'total': 0,
            'success': 0,
            'skipped': 0,
            'errors': []
        }

        try:
            with open(csv_file, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                
                # Verify CSV has expected columns
                if not reader.fieldnames:
                    raise CommandError('CSV file is empty or invalid')
                
                self.stdout.write(f'Found {len(reader.fieldnames)} columns in CSV\n')
                self.stdout.write('Starting import...\n')

                batch = []
                
                for row_num, row in enumerate(reader, start=2):  # start=2 because row 1 is header
                    stats['total'] += 1
                    
                    try:
                        # Map CSV row to model fields
                        census_data = self.map_csv_to_model(row)
                        
                        if dry_run:
                            # Validate only
                            census = CensusKepalaKeluarga(**census_data)
                            census.full_clean()  # Validate without saving
                            stats['success'] += 1
                            if stats['total'] % 10 == 0:
                                self.stdout.write(f'Validated {stats["total"]} rows...')
                        else:
                            batch.append(census_data)
                            
                            # Process batch
                            if len(batch) >= batch_size:
                                self.save_batch(batch, stats)
                                batch = []
                                self.stdout.write(f'Processed {stats["success"]} rows...')
                    
                    except Exception as e:
                        stats['skipped'] += 1
                        error_msg = f'Row {row_num}: {str(e)}'
                        stats['errors'].append(error_msg)
                        self.stdout.write(self.style.WARNING(f'⚠ Skipped {error_msg}'))
                
                # Save remaining batch
                if batch and not dry_run:
                    self.save_batch(batch, stats)

        except FileNotFoundError:
            raise CommandError(f'CSV file not found: {csv_file}')
        except Exception as e:
            raise CommandError(f'Error reading CSV file: {str(e)}')

        # Print summary
        self.print_summary(stats, dry_run)

    def map_csv_to_model(self, row):
        """Map CSV row to CensusKepalaKeluarga model fields"""
        
        return {
            # A. Identifikasi Rumah Tangga dan PAP
            'id_project': self.clean_string(row.get('id_project')),
            'kode_enumerator': self.clean_string(row.get('kode_enumerator')),
            'id_rumah_tangga': self.clean_string(row.get('id_rumah_tangga')),
            'tanggal': self.parse_date(row.get('tanggal')),
            'kode_foto_survei': self.clean_string(row.get('kode_foto_survei')),
            'entitas_terdampak': self.clean_string(row.get('entitas_terdampak')),
            'koordinat': self.clean_string(row.get('koordinat')),
            
            # B. Informasi Kepala Keluarga
            'nama_depan': self.clean_string(row.get('nama_depan')),
            'nama_tengah': self.clean_string(row.get('nama_tengah')),
            'nama_belakang': self.clean_string(row.get('nama_belakang')),
            'nama_ayah': self.clean_string(row.get('nama_ayah')),
            'nama_kakek': self.clean_string(row.get('nama_kakek')),
            'nama_pasangan': self.clean_string(row.get('nama_pasangan')),
            'nomor_telepon': self.clean_string(row.get('nomor_telepon')),
            'nik': self.clean_string(row.get('nik')),
            'desa': self.clean_string(row.get('desa')),
            'kecamatan': self.clean_string(row.get('kecamatan')),
            'kabupaten': self.clean_string(row.get('kabupaten')),
            'provinsi': self.clean_string(row.get('provinsi')),
            'nama_responden': self.clean_string(row.get('nama_responden')),
            'hubungan_responden': self.clean_string(row.get('hubungan_responden')),
            
            # C. Profil Dampak
            'identifikasi_dampak': self.clean_string(row.get('identifikasi_dampak')),
            'identifikasi_dampak_lainnya': self.clean_string(row.get('identifikasi_dampak_lainnya')),
            
            # D. Profil Sosial Rumah Tangga
            'agama': self.clean_string(row.get('agama')),
            'agama_lainnya': self.clean_string(row.get('agama_lainnya')),
            'asal_etnis': self.clean_string(row.get('asal_etnis')),
            'asal_etnis_lainnya': self.clean_string(row.get('asal_etnis_lainnya')),
            'bahasa': self.clean_string(row.get('bahasa')),
            'bahasa_lainnya': self.clean_string(row.get('bahasa_lainnya')),
            'tempat_asal_kk': self.clean_string(row.get('tempat_asal_kk')),
            'tempat_asal_kk_tentukan': self.clean_string(row.get('tempat_asal_kk_tentukan')),
            'jumlah_orang_rumah_tangga': self.parse_int(row.get('jumlah_orang_rumah_tangga')),
            
            # E. Demografi Rumah Tangga
            'jenis_kelamin': self.clean_string(row.get('jenis_kelamin')),
            'tanggal_lahir': self.parse_date(row.get('tanggal_lahir')),
            'usia': self.parse_int(row.get('usia')),
            'status_perkawinan': self.clean_string(row.get('status_perkawinan')),
            'bisa_membaca_menulis': self.clean_string(row.get('bisa_membaca_menulis')),
            'sedang_sekolah': self.clean_string(row.get('sedang_sekolah')),
            'sekolah_dimana': self.clean_string(row.get('sekolah_dimana')),
            'pendidikan_terakhir': self.clean_string(row.get('pendidikan_terakhir')),
            'alasan_penghentian': self.clean_string(row.get('alasan_penghentian')),
            'alasan_penghentian_lainnya': self.clean_string(row.get('alasan_penghentian_lainnya')),
            'disabilitas': self.clean_string(row.get('disabilitas')),
            'disabilitas_lainnya': self.clean_string(row.get('disabilitas_lainnya')),
            'kondisi_kesehatan_kronis': self.clean_string(row.get('kondisi_kesehatan_kronis')),
            'kondisi_kesehatan_kronis_lainnya': self.clean_string(row.get('kondisi_kesehatan_kronis_lainnya')),
            
            # F. Pekerjaan, Keterampilan, dan Tanah
            'bekerja_12_bulan': self.clean_string(row.get('bekerja_12_bulan')),
            'pekerjaan_utama': self.clean_string(row.get('pekerjaan_utama')),
            'pekerjaan_utama_lainnya': self.clean_string(row.get('pekerjaan_utama_lainnya')),
            'jenis_pekerjaan_utama': self.clean_string(row.get('jenis_pekerjaan_utama')),
            'lokasi_pekerjaan_utama': self.clean_string(row.get('lokasi_pekerjaan_utama')),
            'lokasi_pekerjaan_utama_lainnya': self.clean_string(row.get('lokasi_pekerjaan_utama_lainnya')),
            'jumlah_bulan_bekerja': self.parse_int(row.get('jumlah_bulan_bekerja')),
            'penghasilan_per_bulan': self.parse_decimal(row.get('penghasilan_per_bulan')),
            'pekerjaan_sekunder': self.clean_string(row.get('pekerjaan_sekunder')),
            'pekerjaan_sekunder_lainnya': self.clean_string(row.get('pekerjaan_sekunder_lainnya')),
            'lokasi_pekerjaan_sekunder': self.clean_string(row.get('lokasi_pekerjaan_sekunder')),
            'lokasi_pekerjaan_sekunder_lainnya': self.clean_string(row.get('lokasi_pekerjaan_sekunder_lainnya')),
            'jumlah_bulan_bekerja_sekunder': self.parse_int(row.get('jumlah_bulan_bekerja_sekunder')),
            'penghasilan_sekunder_per_bulan': self.parse_decimal(row.get('penghasilan_sekunder_per_bulan')),
            'keterampilan': self.clean_string(row.get('keterampilan')),
            'keterampilan_lainnya': self.clean_string(row.get('keterampilan_lainnya')),
            
            # G. Kesehatan
            'penyakit_umum_anak': self.clean_string(row.get('penyakit_umum_anak')),
            'penyakit_umum_remaja': self.clean_string(row.get('penyakit_umum_remaja')),
            'penyakit_umum_dewasa': self.clean_string(row.get('penyakit_umum_dewasa')),
            'penyakit_umum_lansia': self.clean_string(row.get('penyakit_umum_lansia')),
            'tempat_pelayanan_kesehatan': self.clean_string(row.get('tempat_pelayanan_kesehatan')),
            'tempat_pelayanan_kesehatan_lainnya': self.clean_string(row.get('tempat_pelayanan_kesehatan_lainnya')),
            
            # H. Kecukupan Pangan
            'kecukupan_pangan': self.clean_string(row.get('kecukupan_pangan')),
            'defisit_pangan_cara_menutupi': self.clean_string(row.get('defisit_pangan_cara_menutupi')),
            'defisit_pangan_lainnya': self.clean_string(row.get('defisit_pangan_lainnya')),
            
            # I. Pendapatan, Pengeluaran dan Utang
            'pendapatan_1_pertanian': self.clean_string(row.get('pendapatan_1_pertanian')),
            'pendapatan_1_sumber': self.clean_string(row.get('pendapatan_1_sumber')),
            'pendapatan_1_sumber_lainnya': self.clean_string(row.get('pendapatan_1_sumber_lainnya')),
            'pendapatan_1_primer_sekunder': self.clean_string(row.get('pendapatan_1_primer_sekunder')),
            'pendapatan_1_jumlah': self.parse_decimal(row.get('pendapatan_1_jumlah')),
            'pendapatan_2_pertanian': self.clean_string(row.get('pendapatan_2_pertanian')),
            'pendapatan_2_sumber': self.clean_string(row.get('pendapatan_2_sumber')),
            'pendapatan_2_sumber_lainnya': self.clean_string(row.get('pendapatan_2_sumber_lainnya')),
            'pendapatan_2_primer_sekunder': self.clean_string(row.get('pendapatan_2_primer_sekunder')),
            'pendapatan_2_jumlah': self.parse_decimal(row.get('pendapatan_2_jumlah')),
            'pendapatan_3_pertanian': self.clean_string(row.get('pendapatan_3_pertanian')),
            'pendapatan_3_sumber': self.clean_string(row.get('pendapatan_3_sumber')),
            'pendapatan_3_sumber_lainnya': self.clean_string(row.get('pendapatan_3_sumber_lainnya')),
            'pendapatan_3_primer_sekunder': self.clean_string(row.get('pendapatan_3_primer_sekunder')),
            'pendapatan_3_jumlah': self.parse_decimal(row.get('pendapatan_3_jumlah')),
            'penghasilan_tahunan_total': self.parse_decimal(row.get('penghasilan_tahunan_total')),
            'pengeluaran_1_item': self.clean_string(row.get('pengeluaran_1_item')),
            'pengeluaran_1_item_lainnya': self.clean_string(row.get('pengeluaran_1_item_lainnya')),
            'pengeluaran_1_frekuensi': self.parse_int(row.get('pengeluaran_1_frekuensi')),
            'pengeluaran_1_jumlah': self.parse_decimal(row.get('pengeluaran_1_jumlah')),
            'pengeluaran_2_item': self.clean_string(row.get('pengeluaran_2_item')),
            'pengeluaran_2_item_lainnya': self.clean_string(row.get('pengeluaran_2_item_lainnya')),
            'pengeluaran_2_frekuensi': self.parse_int(row.get('pengeluaran_2_frekuensi')),
            'pengeluaran_2_jumlah': self.parse_decimal(row.get('pengeluaran_2_jumlah')),
            'pengeluaran_3_item': self.clean_string(row.get('pengeluaran_3_item')),
            'pengeluaran_3_item_lainnya': self.clean_string(row.get('pengeluaran_3_item_lainnya')),
            'pengeluaran_3_frekuensi': self.parse_int(row.get('pengeluaran_3_frekuensi')),
            'pengeluaran_3_jumlah': self.parse_decimal(row.get('pengeluaran_3_jumlah')),
            'pengeluaran_bulanan_total': self.parse_decimal(row.get('pengeluaran_bulanan_total')),
            'rekening_bank': self.clean_string(row.get('rekening_bank')),
            'punya_tabungan': self.clean_string(row.get('punya_tabungan')),
            'punya_hutang': self.clean_string(row.get('punya_hutang')),
            'jenis_tabungan': self.clean_string(row.get('jenis_tabungan')),
            'jenis_tabungan_lainnya': self.clean_string(row.get('jenis_tabungan_lainnya')),
            'jenis_hutang': self.clean_string(row.get('jenis_hutang')),
            'jenis_hutang_lainnya': self.clean_string(row.get('jenis_hutang_lainnya')),
            'alasan_hutang': self.clean_string(row.get('alasan_hutang')),
            'alasan_hutang_lainnya': self.clean_string(row.get('alasan_hutang_lainnya')),
            
            # J. Dampak Pembebasan Lahan
            'pernah_terdampak_proyek': self.clean_string(row.get('pernah_terdampak_proyek')),
            'jenis_proyek_sebelumnya': self.clean_string(row.get('jenis_proyek_sebelumnya')),
            'jenis_proyek_lainnya': self.clean_string(row.get('jenis_proyek_lainnya')),
            'luas_lahan_dibebaskan': self.parse_decimal(row.get('luas_lahan_dibebaskan')),
            'pernah_pengungsi': self.clean_string(row.get('pernah_pengungsi')),
            
            # K. Usaha Komersial atau Bisnis
            'punya_bisnis': self.clean_string(row.get('punya_bisnis')),
            'lokasi_bisnis': self.clean_string(row.get('lokasi_bisnis')),
            'lokasi_bisnis_lainnya': self.clean_string(row.get('lokasi_bisnis_lainnya')),
            'kepemilikan_bisnis': self.clean_string(row.get('kepemilikan_bisnis')),
            'kepemilikan_bisnis_lainnya': self.clean_string(row.get('kepemilikan_bisnis_lainnya')),
            'sejak_kapan_bisnis': self.clean_string(row.get('sejak_kapan_bisnis')),
            'jenis_bisnis': self.clean_string(row.get('jenis_bisnis')),
            'jenis_bisnis_lainnya': self.clean_string(row.get('jenis_bisnis_lainnya')),
            'jumlah_pegawai': self.parse_int(row.get('jumlah_pegawai')),
            'pendapatan_bisnis_per_bulan': self.parse_decimal(row.get('pendapatan_bisnis_per_bulan')),
            'deskripsi_produk_layanan': self.clean_string(row.get('deskripsi_produk_layanan')),
            
            # L. Struktur Tempat Tinggal
            'tipe_rumah': self.clean_string(row.get('tipe_rumah')),
            'tipe_rumah_lainnya': self.clean_string(row.get('tipe_rumah_lainnya')),
            'luas_rumah': self.parse_decimal(row.get('luas_rumah')),
            'pelayanan_listrik': self.clean_string(row.get('pelayanan_listrik')),
            'pelayanan_listrik_lainnya': self.clean_string(row.get('pelayanan_listrik_lainnya')),
            'sumber_air': self.clean_string(row.get('sumber_air')),
            'sumber_air_lainnya': self.clean_string(row.get('sumber_air_lainnya')),
            'sanitasi': self.clean_string(row.get('sanitasi')),
            
            # M. Kerentanan
            'karakteristik_kerentanan': self.clean_string(row.get('karakteristik_kerentanan')),
            
            # N. Komunikasi dan Informasi
            'sumber_informasi': self.clean_string(row.get('sumber_informasi')),
            'metode_komunikasi': self.clean_string(row.get('metode_komunikasi')),
            
            # O. Tanah
            'nib': self.clean_string(row.get('nib')),
            'letak_tanah': self.clean_string(row.get('letak_tanah')),
            'status_tanah': self.clean_string(row.get('status_tanah')),
            'surat_bukti_tanah': self.clean_string(row.get('surat_bukti_tanah')),
            'luas_tanah': self.parse_decimal(row.get('luas_tanah')),
            'tahun_kelola_lahan': self.parse_int(row.get('tahun_kelola_lahan')),
            'asal_usul_perolehan': self.clean_string(row.get('asal_usul_perolehan')),
            'biaya_perolehan': self.parse_decimal(row.get('biaya_perolehan')),
            'batas_utara': self.clean_string(row.get('batas_utara')),
            'batas_selatan': self.clean_string(row.get('batas_selatan')),
            'batas_timur': self.clean_string(row.get('batas_timur')),
            'batas_barat': self.clean_string(row.get('batas_barat')),
            
            # P. Ruang Atas dan Bawah
            'hm_sarusun': self.clean_string(row.get('hm_sarusun')),
            'luas_ruang': self.parse_decimal(row.get('luas_ruang')),
            
            # Q. Tanaman (all default to 0 if empty)
            'tanaman_merica': self.parse_int(row.get('tanaman_merica'), default=0),
            'tanaman_alpukat': self.parse_int(row.get('tanaman_alpukat'), default=0),
            'tanaman_aren': self.parse_int(row.get('tanaman_aren'), default=0),
            'tanaman_belimbing': self.parse_int(row.get('tanaman_belimbing'), default=0),
            'tanaman_belukar': self.parse_int(row.get('tanaman_belukar'), default=0),
            'tanaman_bonglai': self.parse_int(row.get('tanaman_bonglai'), default=0),
            'tanaman_buah_naga': self.parse_int(row.get('tanaman_buah_naga'), default=0),
            'tanaman_cabai': self.parse_int(row.get('tanaman_cabai'), default=0),
            'tanaman_cempedak': self.parse_int(row.get('tanaman_cempedak'), default=0),
            'tanaman_cengkeh': self.parse_int(row.get('tanaman_cengkeh'), default=0),
            'tanaman_cokelat': self.parse_int(row.get('tanaman_cokelat'), default=0),
            'tanaman_durian': self.parse_int(row.get('tanaman_durian'), default=0),
            'tanaman_jahe_merah': self.parse_int(row.get('tanaman_jahe_merah'), default=0),
            'tanaman_jambu': self.parse_int(row.get('tanaman_jambu'), default=0),
            'tanaman_jambu_air': self.parse_int(row.get('tanaman_jambu_air'), default=0),
            'tanaman_jambu_batu': self.parse_int(row.get('tanaman_jambu_batu'), default=0),
            'tanaman_jambu_biji': self.parse_int(row.get('tanaman_jambu_biji'), default=0),
            'tanaman_jati_putih': self.parse_int(row.get('tanaman_jati_putih'), default=0),
            'tanaman_jengkol': self.parse_int(row.get('tanaman_jengkol'), default=0),
            'tanaman_jeruk': self.parse_int(row.get('tanaman_jeruk'), default=0),
            'tanaman_jeruk_nipis': self.parse_int(row.get('tanaman_jeruk_nipis'), default=0),
            'tanaman_kapuk': self.parse_int(row.get('tanaman_kapuk'), default=0),
            'tanaman_kecombrang': self.parse_int(row.get('tanaman_kecombrang'), default=0),
            'tanaman_kelapa': self.parse_int(row.get('tanaman_kelapa'), default=0),
            'tanaman_kelapa_sawit': self.parse_int(row.get('tanaman_kelapa_sawit'), default=0),
            'tanaman_kelor': self.parse_int(row.get('tanaman_kelor'), default=0),
            'tanaman_kopi': self.parse_int(row.get('tanaman_kopi'), default=0),
            'tanaman_kunyit': self.parse_int(row.get('tanaman_kunyit'), default=0),
            'tanaman_kunyit_hitam': self.parse_int(row.get('tanaman_kunyit_hitam'), default=0),
            'tanaman_langsat': self.parse_int(row.get('tanaman_langsat'), default=0),
            'tanaman_lengkuas': self.parse_int(row.get('tanaman_lengkuas'), default=0),
            'tanaman_mangga': self.parse_int(row.get('tanaman_mangga'), default=0),
            'tanaman_nanas': self.parse_int(row.get('tanaman_nanas'), default=0),
            'tanaman_nangka': self.parse_int(row.get('tanaman_nangka'), default=0),
            'tanaman_nilam': self.parse_int(row.get('tanaman_nilam'), default=0),
            'tanaman_pepaya': self.parse_int(row.get('tanaman_pepaya'), default=0),
            'tanaman_pinang': self.parse_int(row.get('tanaman_pinang'), default=0),
            'tanaman_rambutan': self.parse_int(row.get('tanaman_rambutan'), default=0),
            'tanaman_serai': self.parse_int(row.get('tanaman_serai'), default=0),
            'tanaman_singkong': self.parse_int(row.get('tanaman_singkong'), default=0),
            'tanaman_sirsak': self.parse_int(row.get('tanaman_sirsak'), default=0),
            'tanaman_sukun': self.parse_int(row.get('tanaman_sukun'), default=0),
            'tanaman_talas': self.parse_int(row.get('tanaman_talas'), default=0),
            'tanaman_ubi': self.parse_int(row.get('tanaman_ubi'), default=0),
            
            # R. Lainnya
            'benda_lain_tanah': self.clean_string(row.get('benda_lain_tanah')),
            'pembebanan_hak_tanah': self.clean_string(row.get('pembebanan_hak_tanah')),
            'perkiraan_dampak': self.clean_string(row.get('perkiraan_dampak')),
            'keterangan': self.clean_string(row.get('keterangan')),
            'fungsi_kawasan': self.clean_string(row.get('fungsi_kawasan')),
        }

    def save_batch(self, batch, stats):
        """Save a batch of records to database"""
        try:
            with transaction.atomic():
                for data in batch:
                    census = CensusKepalaKeluarga(**data)
                    census.save()
                    stats['success'] += 1
        except Exception as e:
            # If batch fails, try saving one by one
            for data in batch:
                try:
                    census = CensusKepalaKeluarga(**data)
                    census.save()
                    stats['success'] += 1
                except Exception as e:
                    stats['skipped'] += 1
                    stats['errors'].append(f'Failed to save record: {str(e)}')

    def clean_string(self, value):
        """Clean and return string value or None"""
        if value is None or value == '':
            return None
        return str(value).strip()

    def parse_int(self, value, default=None):
        """Parse integer value"""
        if value is None or value == '':
            return default
        try:
            return int(float(value))  # Handle decimal strings like "4.0"
        except (ValueError, TypeError):
            return default

    def parse_decimal(self, value):
        """Parse decimal value"""
        if value is None or value == '':
            return None
        try:
            return Decimal(str(value))
        except (InvalidOperation, ValueError):
            return None

    def parse_date(self, value):
        """Parse date value in various formats"""
        if value is None or value == '':
            return None
        
        # Try different date formats
        date_formats = [
            '%m/%d/%Y',  # 8/1/2025
            '%Y-%m-%d',  # 2025-08-01
            '%d/%m/%Y',  # 01/08/2025
            '%d-%m-%Y',  # 01-08-2025
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(str(value).strip(), fmt).date()
            except ValueError:
                continue
        
        return None

    def print_summary(self, stats, dry_run):
        """Print import summary"""
        self.stdout.write(f'\n{"="*60}')
        self.stdout.write(self.style.SUCCESS('Import Summary'))
        self.stdout.write(f'{"="*60}\n')
        
        mode = 'DRY RUN (Validation Only)' if dry_run else 'ACTUAL IMPORT'
        self.stdout.write(f'Mode: {mode}')
        self.stdout.write(f'Total rows processed: {stats["total"]}')
        self.stdout.write(self.style.SUCCESS(f'✓ Successfully imported: {stats["success"]}'))
        
        if stats['skipped'] > 0:
            self.stdout.write(self.style.WARNING(f'⚠ Skipped: {stats["skipped"]}'))
            
            if stats['errors']:
                self.stdout.write('\nErrors:')
                for error in stats['errors'][:10]:  # Show first 10 errors
                    self.stdout.write(self.style.ERROR(f'  - {error}'))
                
                if len(stats['errors']) > 10:
                    self.stdout.write(f'  ... and {len(stats["errors"]) - 10} more errors')
        
        self.stdout.write(f'\n{"="*60}\n')
        
        if not dry_run and stats['success'] > 0:
            self.stdout.write(self.style.SUCCESS(f'✓ Import completed successfully!'))
            self.stdout.write(f'Check database table: census_kepala_keluarga\n')
