from django.db import models
from django.conf import settings

class ActivityRecord(models.Model):
    """
    Basic log record describing all user interaction with the UI.
    Will be propagated by a middle ware.
    This will be one BIG DB table!
    """
    created_at = models.DateTimeField(auto_now_add = True)
    session_id = models.CharField(max_length=256)

    request_user = models.ForeignKey(settings.AUTH_USER_MODEL)
    request_path  = models.TextField()
    request_query_string = models.TextField()
    request_vars = models.TextField()
    request_method = models.CharField(max_length=4)
    request_secure = models.BooleanField(default=False)
    request_ajax = models.BooleanField(default=False)
    request_meta = models.TextField(null=True, blank=True)
    request_address = models.IPAddressField()

    view_function = models.CharField(max_length=256)
    view_doc_string = models.TextField(null=True, blank=True)
    view_args = models.TextField()

    response_code = models.CharField(max_length=3)
    response_content = models.TextField(null=True, blank=True)
