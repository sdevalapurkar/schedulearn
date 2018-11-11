'''This module defines commands for crontab to execute regularly.'''
import datetime
from django.core.management.base import BaseCommand
from dashboard.models import Lesson

class Command(BaseCommand):
    '''This class defines commands for crontab to execute regularly.'''
    help = 'Expires event objects which are out-of-date'
    def handle(self, *args, **options):
        '''This method describes the actions to perform for crontab.'''
        Lesson.objects.filter(end_time__lt=datetime.datetime.now(
            datetime.timezone.utc)).delete()
