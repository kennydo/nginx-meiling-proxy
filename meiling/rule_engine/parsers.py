import re
from typing import (
    Any,
    Dict,
    List,
)

from meiling.rule_engine import models
from meiling.rule_engine.exceptions import InvalidConfig


def _require_keys_in_dict(required_keys: List[str], name: str, data: Dict[str, Any]) -> None:
    for key in required_keys:
        if key not in data:
            raise InvalidConfig("{0} must have a '{1}' defined".format(name, key))


def parse_group(raw_group: Dict[str, Any]) -> models.UserGroup:
    required_keys = ['name', 'members']
    _require_keys_in_dict(required_keys, "Group", raw_group)

    if not isinstance(raw_group['name'], str):
        raise InvalidConfig("Group's 'name' must be a string: {0}".format(raw_group['name']))

    if not isinstance(raw_group['members'], list):
        raise InvalidConfig("Group's 'members' must be a list: {0}".format(raw_group['members']))

    return models.UserGroup(
        name=raw_group['name'],
        members=raw_group['members'],
    )


def parse_rule(raw_rule: Dict[str, Any]) -> models.AccessRule:
    required_keys = [
        'host',
        'request_method',
        'request_uri',
        'group',
        'allow',
    ]
    _require_keys_in_dict(required_keys, "Rule", raw_rule)

    if not isinstance(raw_rule['allow'], bool):
        raise InvalidConfig("Rule 'allow' value must be a bool: {0}".format(raw_rule['allow']))

    return models.AccessRule(
        host=re.compile(raw_rule['host']),
        request_method=re.compile(raw_rule['request_method']),
        request_uri=re.compile(raw_rule['request_uri']),
        group=raw_rule['group'],
        allow=raw_rule['allow'],
    )
