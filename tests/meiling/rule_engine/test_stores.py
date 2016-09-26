from unittest import mock

import pytest

from meiling.rule_engine import (
    exceptions,
    models,
    stores,
)


@pytest.fixture
def basic_store():
    store = stores.RuleStore()
    store.load_config({
        'groups': [
            {
                'name': 'admin',
                'members': [
                    'yamaxanadu@example.com',
                ],
            },
            {
                'name': 'silly-cirno',
                'members': [
                    'cirno@example.com',
                ],
            },
        ],
        'rules': [
            {
                'host': '.*',
                'request_method': '.*',
                'request_uri': '.*',
                'group': 'admin',
                'allow': True,
            },
            {
                'host': 'gensokyo.local',
                'request_method': '.*',
                'request_uri': '.*',
                'group': 'silly-cirno',
                'allow': False,
            },
        ],
    })
    return store


def test_loading_empty_config_is_ok():
    store = stores.RuleStore()
    store.load_config({
        'groups': [],
        'rules': [],
    })
    assert store.has_been_initialized
    assert store.rules == []


def test_loading_rule_with_nonexistent_group_errors():
    store = stores.RuleStore()
    config_with_nonexistent_group = {
        'groups': [],
        'rules': [
            {
                'host': '.*',
                'request_method': '.*',
                'request_uri': '.*',
                'group': 'nonexistent',
                'allow': True,
            }
        ],
    }

    with pytest.raises(exceptions.InvalidConfig):
        store.load_config(config_with_nonexistent_group)


def test_loading_group_with_no_rules_is_ok():
    store = stores.RuleStore()
    store.load_config({
        'groups': [
            {
                'name': 'akbs',
                'members': [
                    'mariko@example.com',
                ]
            },
        ],
        'rules': [],
    })
    assert store.has_been_initialized
    assert store.rules == []


def test_uninitialized_rule_store_raises_exception():
    store = stores.RuleStore()

    with pytest.raises(exceptions.UninitializedRuleStore):
        store.has_access(mock.Mock())


def test_user_not_in_rule_group_does_not_get_access(basic_store: stores.RuleStore):
    request = models.RequestContext(
        user_email='reimu@example.com',
        host='gensokyo.local',
        request_method='GET',
        request_uri='/',
    )
    assert not basic_store.has_access(request)


def test_user_allowed_by_rules_has_access(basic_store: stores.RuleStore):
    request = models.RequestContext(
        user_email='yamaxanadu@example.com',
        host='gensokyo.local',
        request_method='GET',
        request_uri='/',
    )
    assert basic_store.has_access(request)


def test_user_blocked_by_rules_does_not_have_access(basic_store: stores.RuleStore):
    request = models.RequestContext(
        user_email='cirno@example.com',
        host='gensokyo.local',
        request_method='GET',
        request_uri='/',
    )
    assert not basic_store.has_access(request)
