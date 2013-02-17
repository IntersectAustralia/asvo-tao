"""
===========================
tao.context_processors
===========================
"""

def add_tab_to_context(request):
    """
    to be used in conjunction with :func:`tao.decorators.set_tab`.

    :param request: web request
    :return:
    """
    tab = request.META.get('TAO-tab', '')
    return {'tab': tab}
