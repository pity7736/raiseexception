import re

USER_REGEX = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`"
    r"{}|~0-9A-Z]+)*\Z"
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"\Z)',  # noqa: E501
    re.IGNORECASE
)
DOMAIN_REGEX = re.compile(
    r'((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+)(?:[A-Z0-9-]{2,63}(?<!-))\Z',  # noqa: E501
    re.IGNORECASE
)


def validate_email(value: str):
    if '@' not in value:
        raise ValueError('wrong email')
    user, domain = value.rsplit('@', 1)
    if not USER_REGEX.match(user) or not DOMAIN_REGEX.match(domain):
        raise ValueError('wrong email')
