# Import the core libraries and functions
from rest_framework import serializers

# Import the used database tables
from accounts.models import User
from django.contrib.auth.models import Group


# Serialize the `User` table.
# Used to pass user information during the login process
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


# Serialize the `Group` table.
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password',)
        # Extra security to ensure that passwords are only allowed to be written
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Remove the password from the validated data
        password = validated_data.pop('password', None)
        # As long as the other fields exactly match the model, can set the object to the model fields
        instance = self.Meta.model(**validated_data)
        # Verify a password was supplied
        if password is not None:
            # Call the method to encrypt the password and set it into the object
            instance.set_password(password)
        # Save the new user
        instance.save()
        return instance