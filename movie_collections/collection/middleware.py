# middleware.py
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin


class RequestCounterMiddleware(MiddlewareMixin):
    REQUEST_COUNT_KEY = 'request_count'

    def process_request(self, request):
        if not cache.get(self.REQUEST_COUNT_KEY):
            cache.set(self.REQUEST_COUNT_KEY, 0)

        cache.incr(self.REQUEST_COUNT_KEY, 1)
