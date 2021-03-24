from rest_framework.generics import ListAPIView

from maps.models import Map
from maps.serializers import MapSerializer


# List all invoices: api/invoices/
class ViewMaps(ListAPIView):
    queryset = Map.objects.all()
    serializer_class = MapSerializer

