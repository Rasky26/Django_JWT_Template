# Import core libraries and functions
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Import the `User` views
from accounts import views
from accounts.views import RegisterUser, BlacklistTokenUpdateView


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # Contains links to `/users` and `/groups`
    path('', include(router.urls)),
    # Login / Logout methods --> can be removed later...
    path('', include('rest_framework.urls', namespace='rest_framework')),
    # Get a session and refresh token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Get a new refresh token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 
    path('register/', RegisterUser.as_view(), name="register_user"),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(), name='blacklist')
]