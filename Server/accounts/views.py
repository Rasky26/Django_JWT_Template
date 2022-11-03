# Import the core libraries and functions
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

# Import the used database tables
from accounts.models import User
from django.contrib.auth.models import Group

# Import the used serializers
from accounts.serializers import RegistrationSerializer, GroupSerializer, UserSerializer


# ----------------------------------------------------------------
# https://www.django-rest-framework.org/tutorial/quickstart/#views
# ----------------------------------------------------------------

class CurrentUserViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """
        Returns the current user based on their token authentication information.
        This restricts the user's information by binding it directly with
        the current token.
        """
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=request.auth.payload["user_id"])
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Creates a new user in the system
# class CustomUserCreate(APIView):
class RegisterUser(CreateAPIView):
    # Any user should be allowed to register, so AllowAny
    permission_classes = (AllowAny,)

    # Validates a new user's information, saves it, and returns that user information
    def post(self, request):
        """
        Method that takes in the new user information and adds a unique
        user to the database. Returns the registration data with the
        password removed.
        """
        # Set the JSON data to the serailizer object
        serializer = RegistrationSerializer(data=request.data)
        # Validate the data as valid
        if serializer.is_valid():
            # Save the data to the database and return it to a `user` variable.
            # Look at the serializer's `create` method.
            user = serializer.save()
            # Check that a valid save was made
            if user:
                # Get the user data in JSON format
                json_response = serializer.data
                # Return that data to the user with a 201 status
                return Response(json_response, status=status.HTTP_201_CREATED)
        # If any error occured, return a 400 with errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# On logout, moves that used token to the `blacklist` to keep users
# from accessing content without having to login again.
class BlacklistTokenUpdateView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        """
        Upon logout, take the "request_token" from the request
        and add it to the blacklist model.
        """
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)