"""
==================
tao.decorators
==================
"""
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse_lazy
from functools import wraps
from tao.models import TaoUser

from django_rules.decorators import object_permission_required as django_rules_object_permission_required


def object_permission_required(*args, **kwargs):
    new_kwargs = {'redirect_url': reverse_lazy('tao.views.handle_403')}
    new_kwargs.update(kwargs)
    return django_rules_object_permission_required(*args, **new_kwargs)

def aaf_active_or_else_required(function):
    """
    check that, if the user logged in via AAF, it is approved
    """
    login_url = reverse_lazy('tao.views.register')
    actual_decorator = user_passes_test(
        lambda u: u.account_registration_status in [TaoUser.RS_NA, TaoUser.RS_APPROVED],
        login_url=login_url,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def researcher_required(func):
    return login_required(aaf_active_or_else_required(func))

def admin_required(func):
    ## return login_required(staff_member_required(func))
    return login_required(aaf_active_or_else_required(staff_member_required(func)))


def set_tab(tab_name):
    """
    Decorator for menu tabs

    :param tab_name:
    :return:
    """
    def decorator_maker(fn):
        @wraps(fn)
        def decorator(request, *args, **kwargs):
            request.META['TAO-tab'] = tab_name
            return fn(request, *args, **kwargs)

        return decorator
    return decorator_maker
