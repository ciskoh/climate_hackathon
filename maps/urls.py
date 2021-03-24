from django.urls import path
from maps.views import ViewMaps

urlpatterns = [
    path('', ViewMaps.as_view()),
]
