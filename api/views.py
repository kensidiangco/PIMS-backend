from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Pouch, Pouch_In, Pouch_Out
from .serializers import PouchSerializer, PouchInSerializer, PouchOutSerializer, PouchOutFormSerializer, PouchInFormSerializer, PouchBulkOutFormSerializer, PouchUpdateFormSerializer
from django.utils import timezone
from rest_framework import status

@api_view(['GET'])
def getPouchesData(request):
    pouches = Pouch.objects.all()
    serializer = PouchSerializer(pouches, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def getPouchData(request, id):
    pouch = Pouch_Out.objects.get(id=id)
    serializer = PouchOutSerializer(pouch, many=False)

    return Response(serializer.data)
    
@api_view(['GET'])
def getPouchInData(request):
    pouches = Pouch_In.objects.all()
    serializer = PouchInSerializer(pouches, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def getPouchOutData(request):
    pouches = Pouch_Out.objects.all().order_by('-date_created')
    serializer = PouchOutSerializer(pouches, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def pouch_out_today_latest(request):
    today = timezone.now().date()
    logs = Pouch_Out.objects.filter(date_created__date=today).order_by('-date_created')
    serializer = PouchOutSerializer(logs, many=True)
    return Response(serializer.data)

#POST REQUEST
@api_view(['POST'])
def addPouch(request):
    serializer = PouchSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def pouchIn(request):
    serializer = PouchInFormSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def pouchOut(request):
    serializer = PouchOutFormSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def bulk_create_pouches(request):
    serializer = PouchBulkOutFormSerializer(data=request.data, many=True)
    serializer.is_valid(raise_exception=True)
    objs = serializer.save()
    # Return created rows; DRF will serialize them automatically
    out = PouchBulkOutFormSerializer(objs, many=True)
    return Response(out.data, status=status.HTTP_201_CREATED)
    
# PUT REQUEST
@api_view(['PUT'])
def updateOutPouch(request, id):
    try:
        pouch_out = Pouch_Out.objects.get(id=id)
    except Pouch_Out.DoesNotExist:
        return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PouchUpdateFormSerializer(instance=pouch_out, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 👇 return detailed validation errors
    return Response({
        "errors": serializer.errors,
        "data_sent": request.data
    }, status=status.HTTP_400_BAD_REQUEST)


    