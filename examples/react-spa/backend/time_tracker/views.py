from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from time_tracker.serializers import *
from time_tracker.models import *
from rest_framework.filters import SearchFilter
from django_filters import rest_framework as filters
from datetime import datetime

class ProjectCreate(generics.CreateAPIView):
    """
    This api use for To create Project .
    its is only access by manager and merchant.
    """
    serializer_class = ProjectSerializer
    model = Project
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProjectList(generics.ListAPIView):
    """
    This api get Project list.
    """
    serializer_class = ListProjectSerializer
    model = Project
    queryset = model.objects.all().order_by('-id')
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     return self.queryset.filter(business=self.request.user.business)


class ProjectDelete(generics.DestroyAPIView):
    """
    This api use for To delete Project .
    its is only access by manager and merchant.
    """
    serializer_class = ProjectSerializer
    model = Project
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs['pk'])

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if Task.objects.filter(project_id=self.kwargs['pk']).exists():
            return JsonResponse(data={'message': 'Project Task Exists You Can Delete it.'}, status=400)
        obj.delete()
        return JsonResponse(data={'message': 'Deleted Successfully'}, status=204)


class ProjectGetDetails(generics.RetrieveAPIView):
    """
    This api use for To get Project details.
    """
    serializer_class = ListProjectSerializer
    model = Project
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


class ProjectUpdate(generics.UpdateAPIView):
    """
    This api use for To update Project .
    its is only access by manager and merchant.
    """
    serializer_class = ProjectSerializer
    model = Project
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']

    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs['pk'])


class ProjectUpdateStatus(generics.UpdateAPIView):
    """
    This api use for To update Project status.
    its is only access by manager and merchant.
    """
    serializer_class = UpdateStatusProjectSerializer
    model = Project
    queryset = model.objects.all()
    http_method_names = ['patch']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs['pk'])


class CreateTask(generics.CreateAPIView):
    """
        In this Api is use to create task of project.
        Its only Access By Manager or Merchant
    """
    serializer_class = TaskSerializer
    model = Task
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DeleteTask(generics.DestroyAPIView):
    """
        In this Api to delete The task.
        Its only Access By Manager or Merchant
    """
    serializer_class = TaskSerializer
    model = Task
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs['pk'])

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if TimeLogTask.objects.filter(assigned_task__task__id=self.kwargs['pk']).exists():
            return JsonResponse(data={'message': 'Task Time Log Exists You Can Delete it.'}, status=400)
        obj.delete()
        return JsonResponse(data={'message': 'Deleted Successfully'}, status=204)


class RetrieveTask(generics.RetrieveAPIView):
    """
    This is api is get the data particular object.
    It can access you are login
    """
    serializer_class = TaskSerializer
    model = Task
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


class UpdateStatusTask(generics.UpdateAPIView):
    """
        In this Api is use to change the status of task.
        Its only Access By Manager or Merchant
    """
    serializer_class = UpdateStatusTaskSerializer
    model = Task
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']

    def get_queryset(self):
        return self.queryset.filter( id=self.kwargs['pk'])


class UpdateTask(generics.UpdateAPIView):
    """
        In this Api is use to update task.
        Its only Access By Manager or Merchant
    """
    serializer_class = TaskSerializer
    model = Task
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']

    def get_queryset(self):
        return self.queryset.filter( id=self.kwargs['pk'])


class TaskFilter(filters.FilterSet):
    project = filters.BaseInFilter(field_name="project", lookup_expr='in')
    ids = filters.BaseInFilter(field_name="id", lookup_expr='in')
    status = filters.CharFilter(method='status_filters')

    class Meta:
        model = Task
        fields = ["ids", "status"]

    def status_filters(self, queryset, name, value):
        if value == "active":
            return queryset.filter(status="active")
        if value == "completed":
            return queryset.filter(status='completed')
        if value == "in-progress":
            return queryset.filter(status='in-progress')


class ListTask(generics.ListAPIView):
    """
        In this Api is get List of all Task
    """
    serializer_class = TaskSerializer
    model = Task
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_class = TaskFilter
    filter_backends = [SearchFilter, filters.DjangoFilterBackend, ]
    search_fields = ['description', 'user__id', 'name']
    pagination_class = LimitOffsetPagination

    # def get_queryset(self):
    #     return self.queryset.filter(business=self.request.user.business)


class AssignedTaskCreate(generics.CreateAPIView):
    """
    In this Api is use particular task is assign to developer, which developer is part of project.
    Its only Access By Manager or Merchant
    """
    serializer_class = AssignTaskSerializer
    model = AssignTask
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # serializer.save(business=self.request.user.business)
        user = CustomUser.objects.get(id=serializer.data['developer'])

class DeveloperListAssignedTask(generics.ListAPIView):
    """
        This Api is use for to get Developer List of AssignedTask.
    """
    serializer_class = DeveloperAssignTaskSerializer
    model = AssignTask
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter( developer=self.request.user)


