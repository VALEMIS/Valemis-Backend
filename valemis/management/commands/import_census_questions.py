"""
Management command to import census questions from Excel file
"""
import json
import os
from django.core.management.base import BaseCommand
from valemis.models import CensusQuestion


class Command(BaseCommand):
    help = 'Import census survey questions from Excel data'

    def handle(self, *args, **options):
        # Path to questions JSON file
        json_file = '/home/valemis/census_questions_full.json'

        if not os.path.exists(json_file):
            self.stdout.write(self.style.ERROR(f'File not found: {json_file}'))
            return

        # Read questions from JSON
        with open(json_file, 'r', encoding='utf-8') as f:
            questions_data = json.load(f)

        # Clear existing questions
        count_before = CensusQuestion.objects.count()
        CensusQuestion.objects.all().delete()

        # Import questions
        imported = 0
        for q in questions_data:
            # Determine category based on question number range
            q_num = q['column_index']
            category = self.get_category(q_num)

            question_obj = CensusQuestion.objects.create(
                question_number=q_num,
                question_text=q['question_clean'],
                field_name=q['field_name'],
                category=category,
                options=q['options'],
                is_required=True if q_num in [1, 2] else False,
                validation_type='text'
            )
            imported += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully imported {imported} questions '
                f'(deleted {count_before} old questions)'
            )
        )

    def get_category(self, question_num):
        """Determine category based on question number"""
        categories = {
            range(1, 9): 'Identifikasi',
            range(9, 17): 'Demografi',
            range(17, 19): 'Kesehatan',
            range(19, 24): 'Pekerjaan',
            range(24, 26): 'Kesehatan Lanjutan',
            range(26, 28): 'Pangan',
            range(28, 32): 'Keuangan',
            range(32, 40): 'Bisnis',
            range(40, 44): 'Perumahan',
            range(44, 46): 'Kerentanan',
        }

        for range_obj, category in categories.items():
            if question_num in range_obj:
                return category
        return 'Lainnya'
