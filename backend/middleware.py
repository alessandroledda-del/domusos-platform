import uuid


class RequestTraceMiddleware:
    """Attach a stable trace identifier to every request and response."""

    header_name = 'X-Trace-Id'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        incoming_trace_id = request.headers.get(self.header_name, '').strip()
        request.trace_id = incoming_trace_id or str(uuid.uuid4())
        response = self.get_response(request)
        response[self.header_name] = request.trace_id
        return response
