from .models import AuditLog

def record_audit(user, action, entity, metadata=None):
    return AuditLog.objects.create(
        user=user if getattr(user, "is_authenticated", False) else None,
        action=action,
        entity_type=entity.__class__.__name__,
        entity_id=str(getattr(entity, "pk", "")),
        metadata=metadata or {},
    )
