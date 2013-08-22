from django.conf import settings
from django.contrib import auth
from django.contrib.auth import load_backend, get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured
import logging

logger = logging.getLogger(__name__)

_FIELDS = {'username': settings.AAF_USERNAME, 'email': settings.AAF_EMAIL, 'first_name': settings.AAF_FIRST_NAME, 'last_name': settings.AAF_LAST_NAME}
_USERNAME = _FIELDS['username']
_COOKIE_PREFIX = settings.AAF_COOKIE_PREFIX
_INVALID_AAF = 'INVALID_AAF'

class ShibbolethUserMiddleware(object):
    """
    Largely copy of RemoteUserMiddleware in Django, but we need more 
    attributes in auth.athenticate. Silly this cannot be implemented
    in subclasses :(
    """

    def process_request(self, request):
        # MOSTLY SAME CODE AS IN RemoteuserMiddleware !!!
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class.")
        # -- instead of try/except, we should ask the instance
        username = self.process_username(request)
        if not username:
            if request.user.is_authenticated():
                try:
                    stored_backend = load_backend(request.session.get(
                        auth.BACKEND_SESSION_KEY, ''))
                    if isinstance(stored_backend, ShibbolethUserBackend):
                        auth.logout(request)
                except ImproperlyConfigured as e:
                    auth.logout(request)
            return
        if request.user.is_authenticated():
            if request.user.get_username() == self.clean_username(username, request):
                return

        # -- this is how it should be
        user = self.get_authenticated_user(username, request)
        # --

        if user:
            request.user = user
            auth.login(request, user)

    def clean_username(self, username, request):
        return username

    # -- And this would be the code in the subclass
    def get_authenticated_user(self, username, request):
        attrs = {}
        for field in _FIELDS:
            try:
                attrs[field] = request.META[_FIELDS[field]]
            except KeyError:
                attrs[field] = ''
                username = _INVALID_AAF
        attrs.update({'username': username, '_IS_AAF_': True})
        return auth.authenticate(**attrs)

    def process_username(self, request):
        if not hasattr(request, 'COOKIES'): return False
        if not hasattr(request, 'META'): return False
        if not any([name.startswith(_COOKIE_PREFIX) for name in request.COOKIES]): return False
        if not _USERNAME in request.META: return _INVALID_AAF
        return request.META[_USERNAME]
         

class ShibbolethUserBackend(ModelBackend):
    def authenticate(self, **kwargs):
        if not '_IS_AAF_' in kwargs: return None
        username = kwargs.get('username')
        UserModel = get_user_model()
        user, created = UserModel.objects.get_or_create(**{"username": username})
        if _INVALID_AAF == username:
            if created:
                user.aaf_shared_token = username
                user.first_name = 'Unknown'
                user.last_name = 'Unknown'
                user.email = ''
                user.reject_user('The application could not access your description in the AAF. You need to authorise access to your basic information')
                user.save()
        elif created:
            user.email = kwargs['email']
            user.first_name = kwargs['first_name']
            user.last_name = kwargs['last_name']
            user.aaf_shared_token = username
            user.account_registration_status = UserModel.RS_EMPTY
            user.is_active = False
            user.is_rejected = False
            user.save()
        elif kwargs['email'] != user.email or kwargs['first_name'] != user.first_name or kwargs['last_name'] != user.last_name:
            user.email = kwargs['email']
            user.first_name = kwargs['first_name']
            user.last_name = kwargs['last_name']
            user.save()
        return user
