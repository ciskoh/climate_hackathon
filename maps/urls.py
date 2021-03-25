from django.urls import path
from maps.views import ViewMaps, NewCoordinatesMaps

urlpatterns = [
    path('', ViewMaps.as_view()),
    path('new/', NewCoordinatesMaps.as_view()),
]
