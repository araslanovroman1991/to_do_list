from django.utils import timezone
from rest_framework import serializers

from app.admin_panel.admin import Tasks


class TasksSerializer(serializers.ModelSerializer):
    update_time = serializers.SerializerMethodField()

    class Meta:
        model = Tasks
        fields = "__all__"
        read_only_fields = ("update_time",)

    def get_update_time(self, obj):
        if obj.update_time:
            return timezone.localtime(obj.update_time).isoformat()
        return None
