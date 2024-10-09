from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.


@api_view(['GET'])
def simple_api_view(request):
    data = {"message": "Hello from the API!"}
    return Response(data)
