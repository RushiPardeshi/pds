import re
from flask import redirect, url_for, session

date_pattern = "^\d{4}-\d{2}-\d{2}$"
input_string_format = "^[a-zA-Z0-9 .-]+$"
address_string_format = "^[a-zA-Z0-9 ,.-]+$"
integer_only = "^[0-9]+$"
zipcode_format = "^\d{5}$"
def validate_date_format(date):
    if re.match(date_pattern, date):
        return True
    else:
        return False
    

def validate_input_text_format(string):
    if re.match(input_string_format, string):
        return True
    else:
        return False
    
def validate_input_address_format(string):
    if re.match(address_string_format, string):
        return True
    else:
        return False
    
def validate_integer_text_format(id):
    if re.match(integer_only, id):
        return True
    else:
        return False
    

def validate_zipcode(zipcode):
    if re.match(zipcode_format, zipcode):
        return True
    else:
        return False