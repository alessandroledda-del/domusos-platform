from rest_framework import serializers
from apps.properties.access import editable_properties
from .models import Case, Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def validate_case(self, value):
        request = self.context.get("request")
        if request and not editable_properties(request.user).filter(pk=value.property_id).exists():
            if value.assigned_to_id != request.user.id:
                raise serializers.ValidationError("Pratica non modificabile.")
        return value

class CaseSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    timeline = serializers.SerializerMethodField()

    class Meta:
        model = Case
        fields = "__all__"
        read_only_fields = ["created_by", "created_at", "updated_at"]

    def validate_property(self, value):
        request = self.context.get("request")
        if request and not editable_properties(request.user).filter(pk=value.pk).exists():
            raise serializers.ValidationError("Immobile non modificabile.")
        return value

    def get_timeline(self, obj):
        items = [{
            "type": "case_created",
            "label": "Pratica creata",
            "date": obj.created_at,
        }]
        for task in obj.tasks.all():
            items.append({
                "type": "task",
                "label": task.title,
                "status": task.status,
                "date": task.created_at,
            })
        return sorted(items, key=lambda item: item["date"])
