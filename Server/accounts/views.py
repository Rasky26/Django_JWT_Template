# Import the core libraries and functions
from rest_framework import permissions, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
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

# ViewSets that returns a serialized `User` object
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


# ViewSets that returns a serialized 'Group' object
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated,)


# Creates a new user in the system
# class CustomUserCreate(APIView):
class RegisterUser(CreateAPIView):
    # Any user should be allowed to register, so AllowAny
    permission_classes = (AllowAny,)

    # Validates a new user's information, saves it, and returns that user information
    def post(self, request, format='json'):
        # Set the JSON data to the serailizer object
        serializer = RegistrationSerializer(data=request.data)
        # Validate the data as valid
        if serializer.is_valid():
            # Save the data to the database and return it to a `user` variable
            user = serializer.save()
            # Check that a valid save was made
            if user:
                # Get the user data in JSON format
                json = serializer.data
                # Return that data to the user with a 201 status
                return Response(json, status=status.HTTP_201_CREATED)
        # If any error occured, return a 400 with errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# On logout, moves that used token to the `blacklist` to keep users
# from accessing content without having to login again.
class BlacklistTokenUpdateView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)