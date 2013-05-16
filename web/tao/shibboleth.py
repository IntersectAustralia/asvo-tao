from django.contrib import auth
from django.contrib.auth import load_backend, get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.middleware import get_user

class ShibbolethUserMiddleware(object):
    """
    Largely copy of RemoteUserMiddleware in Django, but we need more 
    attributes in auth.athenticate. Silly this cannot be implemented
    in subclasses :(
    """
    header = 'SHIB_auEdupersonSharedToken'

    def process_request(self, request):
        # MOSTLY SAME CODE AS IN RemoteuserMiddleware !!!
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class.")
        try:
            username = request.META[self.header]
        except KeyError:
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
        user = self.get_authenticated_user(username, request.META)
        # --

        if user:
            request.user = user
            auth.login(request, user)

    def clean_username(self, username, request):
        return username

    # -- And this would be the code in the subclass
    def get_authenticated_user(self, username, meta):
        try:
            attrs = dict([(field, meta['SHIB_'+field]) for field in ('email', 'givenName', 'surname')])
        except KeyError as e:
            raise ImproperlyConfigured("TAO does not have access to required shibboleth attributes: " + str(e))
        attrs.update({'username': username})
        return auth.authenticate(**attrs)

class ShibbolethUserBackend(ModelBackend):
    def authenticate(self, username=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        args = {UserModel.USERNAME_FIELD: username,
                'email': kwargs['email'],
                'first_name': kwargs['givenName'],
                'last_name': kwargs['surname']}
        user, created = UserModel.objects.get_or_create(**args)
        return user
