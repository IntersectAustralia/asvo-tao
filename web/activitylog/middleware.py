import time
import json
import logging

from django.core.exceptions import ObjectDoesNotExist

from activitylog.models import ActivityRecord
from django.conf import settings

logger = logging.getLogger(__name__)

class ActivityLogMiddleware(object):

    def process_request(self,request):
        # Only log requests of authinticate users                                                                                                                                                               
        try:
            if not request.user.is_authenticated():
                return None
        except AttributeError:
            return None

        # Skip favicon requests cause I do not care about them
        if request.path =="/favicon.ico":
            return None

        newRecord = ActivityRecord(
            created_at = str(time.time()),
            session_id = request.session.session_key,

            request_user = request.user,
            request_path  = request.path,
            request_query_string = request.META["QUERY_STRING"],
            request_vars = json.dumps(request.REQUEST.__dict__),
            request_method = request.method,
            request_secure = request.is_secure(),
            request_ajax = request.is_ajax(),
            request_meta = request.META.__str__(),
            request_address = request.META["REMOTE_ADDR"],
            )

        newRecord.save()

        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if not request.user.is_authenticated():
                return None
        except AttributeError:
            return None

        # Fix the issue with the authorization request                                                                                                                                                        
        try:
            theRecord  = ActivityRecord.objects.get(
                session_id = request.session.session_key,
                request_user = request.user,
                request_path  = request.path,
                request_method = request.method,
                request_secure = request.is_secure(),
                request_ajax = request.is_ajax(),
                request_meta = request.META.__str__()
                )
            theRecord.view_function = view_func.func_name
            theRecord.view_doc_string = view_func.func_doc
            theRecord.view_args = json.dumps(view_kwargs)

            theRecord.save()
        except  ObjectDoesNotExist:
            logger.debug('failed to find record when processing view')
            pass

        return None


    def process_response(self, request, response):

        # Only log autherized requests
        try:
            if not request.user.is_authenticated():
                return response
        except AttributeError:
            return response

        # Skip favicon requests cause I do not care about them
        if request.path =="/favicon.ico":
            return response


        # Fix the issue with the authorization request                                                                                                                                                                          
        try:
            theRecord  = ActivityRecord.objects.get(
                session_id = request.session.session_key,
                request_user = request.user,
                request_path  = request.path,
                request_method = request.method,
                request_secure = request.is_secure(),
                request_ajax = request.is_ajax(),
                request_meta = request.META.__str__()
                )

            theRecord.response_code = response.status_code

            # Decide what, if anything, from the response to log
            if settings.ACTIVITYLOG_LOG_RESPONSE:
                if settings.ACTIVITYLOG_LOG_HTML_RESPONSE:
                    # IF set to true then log the response regardless                                                                                                                                                               
                    theRecord.response_content = response.content
                elif response.content.startswith(settings.ACTIVITYLOG_HTML_START):
                    theRecord.response_content = "FULL HTML RESPONSE"
                else:
                    theRecord.response_content = response.content

            theRecord.save()

        except  ObjectDoesNotExist:
            logger.debug('failed to find record when processing response')
            pass

        return response
