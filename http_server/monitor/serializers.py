from .models import Storage
from rest_framework import serializers, viewsets

class StorageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Storage
        fields = ['pk', 'key', 'value']

class StorageViewSet(viewsets.ModelViewSet):
    serializer_class = StorageSerializer
    queryset = Storage.objects.all().order_by('key')
