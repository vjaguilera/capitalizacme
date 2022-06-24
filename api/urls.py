from .views.menu import (
    MenuApiView,
    MenuDetailApiView,
    PublicMenuApiView,
    ScheduleMenuApiView,
    ScheduleMenuDetailApiView
)
from .views.plate import (
    PlateApiView,
    PlateDetailApiView
)
from .views.ingredient import (
    IngredientApiView
)
from .views.user import (
    UserDetailAPI,
    RegisterUserAPIView
)
from django.urls import path

from rest_framework_simplejwt import views as jwt_views

from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view


schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Coyote API",
        default_version='1.0.0',
        description="API documentation of App",
    ),
    public=True,
)


urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('ingredients', IngredientApiView.as_view()),
    path('plates', PlateApiView.as_view()),
    path('plates/<int:plate_id>/', PlateDetailApiView.as_view()),
    path('menus/', MenuApiView.as_view()),
    path('menus/<int:menu_id>/', MenuDetailApiView.as_view()),
    path('menus/public', PublicMenuApiView.as_view()),
    path('menus/schedule', ScheduleMenuApiView.as_view()),
    path('menus/schedule/<int:scheduled_menu_id>',
         ScheduleMenuDetailApiView.as_view()),
    path('user/details', UserDetailAPI.as_view()),
    path('user/register', RegisterUserAPIView.as_view()),
    path('swagger/schema/', schema_view.with_ui('swagger',
         cache_timeout=0), name="swagger-schema")
]
