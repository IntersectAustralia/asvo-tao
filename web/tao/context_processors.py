def add_tab_to_context(request):
    # to be used in conjunction with tao.decorators.set_tab
    tab = request.META.get('TAO-tab', '')
    return {'tab': tab}
