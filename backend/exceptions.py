from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler


def _first_leaf(value):
    if isinstance(value, dict):
        for nested in value.values():
            return _first_leaf(nested)
        return None
    if isinstance(value, list):
        return _first_leaf(value[0]) if value else None
    return value


def _extract_message(details, fallback):
    message = _first_leaf(details)
    return str(message) if message is not None else fallback


def standardized_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return response

    details = response.data
    fallback_message = 'Request failed.'
    trace_id = getattr(context.get('request'), 'trace_id', None)
    error_codes = exc.get_codes() if hasattr(exc, 'get_codes') else None
    first_code = _first_leaf(error_codes)

    if isinstance(exc, ValidationError):
        code = 'validation_error'
        fallback_message = 'Validation failed.'
    else:
        code = str(first_code or getattr(exc, 'default_code', 'error'))

    response.data = {
        'code': code,
        'message': _extract_message(details, fallback_message),
        'details': details,
        'trace_id': trace_id,
    }
    return response
