from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render(request))


def events(request):
    template = loader.get_template('events.html')
    return HttpResponse(template.render(request))


def history(request):
    template = loader.get_template('history.html')
    return HttpResponse(template.render(request))

