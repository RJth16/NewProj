from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from masterfile.Geo import findloc


def index(request):
    return render(request, 'index.html')

@require_http_methods(["GET"])
def latlongloc(request):
    response = findloc.query_address(
        request.GET['address'], service=request.GET.get('service', 'google'))
    return JsonResponse(response)

