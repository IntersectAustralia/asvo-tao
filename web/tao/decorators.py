from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from functools import wraps

from django_rules.decorators import object_permission_required as django_rules_object_permission_required


def object_permission_required(*args, **kwargs):
    new_kwargs = {'redirect_url': reverse_lazy('tao.views.handle_403')}
    new_kwargs.update(kwargs)
    return django_rules_object_permission_required(*args, **new_kwargs)


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
