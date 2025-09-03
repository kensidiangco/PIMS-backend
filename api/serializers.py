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
        fields = ['getter', 'quantity', 'purpose', 'status', 'given', 'pouch', 'date_created']

    def create(self, validated_data):
        pouch = validated_data['pouch']
        added_quantity = validated_data['quantity']
        
        # increment pouch quantity
        pouch.quantity -= added_quantity
        pouch.save()

        return super().create(validated_data)
    
# serializers for bulk create
from django.db import transaction
from django.db.models import F

class PouchOutListSerializer(serializers.ListSerializer):
    """
    Handles create() when many=True: validates stock, locks rows, updates quantities atomically,
    then bulk_creates Pouch_Out rows.
    """
    def create(self, validated_data):
        # 1) Group required quantities per pouch
        qty_by_pouch_id = {}
        out_rows = []
        for attrs in validated_data:
            pouch = attrs["pouch"]                 # already a Pouch instance
            qty = int(attrs["quantity"])
            qty_by_pouch_id[pouch.id] = qty_by_pouch_id.get(pouch.id, 0) + qty
            out_rows.append(models.Pouch_Out(**attrs))

        with transaction.atomic():
            # 2) Lock the affected Pouch rows so stock can't change mid-flight
            locked = (models.Pouch.objects
                      .select_for_update()
                      .filter(id__in=qty_by_pouch_id.keys()))

            # 3) Check stock sufficiency
            errors = {}
            locked_by_id = {p.id: p for p in locked}
            for pid, need in qty_by_pouch_id.items():
                have = locked_by_id[pid].quantity
                if have < need:
                    # Use pouch.size for readable error
                    errors[locked_by_id[pid].size] = f"have {have}, need {need}"
            if errors:
                raise serializers.ValidationError({"stock": errors})

            # 4) Deduct with F() (atomic, race-safe)
            for pid, need in qty_by_pouch_id.items():
                models.Pouch.objects.filter(id=pid).update(quantity=F("quantity") - need)

            # 5) Create the Pouch_Out rows efficiently
            created = models.Pouch_Out.objects.bulk_create(out_rows)
            return created


class PouchBulkOutFormSerializer(serializers.ModelSerializer):
    # e.g. "Small" | "Medium" | "Large"
    pouch = serializers.SlugRelatedField(
        slug_field="size",
        queryset=models.Pouch.objects.all(),
    )

    class Meta:
        model = models.Pouch_Out
        fields = ["getter", "quantity", "purpose", "status", "given", "pouch", "date_created"]
        list_serializer_class = PouchOutListSerializer

    def create(self, validated_data):
        """
        Single-object create (many=False). Keep it atomic & race-safe, same as bulk path.
        """
        qty = int(validated_data["quantity"])
        pouch = validated_data["pouch"]

        with transaction.atomic():
            # Lock the row first
            p = models.Pouch.objects.select_for_update().get(pk=pouch.pk)
            if p.quantity < qty:
                raise serializers.ValidationError({"quantity": f"have {p.quantity}, need {qty}"})
            models.Pouch.objects.filter(pk=p.pk).update(quantity=F("quantity") - qty)
            return models.Pouch_Out.objects.create(**validated_data)

class PouchUpdateFormSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = models.Pouch_Out
        fields = ['getter', 'quantity', 'purpose', 'status', 'given', 'pouch', 'date_created']
