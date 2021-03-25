from rest_framework.generics import ListAPIView, CreateAPIView

from maps.models import Map
from maps.serializers import MapSerializer


# List all invoices: api/invoices/
class ViewMaps(ListAPIView):
    queryset = Map.objects.all()
    serializer_class = MapSerializer


# Create a restaurant: api/restaurants/new/
class NewCoordinatesMaps(CreateAPIView):
    queryset = Map.objects.all()  
    serializer_class = MapSerializer 

    def perform_create(self, serializer):
        data = self.request.data
        coor = data.get("coordinates")
        serializer.save(coordinates=coor)
