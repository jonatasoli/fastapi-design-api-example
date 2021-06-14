import re


def camelcase_to_snakecase(value):
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    return pattern.sub("_", value).lower()
