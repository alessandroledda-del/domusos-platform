from rest_framework import serializers
from .models import Case, Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

class CaseSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    timeline = serializers.SerializerMethodField()

    class Meta:
        model = Case
        fields = "__all__"

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
