import src.config as config
import logging as log

def check_int(**kwargs):
    """Function to check if the field is an integer and convert if necessary"""
    int_check = isinstance(kwargs['val'], int)
    val = kwargs['val']
    if int_check == False:
        try:
            val = int(kwargs['val'])
        except Exception as e:
            val = None
            log.error('Unable to convert %s to an integer due to error %s' %
                    (val, e))
    return val

def check_varchar(**kwargs):
    """Function to check if the field is the correct length and trunctuate if necessary"""
    val = kwargs['val']
    try:
        cleaned_val = str(val)[0:kwargs['length']]
    except Exception as e:
        log.error('Unable to convert %s to a string due to error %s' %
                (val, e))
        cleaned_val = None
    return cleaned_val

def check_char(**kwargs):
    """Function to check if the field is the correct length and trunctuate if necessary
        Also checks if it is a string and converts if necessary.
    """

    val = kwargs['val']
    str_check = isinstance(kwargs['val'], str)
    val = kwargs['val']
    if str_check == False:
        try:
            val = str(kwargs['val'])
        except Exception as e:
            log.error('Unable to convert %s to a string due to error %s' %
                    (val, e))
            return None
    cleaned_val = val[0:kwargs['length']]
    return cleaned_val

def check_date(**kwargs):
    """Function to extract the date from the zulu time string"""
    try:
        val = kwargs['val']
        cleaned_val = val[0:10]
    except Exception as e:
        cleaned_val = None
        log.error('Unable to parse date from %s due to error %s' (val, e))
    return cleaned_val

def get_coords(**kwargs):
    """Function to extract the lat/lon coordinates"""
    try:
        val = kwargs['val']
        cleaned_val = [float(val[0]), float(val[1])]
    except Exception as e:
        cleaned_val = None
        log.error('Unable to parse coords from %s due to error %s' % (val, e))
    return cleaned_val


def get_property_type(**kwargs):
    """Function to extract the property type from the Undefined list in the
    json response"""
    try:
        vals = kwargs['val']
        for v in vals:
            if v in config.PROPERTY_TYPES:
                return v
        log.error('No property type found in %s' % vals)
    except Exception as e:
        log.error('Unable to get property type from %s due to error %s'
                % (vals, e))
    return 'Other'
