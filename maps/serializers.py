from rest_framework import serializers

from maps.models import Map

class MapSerializer(serializers.ModelSerializer):

    class Meta:
        model = Map
        fields = ['id', 'created', 'updated', 'name', 'data']
