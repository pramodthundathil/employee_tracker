from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import admin_only, unauthenticated_user, allowed_users
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required

from .models import *


@admin_only
def HomePage(request):
    return render(request,"index.html")


def employee_index(request):
    return render(request,"employee/index.html")


def profile(request):
    return render(request,"employee/profile_page.html")


@login_required(login_url="SignIn")
def AdminIndex(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='staff')
            user.groups.add(group) 
            messages.success(request,"User Registration Successful")
            return redirect("AdminIndex")
        else:
            messages.error(request,"Something went Wrong!!! Try To use password Includes (UPPERCASE, Numbers, Sepecial Characters and Minimum Legth 8  Characters) or User or email id Already Exists")
            return redirect("AdminIndex")
    context = {
        "form":form,
        
    }
    return render(request,"adminindex.html",context)

def VolunteerIndex(request):
    return render(request,"volunteerindex.html")

@unauthenticated_user
def SignIn(request):
    if request.method == "POST":
        uname = request.POST['uname']
        password = request.POST["pswd"]
        user = authenticate(request,username= uname, password = password)
        if user is not None:
            login(request,user)
            return redirect('HomePage')
        else:
            messages.error(request,"Username or Password Incorrect")
            return redirect('SignIn')
    return render(request,"login.html")

@unauthenticated_user
def SignUp(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Successful")
            return redirect("SignIn")
        else:
            messages.error(request,form.errors)
            return redirect("SignUp")
    
    context = {"form":form}
    return render(request,"register.html",context)


def SignOut(request):
    logout(request)
    return redirect("SignIn")


@login_required(login_url="SignIn")
def my_employees(request):
    users = CustomUser.objects.filter(is_superuser=False)
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.save()
            messages.success(request,"User Added Successfully")
            return redirect("my_employees")
        else:
            messages.error(request,form.errors)
            return redirect("my_employees")

    context = {
        "users":users,
        "form":form
    }
    return render(request,"my_employees.html",context)


def edit_employee(request,pk):
    employee = get_object_or_404(CustomUser,id=pk)
    form  = CustomUserChangeForm(instance=employee)
    if request.method == "POST":
        employee  = CustomUserChangeForm(request.POST, request.FILES, instance=employee)
        if employee.is_valid():
            employee.save()
            messages.success(request,"User Updated Successfully")
            return redirect("my_employees")
        else:
            messages.error(request,employee.errors)
            return redirect("edit_employee",pk)

    context = {
        "employee":employee,
        "form":form
    }    
    return render(request,"update_employee.html",context)

@login_required(login_url="SignIn")
def delete_employee(request,pk):
    if request.method == 'POST':
        user = CustomUser.objects.get(id=pk)
        user.profile_pic.delete()
        user.delete()
        messages.success(request,"User Deleted Successfully")
        return redirect("my_employees")


def attendance_sheet(request):
    employees = CustomUser.objects.all()
    return render(request,"attendance_sheet.html", context={"employees":employees})

from calendar import monthrange
from datetime import date, datetime
from django.shortcuts import render, get_object_or_404
from .models import Attendance, CustomUser

def employee_attendance_view(request, employee_id):
    # Get the employee object
    employee = get_object_or_404(CustomUser, id=employee_id)
    today = date.today()
    current_year = today.year

    # Fetch all attendance records for the employee for the current year
    attendance_records = Attendance.objects.filter(employee=employee, in_date_time__year=current_year)
    attendance_map = {att.in_date_time.date(): att for att in attendance_records}

    # Generate data for completed months in the current year
    months = []
    for month in range(1, today.month + 1):  # Loop through months up to the current month
        first_day, days_in_month = monthrange(current_year, month)  # Get weekday of the first day of the month
        weeks = []
        week = []

        # Add leading empty days if the month doesn't start on Sunday
        # We will use the 'first_day' value to determine which weekday the month starts on
        for _ in range(first_day):
            week.append(None)  # Add None for empty days at the start of the month

        # Loop through each day of the month and add it to the current week
        for day in range(1, days_in_month + 1):
            current_date = date(current_year, month, day)
            is_sunday = current_date.weekday() == 6  # Check if it's Sunday
            is_past_day = current_date < today  # Check if it's a past day

            # Use pre-fetched attendance data
            attendance = attendance_map.get(current_date)
            attendance_marked = attendance is not None
            attendance_status = attendance.attendance if attendance_marked else None

            # Add the day to the current week
            week.append({
                'date': day,
                'is_sunday': is_sunday,
                'attendance_marked': attendance_marked,
                'attendance_status': attendance_status,
                'is_past_day': is_past_day,
            })

            # If it's Sunday, or the last day of the month, push the week to weeks
            if is_sunday or day == days_in_month:
                weeks.append(week)
                week = []

        # Handle any leftover days in the last week
        if week:
            weeks.append(week)

        # Add the month data to the months list
        months.append({
            'name': datetime(current_year, month, 1).strftime('%B'),
            'weeks': weeks,
        })

    context = {
        'employee': employee,
        'months': months,
    }

    return render(request, 'attendance_view.html', context)



def messages_to_employees(request):
    form = MessagesToEmployeesForm()
    mess = Messages_to_employees.objects.all().order_by("-date")
    if request.method == "POST":
        message = request.POST.get("message")
        pmesages = PublicMessages(message=message)
        pmesages.save()
        messages.success(request,"Message Sent Successfully")
        return redirect("messages_to_employees")

    context = {
        "form":form,
        "mess":mess
    }
    return render(request,"messages_to_employees.html",context)

@login_required(login_url="SignIn")
def delete_message(request, pk):
   
    message = get_object_or_404(Messages_to_employees, id=pk)
    message.delete()
    messages.success(request, "Message Deleted Successfully")
    return redirect("messages_to_employees")

def sent_personal_message(request):
    if request.method == "POST":
        form = MessagesToEmployeesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Message Sent Successfully")
            return redirect("messages_to_employees")
    return redirect("messages_to_employees")


def employee_feedback(request):
    feedback = FeedBack.objects.all().order_by("-date")

    context = {"feedback":feedback}
    return render(request,"employee_feedback.html",context)


def salaries(request):
    form = SalariesForm()
    salary = Salaries.objects.all().order_by("-date")
    if request.method == "POST":
        form = SalariesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Salary Added Successfully")
            return redirect("salaries")
        else:
            messages.error(request,form.errors)
            return redirect("salaries")
        
    context = {
        "form":form,
        "salary":salary
    }
    return render(request,"salaries.html",context)

@login_required(login_url="SignIn")
def edit_salary(request, pk):
    salary = get_object_or_404(Salaries, id=pk)
    form = SalariesForm(instance=salary)
    if request.method == "POST":
        form = SalariesForm(request.POST, instance=salary)
        if form.is_valid():
            form.save()
            messages.success(request, "Salary Updated Successfully")
            return redirect("salaries")
        else:
            messages.error(request, form.errors)
            return redirect("edit_salary", pk=pk)

    context = {
        "form": form,
        "salary": salary
    }
    return render(request, "edit_salary.html", context)


@login_required(login_url="SignIn")
def delete_salary(request, pk):
    if request.method == 'POST':
        salary = get_object_or_404(Salaries, id=pk)
        salary.delete()
        messages.success(request, "Salary Deleted Successfully")
        return redirect("salaries")


@login_required(login_url="SignIn")
def leaves(request):
    form = LeaveForm()
    leaves = Leave.objects.all().order_by("-applied_on")
    if request.method == "POST":
        form = LeaveForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Leave Request Submitted Successfully")
            return redirect("leaves")
        else:
            messages.error(request, form.errors)
            return redirect("leaves")

    context = {
        "form": form,
        "leaves": leaves
    }
    return render(request, "leaves.html", context)

@login_required(login_url="SignIn")
def delete_leave(request, pk):
    
    leave = get_object_or_404(Leave, id=pk)
    leave.delete()
    messages.success(request, "Leave Request Deleted Successfully")
    return redirect("leaves")

@login_required(login_url="SignIn")
def view_leave(request, pk):
    leave = get_object_or_404(Leave, id=pk)
    context = {
        "leave": leave
    }
    return render(request, "view_leave.html", context)


@login_required(login_url="SignIn")
def approve_leave(request, pk):
    leave = get_object_or_404(Leave, id=pk)
    leave.status = 'Approved'
    leave.approved_on = datetime.now()
    leave.save()
    messages.success(request, "Leave Approved Successfully")
    return redirect("leaves")

@login_required(login_url="SignIn")
def reject_leave(request, pk):
    leave = get_object_or_404(Leave, id=pk)
    leave.status = 'Rejected'
    leave.save()
    messages.success(request, "Leave Rejected Successfully")
    return redirect("leaves")

from employee.models import Task, TaskUpdate
from employee.forms import TaskForm

@login_required(login_url="SignIn")
def assign_task(request):
    tasks = Task.objects.filter(manager=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.manager = request.user
            task.save()
            messages.success(request, "Task Assigned Successfully")
            return redirect("assign_task")
        else:
            messages.error(request, form.errors)
            return redirect("assign_task")
    else:
        form = TaskForm()
    
    context = {
        "form": form,
        "tasks":tasks
    }
    return render(request, "assign_task.html", context)


@login_required(login_url="SignIn")
def edit_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task Updated Successfully")
            return redirect("view_task", pk=pk)
        else:
            messages.error(request, form.errors)
            return redirect("edit_task", pk=pk)
    else:
        form = TaskForm(instance=task)
    
    context = {
        "form": form,
        "task": task
    }
    return render(request, "edit_task.html", context)

@login_required(login_url="SignIn")
def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk)

    task.delete()
    messages.success(request, "Task Deleted Successfully")
    return redirect("assign_task")
    
    

@login_required(login_url="SignIn")
def view_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    updates = TaskUpdate.objects.filter(task=task).order_by("-date")
    context = {
        "task": task,
        "updates": updates
    }
    return render(request, "view_task.html", context)


from django.shortcuts import render
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
import json

from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
def task_analytics(request):
    # Total tasks assigned to each employee
    tasks_by_employee = Task.objects.values('employee__username').annotate(total_tasks=Count('id'))

    # Total updates for each task
    updates_per_task = Task.objects.annotate(total_updates=Count('updates')).values('title', 'total_updates')

    # Tasks created over time (grouped by date)
    tasks_over_time = Task.objects.extra(select={'date_created': 'DATE(created_at)'}).values('date_created').annotate(total_tasks=Count('id')).order_by('date_created')

    # Serialize data to JSON
    context = {
        'tasks_by_employee': json.dumps(list(tasks_by_employee), cls=DjangoJSONEncoder),
        'updates_per_task': json.dumps(list(updates_per_task), cls=DjangoJSONEncoder),
        'tasks_over_time': json.dumps(list(tasks_over_time), cls=DjangoJSONEncoder),
    }
    return render(request, 'analytics.html', context)





