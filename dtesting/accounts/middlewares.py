import uuid
from django.utils.deprecation import MiddlewareMixin


class CustomMiddleware(MiddlewareMixin):
    """ Define a request ID """
    def process_request(self, request):
        request.track_id = uuid.uuid4().hex

class ViewsMantenimiento(MiddlewareMixin):
    """ Define a request ID"""
    def process_request(self, request):
        pass
