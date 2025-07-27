from rest_framework import serializers
from base import models

class PouchSerializer(serializers.ModelSerializer):
    class Meta: 
        model = models.Pouch
        fields = '__all__'

    
class PouchInSerializer(serializers.ModelSerializer):
    class Meta: 
        model = models.Pouch_In
        fields = '__all__'

class PouchOutSerializer(serializers.ModelSerializer):
    class Meta: 
        model = models.Pouch_Out
        fields = '__all__'