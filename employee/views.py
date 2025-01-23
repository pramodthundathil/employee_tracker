from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib import messages
from home.models import *
from home.forms import *
from calendar import monthrange
from datetime import date, datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa
from .models import *
from .forms import *
# Create your views here.

def mark_attendance_sheet(request):
    employee = request.user
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
    return render(request, 'employee/attendance_sheet.html',context)


@login_required(login_url='SignIn')
def mark_attendance(request):
    today = date.today()
    attendance_exists = Attendance.objects.filter(employee=request.user, in_date_time__date=today).exists()

    if attendance_exists:
        messages.warning(request, 'Attendance already marked for today')
        return redirect('mark_attendance_sheet')
    else:
        attendance  = Attendance.objects.create(attendance_marked=True,attendance_status=True,attendance="Present",employee=request.user)
        attendance.save()
        messages.success(request, 'Attendance marked successfully')
        return redirect('mark_attendance_sheet')

def messages_from_employer(request):
    employee = request.user
    messages = Messages_to_employees.objects.filter(employee=employee).order_by('-date')
    context = {
        'mess': messages,
    }
    return render(request, 'employee/messages_from_employer.html',context)

def my_feedback(request):
    # Logic for displaying feedback
    form = FeedBackForm()
    feedbacks = FeedBack.objects.filter(employee=request.user).order_by('-date')
    if request.method == 'POST':
        form = FeedBackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.employee = request.user
            feedback.save()
            messages.success(request, 'Feedback sent successfully')
            return redirect('my_feedback')
        else:
            messages.error(request, 'An error occurred. Please try again.')
            return redirect('my_feedback')
    context = {
        'form': form,
        "feedbacks":feedbacks
    }

    return render(request, 'employee/my_feedback.html', context)

def delete_feedback(request, feedback_id):
    feedback = get_object_or_404(FeedBack, id=feedback_id, employee=request.user)
    feedback.delete()
    messages.success(request, 'Feedback deleted successfully')
    return redirect('my_feedback')
    

def my_salaries(request):
    # Logic for displaying salaries
    salaries  = Salaries.objects.filter(employee=request.user).order_by('-date')
    return render(request, 'employee/my_salaries.html',{"salaries":salaries})

def download_salary_slip(request, salary_id):
    # Fetch employee and their salary details
    employee = request.user
    latest_salary = Salaries.objects.get(id =salary_id) # Fetch latest salary first

    # Use the latest salary record

    # Render HTML content for the PDF
    html_content = render_to_string('employee/salary_slip.html', {
        'employee': employee,
        'salary': latest_salary,
    })
# Render HTML content for the PDF
    html_content = render_to_string('employee/salary_slip.html', {
        'employee': employee,
        'salary': latest_salary,
    })

    # Create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="salary_slip_{employee.id}.pdf"'
    pisa_status = pisa.CreatePDF(BytesIO(html_content.encode('utf-8')), dest=response, encoding='utf-8')

    # Check for errors
    if pisa_status.err:
        return HttpResponse(f'Error generating PDF: {pisa_status.err}')

    return response

def my_leaves(request):
    form = LeaveForm()
    leaves = Leave.objects.filter(employee=request.user).order_by('-start_date')
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user
            leave.save()
            messages.success(request, 'Leave application submitted successfully')
            return redirect('my_leaves')
        else:
            messages.error(request, 'An error occurred. Please try again.')
            return redirect('my_leaves')

    context = {
        'form': form,
        'leaves': leaves,
    }
    return render(request, 'employee/my_leaves.html',context)


def delete_leave_employee(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id, employee=request.user)
    leave.delete()
    messages.success(request, 'Leave deleted successfully')
    return redirect('my_leaves')

def my_tasks(request):
    tasks = Task.objects.filter(employee=request.user).order_by('-updated_at')

    context = {
        "tasks": tasks,
    }
    return render(request, 'employee/my_tasks.html',context)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Task, TaskUpdate
from .forms import TaskUpdateForm

def view_tasks(request, task_id):
    # Fetch the task assigned to the logged-in user
    task = get_object_or_404(Task, id=task_id, employee=request.user)

    if request.method == 'POST':
        # Create a new TaskUpdate instance without binding it to a specific instance
        form = TaskUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            # Create the TaskUpdate object but don't save it to the database yet
            update = form.save(commit=False)
            # Associate the update with the current task
            update.task = task
            update.save()
            messages.success(request, 'Task status updated successfully')
            return redirect('view_tasks', task_id=task_id)
        else:
            messages.error(request, 'An error occurred. Please try again.')
    else:
        # Empty form for creating a new TaskUpdate
        form = TaskUpdateForm()

    context = {
        'form': form,
        'task': task,
    }
    return render(request, 'employee/view_tasks.html', context)

