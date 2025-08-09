from rest_framework import serializers
from base import models

class PouchSerializer(serializers.ModelSerializer):
    quantity_formatted = serializers.SerializerMethodField()
    date_updated = serializers.SerializerMethodField()

    class Meta: 
        model = models.Pouch
        fields = ['id', 'size', 'quantity_formatted', 'date_updated']
        
    def get_quantity_formatted(self, obj):
        return "{:,}".format(obj.quantity)  

    def get_date_updated(self, obj):
        return obj.date_updated.date().strftime("%d-%m-%y")
    
class PouchInSerializer(serializers.ModelSerializer):
    pouch = PouchSerializer()
    quantity_formatted = serializers.SerializerMethodField()
    date_created = serializers.SerializerMethodField()

    class Meta: 
        model = models.Pouch_In
        fields = ['id', 'pouch', 'quantity', 'date_created', 'quantity_formatted']
        
    def get_quantity_formatted(self, obj):
        return "{:,}".format(obj.quantity)  

    def get_date_created(self, obj):
        return obj.date_created.date().strftime("%d-%m-%y")
    
class PouchInFormSerializer(serializers.ModelSerializer):
    quantity_formatted = serializers.SerializerMethodField()

    class Meta:
        model = models.Pouch_In
        fields = ['pouch', 'quantity', 'quantity_formatted']

    def create(self, validated_data):
        pouch = validated_data['pouch']
        added_quantity = validated_data['quantity']
        
        # increment pouch quantity
        pouch.quantity += added_quantity
        pouch.save()
        print("working")
        return super().create(validated_data)
    
    def get_quantity_formatted(self, obj):
        return "{:,}".format(obj.quantity)  
    
class PouchOutSerializer(serializers.ModelSerializer):
    pouch = PouchSerializer()
    quantity_formatted = serializers.SerializerMethodField()
    date_created = serializers.SerializerMethodField()
    
    class Meta: 
        model = models.Pouch_Out
        fields = ['id', 'getter', 'quantity', 'purpose', 'status', 'given', 'date_created', 'pouch', 'quantity_formatted']

    def create(self, validated_data):
        pouch = validated_data['pouch']
        added_quantity = validated_data['quantity']
        
        # increment pouch quantity
        pouch.quantity -= added_quantity
        pouch.save()

        return super().create(validated_data)

    def get_date_created(self, obj):
        return obj.date_created.date().strftime("%d-%m-%y")

    def get_quantity_formatted(self, obj):
        return "{:,}".format(obj.quantity)  
    
class PouchOutFormSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = models.Pouch_Out
        fields = ['getter', 'quantity', 'purpose', 'status', 'given', 'pouch']

    def create(self, validated_data):
        pouch = validated_data['pouch']
        added_quantity = validated_data['quantity']
        
        # increment pouch quantity
        pouch.quantity -= added_quantity
        pouch.save()

        return super().create(validated_data)