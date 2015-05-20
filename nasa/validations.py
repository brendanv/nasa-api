from functools import wraps
import datetime

def optional(validator):
    '''Mark a validation as optional (allow None)'''
    @wraps(validator)
    def wrapper(*args, **kwargs):
        value = args[0]
        return None if value is None else validator(*args, **kwargs)
    return wrapper

@optional
def optional_date(input):
    return nasa_date(input)

def nasa_date(input):
    try:
        datetime.datetime.strptime(input, '%Y-%m-%d')
        return input
    except ValueError:
        raise ValueError('Incorrect date format, should be YYYY-MM-DD')

@optional
def optional_int(input):
    return nasa_int(input)

def nasa_int(input):
    if isinstance(input, int):
        return input
    raise ValueError('Expected an int')

@optional
def optional_float(input):
    return nasa_float(input)

def nasa_float(input):
    if isinstance(input, float):
        return input
    raise ValueError('Expected a float')
