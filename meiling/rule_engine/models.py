import re

from typing import (
    List,
    NamedTuple,
)


class RequestContext(NamedTuple):
    # The e-mail address of the user sending the request.
    user_email: str
    # The hostname of the original request
    host: str
    # The method of the original request
    request_method: str
    # The full URI of the original request. Ex: `/`, `/foo`
    request_uri: str


class UserGroup(NamedTuple):
    name: str
    members: List[str]


class AccessRule(NamedTuple):
    host: re.Pattern
    request_method: re.Pattern
    request_uri: re.Pattern
    group: str
    allow: bool
