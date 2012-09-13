from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from functools import wraps


def researcher_required(func):
    return login_required(func)


def admin_required(func):
    return login_required(staff_member_required(func))


def set_tab(tab_name):
    def decorator_maker(fn):
        @wraps(fn)
        def decorator(request, *args, **kwargs):
            request.META['TAO-tab'] = tab_name
            return fn(request, *args, **kwargs)

        return decorator
    return decorator_maker
