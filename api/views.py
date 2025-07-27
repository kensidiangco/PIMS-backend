from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Pouch
from .serializers import PouchSerializer, PouchInSerializer, PouchOutSerializer

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
    pouchs = Pouch_Out.objects.all()
    serializer = PouchOutSerializer(pouchs, many=True)

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
    serializer = PouchInSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
    
@api_view(['POST'])
def pouchOut(request):
    serializer = PouchOutSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
    
    