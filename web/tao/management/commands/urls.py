from django.core.management.base import BaseCommand, CommandError

def show_urls(urllist, depth=0):
    for entry in urllist:
        if hasattr(entry, 'name') and entry.name:
            print "  " * depth, entry.regex.pattern, '(Name:', entry.name, ')'
        else:
            print "  " * depth, entry.regex.pattern
        if hasattr(entry, 'url_patterns'):
            show_urls(entry.url_patterns, depth + 1)

class Command(BaseCommand):
    def handle(self, *args, **options):
        from tao import urls
        show_urls(urls.urlpatterns)



