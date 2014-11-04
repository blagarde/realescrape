from django.shortcuts import render
from django.http import HttpResponse
from realescrape.models import Property
from json import dumps
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from scraper import Scraper


def add_headers(view):
    def decorate(*args, **kwargs):
        request = args[0]
        if request.method == "POST":
            request.POST = json.loads(request.body)
        resp_str = "PREFLIGHT OK" if request.method == "OPTIONS" else view(*args, **kwargs)
        response = HttpResponse(resp_str)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*,Content-Type"
        return response
    return csrf_exempt(decorate)


def home(request):
    return render(request, 'home.html', {})


@add_headers
def adlisting(request):
    properties = Property.objects.all()
    properties = [p.as_dict() for p in sorted(properties, key=lambda x: x.ppsqm) if p.display]
    return dumps(properties)


@add_headers
def remove(request):
    url = request.POST['url']
    pty = Property.objects.get(url=url)
    pty.blacklisted = timezone.now()
    pty.save()
    return "Property blacklisted"


@add_headers
def star(request):
    url = request.POST['url']
    pty = Property.objects.get(url=url)
    pty.star = not pty.star
    pty.save()
    return pty.star

@add_headers
def save_notes(request):
    url = request.POST['url']
    pty = Property.objects.get(url=url)
    changed = (pty.notes != request.POST['notes'])
    pty.notes = request.POST['notes']
    pty.save()
    return str(changed)

@add_headers
def scrape(request):
    #sites = request.POST['sites']
    Scraper()
    return "Done!"
