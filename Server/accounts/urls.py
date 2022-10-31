# Import core libraries and functions
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Import the `User` views
from accounts import views
from accounts.views import CurrentUserViewSet, RegisterUser, BlacklistTokenUpdateView


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # Login / Logout methods provided by django-rest-framework
    # #    --> can be removed later...
    # path('', include('rest_framework.urls', namespace='rest_framework')),
    
    # Update
    # Access the current user's information.
    # Because I use a generic `Viewset` in views.py, I have to specify the acceptable
    # methods. In this case, the only method being allowed is `get`.
    path("user/", CurrentUserViewSet.as_view({'get': 'get'}), name="current_user"),
    # Get a new refresh token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Get a session and refresh token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Register a new user
    path('register/', RegisterUser.as_view(), name="register_user"),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(), name='blacklist')
]