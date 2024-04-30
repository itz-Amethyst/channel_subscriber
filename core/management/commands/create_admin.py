from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


class Command(BaseCommand):
    help = 'Create initial Admin if none exist'

    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.filter(is_staff=True, is_superuser=False):
            self.stdout.write(self.style.ERROR('Admin User already exist. No action required.'))
        else:
            self.create_initial_admin()
            self.stdout.write(self.style.SUCCESS('Successfully created Admin User'))

    def create_initial_admin(self):
        User = get_user_model()
        while True:
            email = input('Enter admin email: ')
            username = input('Enter admin username: ')
            password = input('Enter admin password: ')

            # Check if a user with the given username already exists
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.ERROR('User with this username already exists. Try a different username.'))
                continue

            try:
                # Validate the password
                validate_password(password, User)

                # If the password is valid, break out of the loop
                break
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Invalid password: {e}'))

        admin_user = User.objects.create_user(email=email, password=password, is_staff=True, username=username)
        admin_user.is_active = True
        admin_user.save()
