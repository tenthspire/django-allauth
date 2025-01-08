from django.urls import path, include
from task import views




app_name = 'task'

urlpatterns = [path('project/',include([
       path('create/', views.TaskCreate.as_view(), name='task-create'),
       path('list/', views.TaskList.as_view(), name='task-list'),
       path('delete/<int:pk>/', views.TaskDelete.as_view(), name='task-delete'),
       path('get/<int:pk>/', views.TaskGetDetails.as_view(), name='task-get-details'),
       path('update/<int:pk>/', views.TaskUpdate.as_view(), name='task-update'),
])),
 
]