from django.core.management.base import BaseCommand
from testing.utils import create_sessions_for_weeks

class Command(BaseCommand):
    help = 'Generate sessions for weeks based on weekly and extra sessions'

    def add_arguments(self, parser):
        parser.add_argument('start_date', type=str, help='Start date in YYYY-MM-DD format')
        parser.add_argument('end_date', type=str, help='End date in YYYY-MM-DD format')
        parser.add_argument('teacher_id', type=int, help='ID of the teacher')

    def handle(self, *args, **kwargs):
        start_date = kwargs['start_date']
        end_date = kwargs['end_date']
        teacher_id = kwargs['teacher_id']
        create_sessions_for_weeks(start_date, end_date, teacher_id)
        self.stdout.write(self.style.SUCCESS('Successfully generated sessions'))

""" 
python manage.py generate_sessions 2024-04-30 2024-06-10 1 """
