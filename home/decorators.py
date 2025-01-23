from django.http import HttpResponse
from django.shortcuts import redirect



#decorator for user redirect...............
def unauthenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('HomePage')
        else:
            return view_func(request,*args,**kwargs)
        
    return wrapper_func

# allowed user decorators................
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator

#decorators for user wise redirect pages...............
def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if not request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        if request.user.role == 'admin':   
            return view_func(request, *args, **kwargs)
        if request.user.role == 'manager':
            return view_func(request, *args, **kwargs)
        if request.user.role == 'employee':
            return redirect('employee_index')
        else:
            return redirect('employee_index')

        
    return wrapper_function

