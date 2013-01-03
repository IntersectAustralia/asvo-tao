from django.shortcuts import render


def asset_handler(request, path):
    content_type = 'text/plain'
    content_type = _detect_content_type(path)
    return render(request, 'assets/%s' % path, content_type=content_type)


def _detect_content_type(path):
    if path.startswith('js/'):
        content_type = 'application/javascript'
    elif path.startswith('css/'):
        content_type = 'text/css'
    else:
        content_type = 'text/plain'
    return content_type
