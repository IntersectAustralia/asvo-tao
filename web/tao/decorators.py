from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

def researcher_required(func):
    return login_required(func)

def admin_required(func):
    return login_required(staff_member_required(func))
