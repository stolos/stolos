from django.core.management.base import BaseCommand, CommandError

from core import watcher


class Command(BaseCommand):
    help = 'Watch docker events for processes them to update Ceryx'

    def handle(self, *args, **options):
        self.stdout.write('Watching events...')
        try:
            watcher.watch()
        except Exception as err:
            raise CommandError('Watching raised an exception', err)
