def format_location(raw_location):
    if raw_location.endswith('/'):
        return raw_location
    else:
        return raw_location + '/'
