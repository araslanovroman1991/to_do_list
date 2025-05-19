from rest_framework import viewsets
from app.admin_panel.admin import Tasks
from app.admin_panel.serializers import TasksSerializer

class TasksViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer