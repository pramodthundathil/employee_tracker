from django.urls import path
from . import views

urlpatterns = [
    path("HomePage",views.HomePage,name="HomePage"),   
    path("AdminIndex",views.AdminIndex,name="AdminIndex"),  
    path("VolunteerIndex",views.VolunteerIndex,name="VolunteerIndex"),  
    path("",views.SignIn,name="SignIn"),
    path("SignUp",views.SignUp,name="SignUp"),
    path("SignOut",views.SignOut,name="SignOut"),
    path("employee_index",views.employee_index,name="employee_index"),
    path("profile", views.profile, name="profile"),


    path("my_employees",views.my_employees,name="my_employees"),
    path("edit_employee/<int:pk>",views.edit_employee,name="edit_employee"),
    path("delete_employee/<int:pk>",views.delete_employee,name="delete_employee"),
    path("attendance_sheet",views.attendance_sheet,name="attendance_sheet"),
    path("employee_attendance_view/<int:employee_id>",views.employee_attendance_view,name="employee_attendance_view"),
    path("messages_to_employees",views.messages_to_employees,name="messages_to_employees"),
    path("delete_message/<int:pk>", views.delete_message, name="delete_message"),
    path("sent_personal_message",views.sent_personal_message,name="sent_personal_message"),
    path("employee_feedback",views.employee_feedback,name="employee_feedback"),
    path("salaries",views.salaries,name="salaries"),
    path("edit_salary/<int:pk>", views.edit_salary, name="edit_salary"),
    path("delete_salary/<int:pk>", views.delete_salary, name="delete_salary"),

    path("leaves", views.leaves, name="leaves"),
    path("delete_leave/<int:pk>", views.delete_leave, name="delete_leave"),
    path("view_leave/<int:pk>", views.view_leave, name="view_leave"),
    path("approve_leave/<int:pk>", views.approve_leave, name="approve_leave"),
    path("reject_leave/<int:pk>", views.reject_leave, name="reject_leave"),

    path("assign_task", views.assign_task, name="assign_task"),

    path("edit_task/<int:pk>", views.edit_task, name="edit_task"),
    path("delete_task/<int:pk>", views.delete_task, name="delete_task"),
    path("view_task/<int:pk>", views.view_task, name="view_task"),

    path("task_analytics", views.task_analytics, name="task_analytics"),
]
