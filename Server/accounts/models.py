from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, password, first_name="", last_name="", **other_fields):
        """
        Function that creates a SUPERUSER that has total access to
        server operations and database values.
        """

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        # Check that superuser is assigned as staff
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')

        # Check that the superuser is also a superuser
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, password, first_name, last_name, **other_fields)

    def create_user(self, email, username, password, first_name="", last_name="", **other_fields):
        """
        Function that creates a standard user that is registered on the server
        """

        # Users MUST provide an email
        if not email:
            raise ValueError(_('You must provide an email address'))

        # Validate and normalize the email
        email = self.normalize_email(email)
        # Create the user based on provided fields
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            **other_fields)
        # Set the password for the user based on the `set_password` routine
        user.set_password(password)
        # Save the user fields to the DB
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True, verbose_name='email address')
    username = models.CharField(max_length=150, unique=True, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', validators=[UnicodeUsernameValidator], verbose_name='username')
    first_name = models.CharField(max_length=150, blank=True, verbose_name='first name')
    last_name = models.CharField(max_length=150, blank=True, verbose_name='last name')
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')
    is_active = models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='date joined')

    # Extends the functions of the base `User` model with
    # custom functions
    objects = CustomAccountManager()

    # This sets the login to utilize the `email` field to login 
    USERNAME_FIELD = 'email'
    # Required fields that a superuser MUST supply when creating an account
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


    def __str__(self):
        """
        Display the user's name based on provided information.
        """
        if (not self.first_name) and (not self.last_name):
            return f"{self.username}"
        elif not self.first_name:
            return f"{self.username} | {self.last_name}"
        elif not self.last_name:
            return f"{self.username} | {self.first_name}"
        return f"{self.username} | {self.first_name} {self.last_name}"

    def full_name(self):
        """
        Returns a name string for easy display.
        """
        return self.__str__()

    # Set the database information
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = (
            "email",
            "last_name",
            "first_name",
            "username",
        )