class AssignedTaskFilter(filters.FilterSet):
    task_id = filters.BaseInFilter(field_name="task", lookup_expr='in')

    class Meta:
        model = AssignTask
        fields = ["task_id"]


class ManagerListAssignedTask(generics.ListAPIView):
    """
        This Api is use for to get Manager List of AssignedTask.
    """
    serializer_class = AssignTaskSerializer
    model = AssignTask
    queryset = model.objects.all()
    filterset_class = AssignedTaskFilter
    filter_backends = [filters.DjangoFilterBackend, ]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return self.queryset.filter(task__project__manager=self.request.user)


class RetrieveAssignedTask(generics.RetrieveAPIView):
    """
    This is api is get the data particular object.
    It can access you are login
    """
    serializer_class = AssignTaskSerializer
    model = AssignTask
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


class DeleteAssignedTask(generics.DestroyAPIView):
    """
        In this Api to delete The AssignedTask.
        Its only Access By Manager or Merchant
    """
    serializer_class = AssignTaskSerializer
    model = AssignTask
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs['pk'])


class ChangeAssignTaskDeveloper(generics.UpdateAPIView):
    """
    In this Api to change assigned developer The AssignedTask.
    Its only Access By Manager or Merchant
    """
    serializer_class = ChangeAssignTaskDeveloperSerializer
    model = AssignTask
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']

    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs['pk'])


class CreateTimeLogTask(generics.CreateAPIView):
    serializer_class = TimeLogTaskSerializer
    model = TimeLogTask
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(developer=self.request.user)


class EndTimeUpdateTimeLogTask(generics.UpdateAPIView):
    serializer_class = EndTimeUpdateTimeLogTaskSerializer
    model = TimeLogTask
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']

    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs['pk'], developer=self.request.user,
                                    assigned_task__business=self.request.user.business)


class DeleteTimeLogTask(generics.DestroyAPIView):
    serializer_class = TimeLogTaskSerializer
    model = TimeLogTask
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs['pk'], developer=self.request.user,
                                    assigned_task__business=self.request.user.business)


class TimeLogTaskFilter(filters.FilterSet):
    assigned_task_id = filters.BaseInFilter(field_name="assigned_task", lookup_expr='in')

    class Meta:
        model = TimeLogTask
        fields = ["assigned_task_id"]


class ListTimeLogTask(generics.ListAPIView):
    """
        This Api is use for to get Developer List of Time-Log-Task.
    """
    serializer_class = TimeLogTaskSerializer
    model = TimeLogTask
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_class = TimeLogTaskFilter
    filter_backends = [filters.DjangoFilterBackend, ]

    def get_queryset(self):
        return self.queryset.filter(assigned_task__business=self.request.user.business,
                                    developer=self.request.user)


class Report(generics.ListAPIView):
    serializer_class = ReportSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.report_data()
        return Response(response)


class CreateComment(generics.CreateAPIView):
    serializer_class = CommentsSerializer
    model = Comments
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListComments(generics.ListAPIView):
    serializer_class = CommentsSerializer
    model = Comments
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     return self.queryset.filter(user__business=self.request.user.business)


class DeleteComments(generics.DestroyAPIView):
    serializer_class = CommentsSerializer
    model = Comments
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs['pk'])


class UpdateComments(generics.UpdateAPIView):
    serializer_class = UpdatesCommentsSerializer
    model = Comments
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']

    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs['pk'], user=self.request.user)


class GetComment(generics.RetrieveAPIView):
    serializer_class = CommentsSerializer
    model = Comments
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


class CreateTimeTracker(generics.CreateAPIView):
    serializer_class = TimeTrackerSerializer
    model = TimeTracker
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DeleteTimeTracker(generics.DestroyAPIView):
    serializer_class = TimeTrackerSerializer
    model = TimeTracker
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs['pk'])


class RetrieveTimeTracker(generics.RetrieveAPIView):
    serializer_class = TimeTrackerSerializer
    model = TimeTracker
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


class UpdateTimeTracker(generics.UpdateAPIView):
    serializer_class = UpdateTimeTrackerSerializer
    model = TimeTracker
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user, id=self.kwargs['pk'])

    def perform_update(self, serializer):
        serializer.save(end=datetime.now(), is_active=True)


class RetrieveTimeLogValidation(generics.RetrieveAPIView):
    serializer_class = TimeLogValidationSerializer
    model = TimeLogValidation
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


class DeleteTimeLogValidation(generics.DestroyAPIView):
    serializer_class = TimeLogValidationSerializer
    model = TimeLogValidation
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs['pk'])


class ListTimeLogValidation(generics.ListAPIView):
    serializer_class = TimeLogValidationSerializer
    model = TimeLogValidation
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(time_tracker__id=self.kwargs['time_tracker_id'])


class UpdateTimeLogValidation(generics.UpdateAPIView):
    serializer_class = TimeLogValidationSerializer
    model = TimeLogValidation
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']

    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs['pk'])

    def perform_update(self, serializer):
        serializer.save(validate_at=datetime.now())