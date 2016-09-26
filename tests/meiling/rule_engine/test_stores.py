import pytest

from meiling.rule_engine import (
    exceptions,
    stores,
)


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
