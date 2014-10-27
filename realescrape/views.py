from django.shortcuts import render
from django.http import HttpResponse
from realescrape.models import Property
from json import dumps


def home(request):
    return render(request, 'home.html', {})


def adlisting(request):
    properties = Property.objects.all()
    properties = [p.as_dict() for p in sorted(properties, key=lambda x: x.ppsqm) if p.display]
    response = HttpResponse(dumps(properties)) 
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
