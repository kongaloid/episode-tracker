import time
from django.core.management.base import BaseCommand
from tracker.models import Show
from tracker.views import ShowManager

action = ShowManager()

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('============ working ... ============')

        shows = Show.objects.all()
        self.stdout.write(f'Updating {len(shows)} shows')

        for show in shows:

            action.update_show(show)
            
            self.stdout.write(f'  - {show.name}')

            ''' take it easy on the api '''
            time.sleep(20)

        return self.stdout.write(self.style.SUCCESS('  - Done!'))