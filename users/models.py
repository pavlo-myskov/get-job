from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, Group)
from django.utils import timezone


# _____Overide UserManager and Base User Model_____

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_staff, is_superuser,
                     **extra_fields):
        '''Create and save a User with the given email and password.'''
        if not email:
            raise ValueError('The given email must be set')
        now = timezone.now()
        # normalize email address (lowercase)
        email = self.normalize_email(email)
        # create user model
        user = self.model(
            email=email,
            is_staff=is_staff, is_active=True,
            is_superuser=is_superuser,
            last_login=now, date_joined=now,
            **extra_fields
        )
        # set password
        user.set_password(password)
        # save user model
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        '''Create and save a regular User with the given email and password.'''
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        '''Create and save a SuperUser with the given email and password.'''
        return self._create_user(email, password, True, True, role='ADMIN',
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        JOBSEEKER = ("JOBSEEKER", 'Jobseeker')
        EMPLOYER = ("EMPLOYER", 'Employer')
        MODERATOR = ("MODERATOR", 'Moderator')

    email = models.EmailField(max_length=254, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    role = models.CharField(max_length=50, choices=Role.choices,
                            default=Role.JOBSEEKER)

    # Serve email field as a unique identifier instead of username
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    def unread_application_notifications_count(self):
        return self.application_notifications.filter(is_read=False).count()
