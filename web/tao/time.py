from django.utils.timezone import now, get_default_timezone

TIMESTAMP_FORMAT = "%Y-%m-%dT%T%z"

frozen_time = None

def timestamp():
    if frozen_time is None:
        time = now().astimezone(get_default_timezone())
    else:
        time = frozen_time
    return time.strftime(TIMESTAMP_FORMAT)
