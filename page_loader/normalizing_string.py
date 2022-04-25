import re


def normalize_string(string):
    string_name = re.sub('[^a-z0-9]', '-', string)
    return string_name
