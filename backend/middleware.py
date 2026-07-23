import time

import structlog


logger = structlog.get_logger('backend.request')


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.perf_counter()
        response = self.get_response(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        logger.info(
            'request_completed',
            method=request.method,
            path=request.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
            user_id=getattr(request.user, 'id', None),
            remote_addr=request.META.get('REMOTE_ADDR'),
        )
        return response
