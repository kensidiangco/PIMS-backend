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
    
    
#FORM SERIALIZERS
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
    

class PouchBulkOutFormSerializer(serializers.ModelSerializer):
    pouch = serializers.SlugRelatedField(
        slug_field="size",   # "small" | "medium" | "large"
        queryset=models.Pouch.objects.all()
    )

    class Meta: 
        model = models.Pouch_Out
        fields = ['getter', 'quantity', 'purpose', 'status', 'given', 'pouch', 'date_created']

    def create(self, validated_data):
        # If bulk insert (many=True), validated_data will be a list
        if isinstance(validated_data, list):
            instances = []
            for item in validated_data:
                pouch = item['pouch']
                qty = item['quantity']

                # decrement pouch quantity for each row
                pouch.quantity -= qty
                pouch.save()

                instances.append(models.Pouch_Out.objects.create(**item))
            return instances
        else:
            # single object
            pouch = validated_data['pouch']
            qty = validated_data['quantity']

            pouch.quantity -= qty
            pouch.save()

            return models.Pouch_Out.objects.create(**validated_data)
