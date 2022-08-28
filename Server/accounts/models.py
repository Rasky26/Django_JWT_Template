# Import the core libraries and functions
# from django.contrib.auth.models import AbstractUser


# # Abstract the `User` model, allowing for later updates
# # to be made to that database table.
# class User(AbstractUser):
#     pass

#     def __str__(self):
#         """
#         Display the user's name based on provided information.
#         """
#         if (not self.first_name) and (not self.last_name):
#             return f"{self.username}"
#         elif not self.first_name:
#             return f"{self.username} | {self.last_name}"
#         elif not self.last_name:
#             return f"{self.username} | {self.first_name}"
#         return f"{self.username} | {self.first_name} {self.last_name}"

#     def display_name(self):
#         """
#         Returns a name string for easy display.
#         """
#         return self.__str__()
            
#     # Set the database information
#     class Meta:
#         verbose_name = "User"
#         verbose_name_plural = "Users"
#         ordering = (
#             "last_name",
#             "first_name",
#         )

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        # Check that superuser is assigned as staff
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')

        # Check that the superuser is also a superuser
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, first_name, password, **other_fields)

    def create_user(self, email, user_name, first_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, **other_fields)
        user.set_password(password)
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

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    # def __str__(self):
    #     return self.user_name

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

    def display_name(self):
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