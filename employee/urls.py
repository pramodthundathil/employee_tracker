from django.urls import path
from . import views

urlpatterns = [
    path('mark_attendance_sheet', views.mark_attendance_sheet, name='mark_attendance_sheet'),
    path('messages_from_employer', views.messages_from_employer, name='messages_from_employer'),
    path('my_feedback', views.my_feedback, name='my_feedback'),
    path('my_salaries', views.my_salaries, name='my_salaries'),
    path('my_leaves', views.my_leaves, name='my_leaves'),
    path('my_tasks', views.my_tasks, name='my_tasks'),
    path("mark_attendance",views.mark_attendance,name="mark_attendance"),
    path("delete_feedback/<int:feedback_id>",views.delete_feedback,name="delete_feedback"),
    path("download_salary_slip/<int:salary_id>",views.download_salary_slip,name="download_salary_slip"),
    path("delete_leave_employee/<int:leave_id>", views.delete_leave_employee, name="delete_leave_employee"),
    path("view_tasks/<int:task_id>", views.view_tasks, name="view_tasks"),

]