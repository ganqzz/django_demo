import django
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View


@cache_page(86400)
def top(request):
    return render(request, 'top.html', {'version': django.__version__})


def trailing_slash(request):
    return HttpResponse('<h2>Try access to the URL with or without trailing slash.</h2>')


@csrf_exempt
def params(request):
    if request.method == 'GET':
        res = str(dict(request.GET))
    elif request.method == 'POST':
        res = str(dict(request.POST))
    else:
        res = 'GET/POST method only'
    return HttpResponse(res)


class HelloWorldView(View):
    def get(self, request):  # http GET
        return HttpResponse('Hello World!')
