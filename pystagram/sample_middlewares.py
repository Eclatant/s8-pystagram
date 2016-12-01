from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render

from .sample_exceptions import HelloWorldError


class SampleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.just_say = 'Lorem Ipsum'

    def process_exception(self, request, exc):
        if isinstance(exc, HelloWorldError):
            ctx = {
                'error': exc,
                'status': 500,
            }
            return render(request, 'error.html', ctx)

