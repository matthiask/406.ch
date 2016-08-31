from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = '<password>'
    help = 'Updates all empty passwords to the given password'

    def add_arguments(self, parser):
        parser.add_argument('password', type=str)

    def handle(self, **options):
        if 'password' not in options:
            raise CommandError('Pass the password')

        for user in get_user_model()._default_manager.filter(password=''):
            user.set_password(options['password'])
            user.save()
