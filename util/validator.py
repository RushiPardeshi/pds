import common
import re

def validate_date_format(date):
    if re.match(common.date_pattern, date):
        return True
    else:
        return False
    

def validate_input_text_format(string):
    if re.match(common.input_string_format, string):
        return True
    else:
        return False
    
def validate_input_address_format(string):
    if re.match(common.address_string_format, string):
        return True
    else:
        return False
    
def validate_integer_text_format(id):
    if re.match(common.integer_only, id):
        return True
    else:
        return False
    

def validate_zipcode(zipcode):
    if re.match(common.zipcode_format, zipcode):
        return True
    else:
        return False