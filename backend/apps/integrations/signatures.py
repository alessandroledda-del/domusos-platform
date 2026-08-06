import hashlib
import hmac
import json

def canonical_payload(payload):
    return json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")

def sign_payload(payload, secret):
    return hmac.new(
        secret.encode("utf-8"),
        canonical_payload(payload),
        hashlib.sha256,
    ).hexdigest()

def verify_signature(payload, secret, signature):
    expected = sign_payload(payload, secret)
    return hmac.compare_digest(expected, signature or "")
