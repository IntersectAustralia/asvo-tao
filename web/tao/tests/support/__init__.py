import datetime

def stripped_joined_lines(string):
    return ''.join([line.strip() for line in string.split('\n')])

class UtcPlusTen(datetime.tzinfo):
    """ timezone UTC+10 """
    def utcoffset(self, dt):
        return datetime.timedelta(hours=10)

    def tzname(self, dt):
        return 'UTC+10'

    def dst(self, dt):
        return datetime.timedelta(0)