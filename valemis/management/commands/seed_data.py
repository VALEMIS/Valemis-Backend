"""
Management command to seed the database with mock data from frontend.
Run with: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from datetime import date, timedelta
from decimal import Decimal
from valemis.models_new import (
    AssetInventory,
    LandInventory,
    LandDocument,
    LandAcquisition,
    LandCompliance,
    Litigation,
    StakeholderNew,
)


class Command(BaseCommand):
    help = 'Seed database with mock data from frontend'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            AssetInventory.objects.all().delete()
            LandInventory.objects.all().delete()
            LandAcquisition.objects.all().delete()
            LandCompliance.objects.all().delete()
            Litigation.objects.all().delete()
            StakeholderNew.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared all data.'))

        self.seed_assets()
        self.seed_lands()
        self.seed_acquisitions()
        self.seed_compliances()
        self.seed_litigations()
        self.seed_stakeholders()

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

    def seed_assets(self):
        """Seed Asset Inventory from frontend mock data"""
        self.stdout.write('Seeding Asset Inventory...')
        
        assets_data = [
            {'code': 'AST-SRW-001', 'owner_name': 'Budi Santoso', 'village': 'Desa Sorowako', 'land_area': 500, 'building_area': 120, 'certificate_status': 'SHM', 'lat': -2.5595, 'lng': 121.3415},
            {'code': 'AST-SRW-002', 'owner_name': 'Ahmad Hidayat', 'village': 'Desa Sorowako', 'land_area': 450, 'building_area': 110, 'certificate_status': 'SHM', 'lat': -2.5605, 'lng': 121.3425},
            {'code': 'AST-SRW-003', 'owner_name': 'Siti Rahma', 'village': 'Desa Sorowako', 'land_area': 600, 'building_area': 150, 'certificate_status': 'SHGB', 'lat': -2.5615, 'lng': 121.3435},
            {'code': 'AST-SRW-004', 'owner_name': 'Joko Widodo', 'village': 'Desa Sorowako', 'land_area': 520, 'building_area': 130, 'certificate_status': 'SHM', 'lat': -2.5610, 'lng': 121.3410},
            {'code': 'AST-MGN-001', 'owner_name': 'Andi Suryanto', 'village': 'Desa Magani', 'land_area': 480, 'building_area': 115, 'certificate_status': 'SHM', 'lat': -2.5605, 'lng': 121.3465},
            {'code': 'AST-MGN-002', 'owner_name': 'Maria Ulfa', 'village': 'Desa Magani', 'land_area': 550, 'building_area': 140, 'certificate_status': 'SHGB', 'lat': -2.5615, 'lng': 121.3475},
            {'code': 'AST-MGN-003', 'owner_name': 'Hasan Basri', 'village': 'Desa Magani', 'land_area': 470, 'building_area': 125, 'certificate_status': 'SHM', 'lat': -2.5620, 'lng': 121.3485},
            {'code': 'AST-MGN-004', 'owner_name': 'Ratna Dewi', 'village': 'Desa Magani', 'land_area': 490, 'building_area': 120, 'certificate_status': 'SHM', 'lat': -2.5612, 'lng': 121.3460},
            {'code': 'AST-WWR-001', 'owner_name': 'Usman Harun', 'village': 'Desa Wewangriu', 'land_area': 530, 'building_area': 135, 'certificate_status': 'SHM', 'lat': -2.5685, 'lng': 121.3425},
            {'code': 'AST-WWR-002', 'owner_name': 'Fatimah Zahra', 'village': 'Desa Wewangriu', 'land_area': 510, 'building_area': 128, 'certificate_status': 'SHGB', 'lat': -2.5695, 'lng': 121.3435},
            {'code': 'AST-WWR-003', 'owner_name': 'Rahman Wiranto', 'village': 'Desa Wewangriu', 'land_area': 560, 'building_area': 145, 'certificate_status': 'SHM', 'lat': -2.5705, 'lng': 121.3445},
            {'code': 'AST-WWR-004', 'owner_name': 'Nurul Huda', 'village': 'Desa Wewangriu', 'land_area': 495, 'building_area': 122, 'certificate_status': 'SHM', 'lat': -2.5698, 'lng': 121.3420},
            {'code': 'AST-NKL-001', 'owner_name': 'Bambang Trianto', 'village': 'Desa Nikkel', 'land_area': 540, 'building_area': 138, 'certificate_status': 'SHM', 'lat': -2.5695, 'lng': 121.3485},
            {'code': 'AST-NKL-002', 'owner_name': 'Dewi Anggraini', 'village': 'Desa Nikkel', 'land_area': 520, 'building_area': 132, 'certificate_status': 'SHGB', 'lat': -2.5705, 'lng': 121.3495},
            {'code': 'AST-NKL-003', 'owner_name': 'Irfan Maulana', 'village': 'Desa Nikkel', 'land_area': 575, 'building_area': 148, 'certificate_status': 'SHM', 'lat': -2.5715, 'lng': 121.3505},
            {'code': 'AST-NKL-004', 'owner_name': 'Wulan Sari', 'village': 'Desa Nikkel', 'land_area': 505, 'building_area': 125, 'certificate_status': 'SHM', 'lat': -2.5708, 'lng': 121.3480},
        ]
        
        for data in assets_data:
            AssetInventory.objects.get_or_create(code=data['code'], defaults=data)
        
        self.stdout.write(f'  Created {len(assets_data)} assets')

    def seed_lands(self):
        """Seed Land Inventory from frontend mock data"""
        self.stdout.write('Seeding Land Inventory...')
        
        lands_data = [
            {'code': 'LND-VALE-001', 'location_name': 'Vale Central Mining Area', 'category': 'Vale Owned', 'area': 450.5, 'certificate': 'HGU', 'certificate_no': 'HGU-001/2015', 'lat': -2.5650, 'lng': 121.3450, 'acquisition_year': 2015, 'documents': ['HGU-001-2015.pdf', 'Peta-Kadaster.pdf']},
            {'code': 'LND-VALE-002', 'location_name': 'Vale North Sector', 'category': 'Vale Owned', 'area': 320.8, 'certificate': 'HGU', 'certificate_no': 'HGU-002/2016', 'lat': -2.5500, 'lng': 121.3500, 'acquisition_year': 2016, 'documents': ['HGU-002-2016.pdf', 'Site-Plan.pdf']},
            {'code': 'LND-VALE-003', 'location_name': 'Vale South Sector', 'category': 'Vale Owned', 'area': 285.3, 'certificate': 'HGU', 'certificate_no': 'HGU-003/2017', 'lat': -2.5800, 'lng': 121.3400, 'acquisition_year': 2017, 'documents': ['HGU-003-2017.pdf']},
            {'code': 'LND-ACQ-001', 'location_name': 'Sorowako Expansion Area', 'category': 'Acquired', 'area': 125.5, 'certificate': 'SHM', 'certificate_no': 'SHM-045/2020', 'lat': -2.5595, 'lng': 121.3415, 'acquisition_year': 2020, 'documents': ['SHM-045-2020.pdf', 'Akta-Jual-Beli.pdf', 'PPJB.pdf']},
            {'code': 'LND-ACQ-002', 'location_name': 'Magani Buffer Zone', 'category': 'Acquired', 'area': 98.7, 'certificate': 'SHM', 'certificate_no': 'SHM-046/2021', 'lat': -2.5605, 'lng': 121.3465, 'acquisition_year': 2021, 'documents': ['SHM-046-2021.pdf', 'Akta-Jual-Beli.pdf']},
            {'code': 'LND-ACQ-003', 'location_name': 'Wewangriu Access Road', 'category': 'Acquired', 'area': 45.2, 'certificate': 'SHGB', 'certificate_no': 'SHGB-012/2022', 'lat': -2.5685, 'lng': 121.3425, 'acquisition_year': 2022, 'documents': ['SHGB-012-2022.pdf', 'Perjanjian-Kompensasi.pdf']},
            {'code': 'LND-ACQ-004', 'location_name': 'Nikkel Infrastructure', 'category': 'Acquired', 'area': 67.8, 'certificate': 'SHM', 'certificate_no': 'SHM-047/2023', 'lat': -2.5695, 'lng': 121.3485, 'acquisition_year': 2023, 'documents': ['SHM-047-2023.pdf']},
            {'code': 'LND-IUPK-001', 'location_name': 'IUPK Block A', 'category': 'IUPK', 'area': 550.0, 'certificate': 'HGU', 'certificate_no': 'IUPK-A/2010', 'lat': -2.5400, 'lng': 121.3300, 'acquisition_year': 2010, 'documents': ['SK-IUPK-A-2010.pdf', 'Peta-Wilayah-Kerja.pdf']},
            {'code': 'LND-IUPK-002', 'location_name': 'IUPK Block B', 'category': 'IUPK', 'area': 475.5, 'certificate': 'HGU', 'certificate_no': 'IUPK-B/2011', 'lat': -2.5450, 'lng': 121.3600, 'acquisition_year': 2011, 'documents': ['SK-IUPK-B-2011.pdf']},
            {'code': 'LND-IUPK-003', 'location_name': 'IUPK Block C', 'category': 'IUPK', 'area': 390.2, 'certificate': 'HGU', 'certificate_no': 'IUPK-C/2012', 'lat': -2.5700, 'lng': 121.3300, 'acquisition_year': 2012, 'documents': ['SK-IUPK-C-2012.pdf', 'AMDAL.pdf']},
            {'code': 'LND-PPKH-001', 'location_name': 'PPKH Conservation Area 1', 'category': 'PPKH', 'area': 280.5, 'certificate': 'HGU', 'certificate_no': 'PPKH-001/2018', 'lat': -2.5350, 'lng': 121.3550, 'acquisition_year': 2018, 'documents': ['SK-PPKH-001-2018.pdf', 'RKL-RPL.pdf']},
            {'code': 'LND-PPKH-002', 'location_name': 'PPKH Conservation Area 2', 'category': 'PPKH', 'area': 315.8, 'certificate': 'HGU', 'certificate_no': 'PPKH-002/2019', 'lat': -2.5750, 'lng': 121.3550, 'acquisition_year': 2019, 'documents': ['SK-PPKH-002-2019.pdf']},
            {'code': 'LND-OPS-001', 'location_name': 'Operational Base Camp', 'category': 'Operational', 'area': 35.5, 'certificate': 'SHGB', 'certificate_no': 'SHGB-020/2020', 'lat': -2.5600, 'lng': 121.3450, 'acquisition_year': 2020, 'documents': ['SHGB-020-2020.pdf', 'IMB.pdf']},
            {'code': 'LND-OPS-002', 'location_name': 'Processing Plant Area', 'category': 'Operational', 'area': 120.3, 'certificate': 'HGU', 'certificate_no': 'HGU-008/2015', 'lat': -2.5620, 'lng': 121.3470, 'acquisition_year': 2015, 'documents': ['HGU-008-2015.pdf', 'Izin-Operasional.pdf', 'UKL-UPL.pdf']},
            {'code': 'LND-OPS-003', 'location_name': 'Storage & Logistics', 'category': 'Operational', 'area': 48.7, 'certificate': 'SHGB', 'certificate_no': 'SHGB-021/2021', 'lat': -2.5680, 'lng': 121.3480, 'acquisition_year': 2021, 'documents': ['SHGB-021-2021.pdf']},
        ]
        
        for data in lands_data:
            docs = data.pop('documents', [])
            land, created = LandInventory.objects.get_or_create(code=data['code'], defaults=data)
            if created:
                for doc_name in docs:
                    LandDocument.objects.create(land=land, file_name=doc_name)
        
        self.stdout.write(f'  Created {len(lands_data)} lands')

    def seed_acquisitions(self):
        """Seed Land Acquisition from frontend mock data"""
        self.stdout.write('Seeding Land Acquisition...')
        
        acquisitions_data = [
            # Project Alpha parcels
            {'code': 'PCL-ALP-001', 'project': 'Project Alpha - Mining Expansion', 'owner_name': 'Budi Santoso', 'village': 'Desa Sorowako', 'area': 500, 'status': 'Bebas', 'jumlah_bebas': 500, 'biaya_pembebasan': 450000000, 'negotiation_date': '2024-10-15'},
            {'code': 'PCL-ALP-002', 'project': 'Project Alpha - Mining Expansion', 'owner_name': 'Ahmad Hidayat', 'village': 'Desa Sorowako', 'area': 450, 'status': 'Bebas', 'jumlah_bebas': 450, 'biaya_pembebasan': 425000000, 'negotiation_date': '2024-10-18'},
            {'code': 'PCL-ALP-003', 'project': 'Project Alpha - Mining Expansion', 'owner_name': 'Siti Rahma', 'village': 'Desa Sorowako', 'area': 600, 'status': 'Dalam Negosiasi', 'jumlah_bebas': 0, 'biaya_pembebasan': 0, 'negotiation_date': '2024-11-20'},
            {'code': 'PCL-ALP-004', 'project': 'Project Alpha - Mining Expansion', 'owner_name': 'Andi Suryanto', 'village': 'Desa Magani', 'area': 480, 'status': 'Bebas', 'jumlah_bebas': 480, 'biaya_pembebasan': 435000000, 'negotiation_date': '2024-10-22'},
            {'code': 'PCL-ALP-005', 'project': 'Project Alpha - Mining Expansion', 'owner_name': 'Maria Ulfa', 'village': 'Desa Magani', 'area': 550, 'status': 'Dalam Negosiasi', 'jumlah_bebas': 0, 'biaya_pembebasan': 0, 'negotiation_date': '2024-11-25'},
            {'code': 'PCL-ALP-006', 'project': 'Project Alpha - Mining Expansion', 'owner_name': 'Hasan Basri', 'village': 'Desa Magani', 'area': 470, 'status': 'Belum Diproses', 'jumlah_bebas': 0, 'biaya_pembebasan': 0, 'negotiation_date': '-'},
            # Project Beta parcels
            {'code': 'PCL-BTA-001', 'project': 'Project Beta - Infrastructure Development', 'owner_name': 'Usman Harun', 'village': 'Desa Wewangriu', 'area': 530, 'status': 'Bebas', 'jumlah_bebas': 530, 'biaya_pembebasan': 485000000, 'negotiation_date': '2024-09-10'},
            {'code': 'PCL-BTA-002', 'project': 'Project Beta - Infrastructure Development', 'owner_name': 'Fatimah Zahra', 'village': 'Desa Wewangriu', 'area': 510, 'status': 'Dalam Negosiasi', 'jumlah_bebas': 0, 'biaya_pembebasan': 0, 'negotiation_date': '2024-11-15'},
            {'code': 'PCL-BTA-003', 'project': 'Project Beta - Infrastructure Development', 'owner_name': 'Rahman Wiranto', 'village': 'Desa Wewangriu', 'area': 560, 'status': 'Belum Diproses', 'jumlah_bebas': 0, 'biaya_pembebasan': 0, 'negotiation_date': '-'},
            {'code': 'PCL-BTA-004', 'project': 'Project Beta - Infrastructure Development', 'owner_name': 'Nurul Huda', 'village': 'Desa Wewangriu', 'area': 495, 'status': 'Dalam Negosiasi', 'jumlah_bebas': 0, 'biaya_pembebasan': 0, 'negotiation_date': '2024-11-28'},
            # Project Gamma parcels
            {'code': 'PCL-GMA-001', 'project': 'Project Gamma - Road Access', 'owner_name': 'Bambang Trianto', 'village': 'Desa Nikkel', 'area': 540, 'status': 'Bebas', 'jumlah_bebas': 540, 'biaya_pembebasan': 495000000, 'negotiation_date': '2024-08-20'},
            {'code': 'PCL-GMA-002', 'project': 'Project Gamma - Road Access', 'owner_name': 'Dewi Anggraini', 'village': 'Desa Nikkel', 'area': 520, 'status': 'Bebas', 'jumlah_bebas': 520, 'biaya_pembebasan': 475000000, 'negotiation_date': '2024-08-25'},
            {'code': 'PCL-GMA-003', 'project': 'Project Gamma - Road Access', 'owner_name': 'Irfan Maulana', 'village': 'Desa Nikkel', 'area': 575, 'status': 'Bebas', 'jumlah_bebas': 575, 'biaya_pembebasan': 525000000, 'negotiation_date': '2024-09-01'},
            {'code': 'PCL-GMA-004', 'project': 'Project Gamma - Road Access', 'owner_name': 'Wulan Sari', 'village': 'Desa Nikkel', 'area': 505, 'status': 'Dalam Negosiasi', 'jumlah_bebas': 0, 'biaya_pembebasan': 0, 'negotiation_date': '2024-11-30'},
        ]
        
        for data in acquisitions_data:
            LandAcquisition.objects.get_or_create(code=data['code'], defaults=data)
        
        self.stdout.write(f'  Created {len(acquisitions_data)} acquisitions')

    def seed_compliances(self):
        """Seed Land Compliance from frontend mock data"""
        self.stdout.write('Seeding Land Compliance...')
        
        # Calculate dates
        today = date.today()
        
        compliances_data = [
            {'land_code': 'LND-VALE-001', 'location_name': 'Vale Central Mining Area', 'permit_type': 'IUPK', 'permit_number': 'IUPK-001/2020', 'issue_date': date(2020, 1, 15), 'expiry_date': date(2030, 1, 15), 'status': 'Compliant', 'notes': ''},
            {'land_code': 'LND-VALE-001', 'location_name': 'Vale Central Mining Area', 'permit_type': 'AMDAL', 'permit_number': 'AMDAL-001/2019', 'issue_date': date(2019, 6, 10), 'expiry_date': date(2024, 6, 10), 'status': 'Expired', 'notes': 'Perlu renewal segera'},
            {'land_code': 'LND-VALE-002', 'location_name': 'Vale North Sector', 'permit_type': 'HGU', 'permit_number': 'HGU-002/2016', 'issue_date': date(2016, 3, 20), 'expiry_date': date(2026, 3, 20), 'status': 'Compliant', 'notes': ''},
            {'land_code': 'LND-VALE-003', 'location_name': 'Vale South Sector', 'permit_type': 'HGU', 'permit_number': 'HGU-003/2017', 'issue_date': date(2017, 7, 15), 'expiry_date': date(2027, 7, 15), 'status': 'Compliant', 'notes': ''},
            {'land_code': 'LND-VALE-001', 'location_name': 'Vale Central Mining Area', 'permit_type': 'UKL-UPL', 'permit_number': 'UKL-001/2021', 'issue_date': date(2021, 2, 20), 'expiry_date': date(2026, 2, 20), 'status': 'Expiring Soon', 'notes': ''},
            {'land_code': 'LND-ACQ-001', 'location_name': 'Sorowako Expansion Area', 'permit_type': 'SHM', 'permit_number': 'SHM-045/2020', 'issue_date': date(2020, 5, 10), 'expiry_date': None, 'status': 'Compliant', 'notes': 'SHM tidak expire'},
            {'land_code': 'LND-ACQ-002', 'location_name': 'Magani Buffer Zone', 'permit_type': 'SHM', 'permit_number': 'SHM-046/2021', 'issue_date': date(2021, 8, 15), 'expiry_date': None, 'status': 'Compliant', 'notes': ''},
            {'land_code': 'LND-IUPK-001', 'location_name': 'IUPK Block A', 'permit_type': 'IUPK', 'permit_number': 'IUPK-A/2010', 'issue_date': date(2010, 1, 10), 'expiry_date': date(2030, 1, 10), 'status': 'Compliant', 'notes': ''},
            {'land_code': 'LND-IUPK-001', 'location_name': 'IUPK Block A', 'permit_type': 'IMB', 'permit_number': 'IMB-001/2015', 'issue_date': date(2015, 5, 20), 'expiry_date': date(2025, 5, 20), 'status': 'Expiring Soon', 'notes': 'Proses renewal'},
            {'land_code': 'LND-PPKH-001', 'location_name': 'PPKH Conservation Area 1', 'permit_type': 'PPKH', 'permit_number': 'PPKH-001/2018', 'issue_date': date(2018, 3, 15), 'expiry_date': date(2028, 3, 15), 'status': 'Compliant', 'notes': ''},
            {'land_code': 'LND-OPS-002', 'location_name': 'Processing Plant Area', 'permit_type': 'IMB', 'permit_number': 'IMB-002/2020', 'issue_date': date(2020, 9, 10), 'expiry_date': date(2025, 9, 10), 'status': 'Expiring Soon', 'notes': ''},
            {'land_code': 'LND-OPS-002', 'location_name': 'Processing Plant Area', 'permit_type': 'UKL-UPL', 'permit_number': 'UKL-002/2019', 'issue_date': date(2019, 11, 20), 'expiry_date': date(2024, 11, 20), 'status': 'Expired', 'notes': 'Urgent renewal'},
        ]
        
        for data in compliances_data:
            LandCompliance.objects.get_or_create(
                land_code=data['land_code'], 
                permit_type=data['permit_type'],
                defaults=data
            )
        
        self.stdout.write(f'  Created {len(compliances_data)} compliances')

    def seed_litigations(self):
        """Seed Litigation from frontend mock data"""
        self.stdout.write('Seeding Litigation...')
        
        litigations_data = [
            {'case_code': 'LIT-2025-001', 'land_code': 'LND-VALE-001', 'case_type': 'Land Ownership', 'claimant': 'Ahmad Kusuma', 'description': 'Klaim kepemilikan lahan oleh warga lokal dengan bukti sertifikat lama', 'start_date': date(2025, 1, 15), 'status': 'Active', 'priority': 'High'},
            {'case_code': 'LIT-2025-002', 'land_code': 'LND-ACQ-001', 'case_type': 'Compensation Claim', 'claimant': 'Siti Rahayu', 'description': 'Klaim kompensasi tambahan untuk pembebasan lahan', 'start_date': date(2025, 2, 10), 'status': 'Under Review', 'priority': 'Medium'},
            {'case_code': 'LIT-2025-003', 'land_code': 'LND-VALE-002', 'case_type': 'Boundary Dispute', 'claimant': 'Budi Santoso', 'description': 'Sengketa batas lahan dengan area operasional Vale', 'start_date': date(2025, 1, 20), 'status': 'Active', 'priority': 'High'},
            {'case_code': 'LIT-2024-015', 'land_code': 'LND-ACQ-002', 'case_type': 'Compensation Claim', 'claimant': 'Dewi Lestari', 'description': 'Klaim kompensasi untuk kerusakan tanaman', 'start_date': date(2024, 11, 5), 'status': 'Resolved', 'priority': 'Low'},
            {'case_code': 'LIT-2025-004', 'land_code': 'LND-IUPK-001', 'case_type': 'Environmental Claim', 'claimant': 'Kelompok Tani Sorowako', 'description': 'Klaim dampak lingkungan terhadap area pertanian', 'start_date': date(2025, 3, 1), 'status': 'Under Review', 'priority': 'High'},
            {'case_code': 'LIT-2024-020', 'land_code': 'LND-ACQ-003', 'case_type': 'Boundary Dispute', 'claimant': 'Hendra Wijaya', 'description': 'Perbedaan batas kepemilikan dengan area jalan akses', 'start_date': date(2024, 12, 10), 'status': 'Resolved', 'priority': 'Medium'},
            {'case_code': 'LIT-2025-005', 'land_code': 'LND-VALE-003', 'case_type': 'Land Ownership', 'claimant': 'Keluarga Marzuki', 'description': 'Klaim kepemilikan berdasarkan warisan keluarga', 'start_date': date(2025, 2, 28), 'status': 'Active', 'priority': 'High'},
            {'case_code': 'LIT-2025-006', 'land_code': 'LND-OPS-001', 'case_type': 'Others', 'claimant': 'Yusuf Rahman', 'description': 'Klaim akses jalan yang terblokir operasional', 'start_date': date(2025, 3, 15), 'status': 'Under Review', 'priority': 'Low'},
            {'case_code': 'LIT-2024-018', 'land_code': 'LND-ACQ-004', 'case_type': 'Compensation Claim', 'claimant': 'Nina Fitriani', 'description': 'Klaim kompensasi untuk relokasi rumah', 'start_date': date(2024, 11, 20), 'status': 'Dismissed', 'priority': 'Medium'},
            {'case_code': 'LIT-2025-007', 'land_code': 'LND-PPKH-001', 'case_type': 'Environmental Claim', 'claimant': 'LSM Lingkungan Luwu', 'description': 'Klaim dampak terhadap area konservasi', 'start_date': date(2025, 3, 20), 'status': 'Active', 'priority': 'High'},
        ]
        
        for data in litigations_data:
            Litigation.objects.get_or_create(case_code=data['case_code'], defaults=data)
        
        self.stdout.write(f'  Created {len(litigations_data)} litigations')

    def seed_stakeholders(self):
        """Seed Stakeholder from frontend mock data"""
        self.stdout.write('Seeding Stakeholders...')
        
        stakeholders_data = [
            {'sh_id': 'SH001', 'nama': 'PT. Vale Indonesia', 'tipe': 'Perusahaan', 'kategori': 'Primary', 'alamat': 'Sorowako, Sulawesi Selatan', 'kontak': '0411-5221234', 'interest': 5, 'influence': 5},
            {'sh_id': 'SH002', 'nama': 'Pemerintah Kabupaten Luwu Timur', 'tipe': 'Pemerintah', 'kategori': 'Primary', 'alamat': 'Malili, Luwu Timur', 'kontak': '0461-21001', 'interest': 5, 'influence': 5},
            {'sh_id': 'SH003', 'nama': 'Komunitas Masyarakat Sorowako', 'tipe': 'Masyarakat', 'kategori': 'Primary', 'alamat': 'Sorowako, Luwu Timur', 'kontak': '0812-4567-8901', 'interest': 4, 'influence': 3},
            {'sh_id': 'SH004', 'nama': 'LSM Lingkungan Sulawesi', 'tipe': 'NGO', 'kategori': 'Secondary', 'alamat': 'Makassar, Sulawesi Selatan', 'kontak': '0411-3456789', 'interest': 4, 'influence': 3},
            {'sh_id': 'SH005', 'nama': 'Media Lokal Sulawesi', 'tipe': 'Media', 'kategori': 'Secondary', 'alamat': 'Makassar, Sulawesi Selatan', 'kontak': '0411-8765432', 'interest': 3, 'influence': 4},
        ]
        
        for data in stakeholders_data:
            StakeholderNew.objects.get_or_create(sh_id=data['sh_id'], defaults=data)
        
        self.stdout.write(f'  Created {len(stakeholders_data)} stakeholders')
