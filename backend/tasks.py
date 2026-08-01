from decimal import Decimal

from celery import shared_task
from django.db.models import Avg

from .models import Property


@shared_task
def update_property_score(property_id, score):
    property_obj = Property.objects.get(pk=property_id)
    property_obj.domus_score = Decimal(str(score))
    property_obj.save(update_fields=['domus_score'])
    return {
        'property_id': property_obj.id,
        'domus_score': str(property_obj.domus_score),
    }


@shared_task
def calculate_company_average_score(company_id):
    average_score = (
        Property.objects.filter(company_id=company_id, domus_score__isnull=False)
        .aggregate(avg=Avg('domus_score'))
        .get('avg')
    )
    return {
        'company_id': company_id,
        'average_domus_score': float(average_score) if average_score is not None else None,
    }
