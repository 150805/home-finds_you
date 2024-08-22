from django.shortcuts import redirect

def login_required(function):
    def wrap(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login')
        return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap