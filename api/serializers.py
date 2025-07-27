from rest_framework import serializers
from base import models

class PouchSerializer(serializers.ModelSerializer):
    class Meta: 
        model = models.Pouch
        fields = '__all__'

    
class PouchInSerializer(serializers.ModelSerializer):
    class Meta: 
        model = models.Pouch_In
        fields = ['id', 'pouch', 'quantity', 'date_created']

    def create(self, validated_data):
        pouch = validated_data['pouch']
        added_quantity = validated_data['quantity']
        
        # increment pouch quantity
        pouch.quantity += added_quantity
        pouch.save()

        return super().create(validated_data)

class PouchOutSerializer(serializers.ModelSerializer):
    class Meta: 
        model = models.Pouch_Out
        fields = '__all__'

    def create(self, validated_data):
        pouch = validated_data['pouch']
        added_quantity = validated_data['quantity']
        
        # increment pouch quantity
        pouch.quantity -= added_quantity
        pouch.save()

        return super().create(validated_data)