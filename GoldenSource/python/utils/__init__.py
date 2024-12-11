import re

def camelcase_to_underscore(s):

    return camelcase_to_underscore.pattern.sub(r'_\1', s).lower()

camelcase_to_underscore.pattern = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')