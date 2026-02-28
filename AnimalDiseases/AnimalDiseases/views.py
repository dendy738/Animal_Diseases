from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest
from django.shortcuts import render


def main_page(request: HttpRequest) -> HttpResponse:
    """ Greet page view. Takes a request as parameter. """
    if request.method == 'GET':
        return render(request, "main.html")
    else:
        return HttpResponseBadRequest('This action is not supported.')