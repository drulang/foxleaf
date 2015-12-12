import random
import string
from functools import partial
import json
import re

from django.http import HttpResponse


OK = "OK"
ERR = "ERR"

def err_resp(message, debug=None):
    return {
       "status": "ERR",
       "message": message,
       "debug": debug,
    }

def random_string(length=10):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(length))


def group_into_groups_of(group_count, the_list):
    groups = []
    current_group = [] 
    for item in the_list:
        if len(current_group) == group_count:
            groups.append(current_group)
            current_group = [item]
        else:
            current_group.append(item)

    groups.append(current_group)
    return groups

def divide_into_columns(number_columns, the_list):
    return_list = []

    # Create initial columns
    for i in range(number_columns):
        return_list.append([])

    # Divide data
    for idx, item in enumerate(the_list):
        col = idx % number_columns
        return_list[col].append(item)

    return return_list

def string_to_url(string):
    return re.sub(r'\W+', '-', string)

def json_response(data):
    return HttpResponse(json.dumps(data), content_type="application/json")
