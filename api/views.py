from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Pouch, Pouch_In, Pouch_Out
from .serializers import PouchSerializer, PouchInSerializer, PouchOutSerializer, PouchOutFormSerializer, PouchInFormSerializer
from django.utils import timezone

@api_view(['GET'])
def getPouchData(request):
    pouchs = Pouch.objects.all()
    serializer = PouchSerializer(pouchs, many=True)

    return Response(serializer.data)
    
@api_view(['GET'])
def getPouchInData(request):
    pouchs = Pouch_In.objects.all()
    serializer = PouchInSerializer(pouchs, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def getPouchOutData(request):
    pouchs = Pouch_Out.objects.all().order_by('-date_created')
    serializer = PouchOutSerializer(pouchs, many=True)

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
    return Response(serializer.data)
    
@api_view(['POST'])
def pouchIn(request):
    serializer = PouchInFormSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
    
@api_view(['POST'])
def pouchOut(request):
    serializer = PouchOutFormSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
    
#PUT REQUEST
@api_view(['PUT'])
def updateOutPouch(request):
    serializer = PouchOutSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)