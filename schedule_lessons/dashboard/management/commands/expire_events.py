from django.core.management.base import BaseCommand
from dashboard.models import Lesson
import datetime

class Command(BaseCommand):

    help = 'Expires event objects which are out-of-date'

    def handle(self, *args, **options):
        Lesson.objects.filter(end_time__gt=datetime.datetime.now()).delete()
