from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from DjangoProject.Models.task import Task

class TaskView(APIView):
    def get(self, request):
        user = request.user

        tasks = Task.objects.filter(owner=user)

        data = []
        for t in tasks:
            data.append({
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "is_done": t.is_done,
                "priority": t.priority,
            })
        return Response(data)
