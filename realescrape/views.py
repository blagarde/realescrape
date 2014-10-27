from django.shortcuts import render
from realescrape.models import Property


def adlisting(request):
    properties = Property.objects.all()
    properties = [p for p in sorted(properties, key=lambda x: x.ppsqm) if p.display]
    return render(request, 'home.html', {"properties": properties})
