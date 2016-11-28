
from django.utils.deprecation import MiddlewareMixin

class SampleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.just_say = 'Lorem Ipsum'

