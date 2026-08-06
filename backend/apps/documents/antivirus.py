from django.conf import settings
import pyclamd

class MalwareDetectedError(ValueError):
    pass

def scan_file(file_obj):
    if not settings.ANTIVIRUS_ENABLED:
        return {"status": "SKIPPED", "reason": "disabled"}

    client = pyclamd.ClamdNetworkSocket(
        host=settings.CLAMAV_HOST,
        port=settings.CLAMAV_PORT,
        timeout=30,
    )

    file_obj.seek(0)
    result = client.scan_stream(file_obj.read())
    file_obj.seek(0)

    if result:
        signature = next(iter(result.values()))[1]
        raise MalwareDetectedError(f"File bloccato: {signature}")

    return {"status": "CLEAN"}
