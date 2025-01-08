from datetime import datetime, timedelta

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from time_tracker.models import *
from users.serializers import *


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ('user',  'status')

        


class ListProjectSerializer(serializers.ModelSerializer):
    total_time_hr = serializers.SerializerMethodField('_get_total_time')

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ('user', 'status')

    def _get_total_time(self, project):
        data = TaskSerializer(Task.objects.filter(project=project), context={'request': self.context['request']},
                              many=True).data
        total_time = sum([float(j) for dict_data in data for i, j in dict_data.items() if i == 'total_time_hr'])
        return total_time


class UpdateStatusProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('status',)


class TaskSerializer(serializers.ModelSerializer):
    assigned_task = serializers.SerializerMethodField('_get_assigned_task')
    total_time_hr = serializers.SerializerMethodField('_get_total_time')

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ('user',  'status')

    def _get_assigned_task(self, task):
        serializers_data = AssignTaskDataSerializer(AssignTask.objects.filter(task=task), many=True)
        return serializers_data.data

    def _get_total_time(self, task):
        data = AssignTaskSerializer(AssignTask.objects.filter(task=task), many=True).data
        total_time = sum([float(j) for dict_data in data for i, j in dict_data.items() if i == 'total_time_hr'])
        return total_time


class UpdateStatusTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('status',)


class AssignTaskDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssignTask
        fields = "__all__"


class AssignTaskSerializer(serializers.ModelSerializer):
    total_time_hr = serializers.SerializerMethodField('_get_total_time')

    class Meta:
        model = AssignTask
        fields = "__all__"
        # read_only_fields = ('business',)

    def validate(self, data):
        task = data.get("task")
        developer = data.get("developer")
        project = ProjectSerializer(Project.objects.get(id=task.project.id), many=False).data
        project_members = project['team'] # remove + project['manager]
        if developer.id not in project_members:
            raise ValidationError("This Developer is not assign to this Project")
        return data

    def _get_total_time(self, assign_task):
        data = TimeLogTask.objects.filter(assigned_task=assign_task, developer=assign_task.developer)
        total = sum([float(i.total_time_hr) for i in data])
        return total


class DeveloperAssignTaskSerializer(serializers.ModelSerializer):
    total_time_hr = serializers.SerializerMethodField('_get_total_time')
    time_log_task = serializers.SerializerMethodField('_get_time_log_task')

    class Meta:
        model = AssignTask
        fields = "__all__"

    def _get_total_time(self, assign_task):
        data = TimeLogTask.objects.filter(assigned_task=assign_task, developer=assign_task.developer)
        total = sum([float(i.total_time_hr) for i in data])
        return total

    def _get_time_log_task(self, assign_task):
        data = TimeLogTaskSerializer(instance=TimeLogTask.objects.filter(assigned_task=assign_task), many=True).data
        return data


class ChangeAssignTaskDeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignTask
        fields = ('developer', 'note')

    def validate(self, data):
        assign_task = AssignTask.objects.get(id=self.context['request'].parser_context.get('kwargs').get('pk'))
        developer = data.get("developer")
        project = ProjectSerializer(Project.objects.get(id=assign_task.task.project.id), many=False).data
        project_members = project['team'] # remove + project['manager]
        if developer.id not in project_members:
            raise ValidationError("This Developer is not assign to this Project")
        return data


class TimeLogTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLogTask
        fields = "__all__"
        read_only_fields = ('developer', 'total_time_hr')

    def validate(self, data):
        assign_task = data.get('assigned_task')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        time = (end_time - start_time)
        if self.context['request'].user != assign_task.developer:
            raise ValidationError("Please Select Task That Are Assigned To You.")
        data['total_time_hr'] = str(round(time.total_seconds() / 3600, 2))
        return data


class EndTimeUpdateTimeLogTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLogTask
        fields = ('end_time',)

    def validate(self, data):
        time_log_task = TimeLogTask.objects.get(id=self.context['request'].parser_context.get('kwargs').get('pk'))
        start_time = time_log_task.start_time
        end_time = data.get('end_time')
        time = (end_time - start_time)
        data['total_time_hr'] = str(round(time.total_seconds() / 3600, 2))
        return data


class ReportTimeLogTaskSerializer(serializers.ModelSerializer):
    assigned_task = AssignTaskSerializer(many=False, read_only=True)

    class Meta:
        model = TimeLogTask
        fields = "__all__"


