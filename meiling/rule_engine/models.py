import re

from typing import (
    List,
    NamedTuple,
)


RequestContext = NamedTuple('RequestContext', [
    # The e-mail address of the user sending the request.
    ('user_email', str),
    # The hostname of the original request
    ('host', str),
    # The method of the original request
    ('request_method', str),
    # The full URI of the original request. Ex: `/`, `/foo`
    ('request_uri', str),
])


UserGroup = NamedTuple('UserGroup', [
    ('name', str),
    ('members', List[str]),
])


AccessRule = NamedTuple('AccessRule', [
    ('host', re._pattern_type),
    ('request_method', re._pattern_type),
    ('request_uri', re._pattern_type),
    ('group', str),
    ('allow', bool),
])