from .views.menu import (
    MenuApiView
)
from .views.plate import (
    PlateApiView
)
from .views.ingredient import (
    IngredientApiView
)
from .views.coyote import (
    CoyotesApiView,
)
from django.urls import path

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
    path('coyotes', CoyotesApiView.as_view()),
    path('ingredients', IngredientApiView.as_view()),
    path('plates', PlateApiView.as_view()),
    path('menus', MenuApiView.as_view()),
    path('swagger/schema/', schema_view.with_ui('swagger',
         cache_timeout=0), name="swagger-schema")
]
