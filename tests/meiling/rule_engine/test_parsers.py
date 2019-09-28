import pytest
import re

from meiling.rule_engine import (
    exceptions,
    parsers,
)


@pytest.fixture(scope='function')
def group_data():
    return {
        'name': 'touhous',
        'members': [
            'kaguya@gmail.com',
            'reimu@gmail.com',
        ]
    }


@pytest.fixture(scope='function')
def rule_data():
    return {
        'host': '^(plex|grafana).misaka.hanekawa.net$',
        'request_method': '.*',
        'request_uri': '.*',
        'group': 'touhous',
        'allow': True,
    }


def test_missing_name_in_group_errors(group_data):
    del group_data['name']
    with pytest.raises(exceptions.InvalidConfig):
        parsers.parse_group(group_data)


def test_missing_members_in_group_errors(group_data):
    del group_data['members']
    with pytest.raises(exceptions.InvalidConfig):
        parsers.parse_group(group_data)


def test_normal_group_parses_ok(group_data):
    group = parsers.parse_group(group_data)

    assert group.name == group_data['name']
    assert group.members == group_data['members']


@pytest.mark.parametrize("missing_key", [
    "host",
    "request_method",
    "request_uri",
    "group",
    "allow",
])
def test_missing_key_in_rule_errors(rule_data, missing_key):
    del rule_data[missing_key]
    with pytest.raises(exceptions.InvalidConfig):
        parsers.parse_rule(rule_data)


def test_normal_rule_parses_ok(rule_data):
    rule = parsers.parse_rule(rule_data)

    # Do a comparison on the literals that should stay the same after parsing
    assert rule.group == rule_data['group']
    assert rule.allow == rule_data['allow']

    for regex_name in ['host', 'request_method', 'request_uri']:
        assert isinstance(getattr(rule, regex_name), re.Pattern)