class ReportSerializer(serializers.Serializer):
    start_date = serializers.DateTimeField(required=True)
    end_date = serializers.DateTimeField(required=True)
    project = serializers.IntegerField(required=False, default=0)

    # assigned_task = AssignTaskSerializer(read_only=True)

    class Meta:
        fields = "__all__"

    def report_data(self):
        start_date = self.validated_data.get('start_date')
        end_date = self.validated_data.get('end_date')

        if self.validated_data.get('start_date') > self.validated_data.get('end_date'):
            raise ValidationError('Please Enter Valid Date and Time')

        
        dates = [start_date + timedelta(days=x) for x in
                 range(((end_date + timedelta(days=1)) - start_date).days)] 

        time_log_data = []
        task = []
        if self.context['request'].user.user_type == 'merchant':
            if self.validated_data.get('project') > 0:
                for i in dates:
                    dict_data = {str(i): ReportTimeLogTaskSerializer(TimeLogTask.objects.filter(start_time__date__gte=i,
                                                                                                end_time__date__lte=i,
                                                                                                assigned_task__task__project__id=self.validated_data.get('project')), many=True).data}
                    time_log_data.append(dict_data)
                task = [TaskSerializer(i, many=False).data for i in
                        Task.objects.filter(project__id=self.validated_data.get('project'))]
            else:
                for i in dates:
                    dict_data = {str(i): ReportTimeLogTaskSerializer(TimeLogTask.objects.filter(start_time__date__gte=i,
                                                                                                end_time__date__lte=i), many=True).data}
                    time_log_data.append(dict_data)
                # task = [TaskSerializer(i, many=False).data for i in
                #         Task.objects.filter(business=self.context['request'].user.business)]
        elif self.context['request'].user.user_type == 'manager':
            if self.validated_data.get('project') > 0:
                for i in dates:
                    dict_data = {str(i): ReportTimeLogTaskSerializer(TimeLogTask.objects.filter(start_time__date__gte=i,
                                                                                                end_time__date__lte=i,
                                                                                                assigned_task__task__project__id=self.validated_data.get('project'))
                                                                     , assigned_task__task__project__manager=self.context['request'].user, many=True).data}
                    time_log_data.append(dict_data)
                task = [TaskSerializer(i, many=False).data for i in
                        Task.objects.filter(project__id=self.validated_data.get('project'), project__manager=self.context['request'].user)]
            else:
                for i in dates:
                    dict_data = {str(i): ReportTimeLogTaskSerializer(TimeLogTask.objects.filter(start_time__date__gte=i,
                                                                                                end_time__date__lte=i, assigned_task__task__project__manager=self.context['request'].user), many=True).data}
                    time_log_data.append(dict_data)
                task = [TaskSerializer(i, many=False).data for i in
                        Task.objects.filter(project__manager=self.context['request'].user)]
        elif self.context['request'].user.user_type == 'developer':
            if self.validated_data.get('project') > 0:
                for i in dates:
                    dict_data = {str(i): ReportTimeLogTaskSerializer(TimeLogTask.objects.filter(start_time__date__gte=i,
                                                                                                end_time__date__lte=i,
                                                                                                assigned_task__task__project__id=self.validated_data.get(
                                                                                                    'project'))
                                                                     ,
                                                                     assigned_task__developer=self.context[
                                                                         'request'].user, many=True).data}
                    time_log_data.append(dict_data)
                task = [TaskSerializer(i, many=False).data for i in
                        Task.objects.filter(project__id=self.validated_data.get('project'),
                                            project__team__in=[self.context['request'].user])]
            else:
                for i in dates:
                    dict_data = {str(i): ReportTimeLogTaskSerializer(TimeLogTask.objects.filter(start_time__date__gte=i,
                                                                                                end_time__date__lte=i, assigned_task__developer=self.context['request'].user), many=True).data}
                    time_log_data.append(dict_data)
                task = [TaskSerializer(i, many=False).data for i in
                        Task.objects.filter(project__team__in=[self.context['request'].user.id])]
        for i in task:
            for dates_data in time_log_data:
                for k, v in dates_data.items():
                    for data in v:
                        if i['id'] == data['assigned_task']['task']:
                            i['time_log_data'] = dates_data
                        else:
                            i['time_log_data'] = []
        return task


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"
        read_only_fields = ('user',)


class UpdatesCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ("message",)


class TimeTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTracker
        fields = "__all__"
        read_only_fields = ('user', 'is_active')


class UpdateTimeTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTracker
        fields = "__all__"
        read_only_fields = ('user', 'is_active')


class TimeLogValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLogValidation
        fields = "__all__"
        read_only_fields = ('time_tracker', 'validate_at')