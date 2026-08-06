REQUIRED_DOCUMENT_TYPES = {"DEED", "CADASTRAL", "PLAN", "ENERGY"}

def calculate_domus_score(property_obj):
    score = 0
    cadastral_fields = [
        property_obj.cadastral_sheet,
        property_obj.cadastral_particle,
        property_obj.cadastral_subaltern,
    ]
    score += sum(10 for value in cadastral_fields if value)

    present_types = set(property_obj.documents.values_list("document_type", flat=True))
    score += len(REQUIRED_DOCUMENT_TYPES.intersection(present_types)) * 15

    if property_obj.owners.exists():
        score += 10

    return min(score, 100)

def refresh_domus_score(property_obj):
    property_obj.domus_score = calculate_domus_score(property_obj)
    property_obj.save(update_fields=["domus_score", "updated_at"])
    return property_obj.domus_score
