from django.urls import path, include
from time_tracker import views




app_name = 'time_tracker'

urlpatterns = [
    path('project/', include([
        path('create', views.ProjectCreate.as_view(), name='project-create'),
        path('list', views.ProjectList.as_view(), name='project-list'),
        path('delete/<int:pk>', views.ProjectDelete.as_view(), name='project-delete'),
        path('get/<int:pk>', views.ProjectGetDetails.as_view(), name='project-get-details'),
        path('update/<int:pk>', views.ProjectUpdate.as_view(), name='project-update'),
        # path('update/status/<int:pk>', views.ProjectUpdateStatus.as_view(), name='project-update-status'),
    ])),
    path('task/', include([
        path('create', views.CreateTask.as_view(), name='task-create'),
        path('delete/<int:pk>', views.DeleteTask.as_view(), name='task-delete'),
        path('get/<int:pk>', views.RetrieveTask.as_view(), name='task-get-details'),
        path('list', views.ListTask.as_view(), name='task-list'),
        path('update/status/<int:pk>', views.UpdateStatusTask.as_view(), name='task-update-status'),
        path('update/<int:pk>', views.UpdateTask.as_view(), name='task-updates'),
    ])),
    path('assigned_task/', include([
        path('create', views.AssignedTaskCreate.as_view(), name='assigned_task-create'),
        path('manager/list', views.ManagerListAssignedTask.as_view(), name='manager-assigned-task-list'),
        path('developer/list', views.DeveloperListAssignedTask.as_view(), name='developer-assigned-task-list'),
        path('get/<int:pk>', views.RetrieveAssignedTask.as_view(), name='assigned-task-details'),
        path('delete/<int:pk>', views.DeleteAssignedTask.as_view(), name='assigned-task-delete'),
        path('change/developer/<int:pk>', views.ChangeAssignTaskDeveloper.as_view(), name='change-developer'),
    ])),
    path('time_log_task/', include([
        path('create', views.CreateTimeLogTask.as_view(), name='time-log-task-create'),
        path('update/end_time/<int:pk>', views.EndTimeUpdateTimeLogTask.as_view(),
             name='time-log-task-update-end-time'),
        path('delete/<int:pk>', views.DeleteTimeLogTask.as_view(), name='time-log-task-delete'),
        path('list', views.ListTimeLogTask.as_view(), name='time-log-task-list'),
    ])),
    path('developer/report', views.Report.as_view(), name='report-developer'),

    path('comment/', include([
        path('create', views.CreateComment.as_view(), name='comment-create'),
        path('list', views.ListComments.as_view(), name='comment-list'),
        path('delete/<int:pk>', views.DeleteComments.as_view(), name='comment-delete'),
        path('get/<int:pk>', views.GetComment.as_view(), name='get-comment-details'),
        path('update/<int:pk>', views.UpdateComments.as_view(), name='update-comment'),
    ])),

    path('track-time/', include([
        path('start', views.CreateTimeTracker.as_view(), name='time-tracker-create'),
        path('delete/<int:pk>', views.DeleteTimeTracker.as_view(), name='time-tracker-delete'),
        path('get/<int:pk>', views.RetrieveTimeTracker.as_view(), name='get-time-tracker-details'),
        path('end/<int:pk>', views.UpdateTimeTracker.as_view(), name='update-time-tracker'),
    ])),

    path('track-log-validation/', include([
        path('delete/<int:pk>', views.DeleteTimeLogValidation.as_view(), name='track-log-validation-delete'),
        path('get/<int:pk>', views.RetrieveTimeLogValidation.as_view(), name='get-track-log-validation-details'),
        path('update/<int:pk>', views.UpdateTimeLogValidation.as_view(), name='update-track-log-validation'),
        path('list/<int:time_tracker_id>', views.ListTimeLogValidation.as_view(), name='list-track-log-validation'),
    ])),
]
