import logging
from collections import defaultdict

from meiling.rule_engine import parsers
from meiling.rule_engine.exceptions import (
    InvalidConfig,
    UninitializedRuleStore,
)


log = logging.getLogger(__name__)


class RuleStore:
    def __init__(self):
        self.has_been_initialized = False

        self.groups_by_name = {}
        # Inverted index so we can quickly find which groups a user is a member of
        self.group_names_by_member = defaultdict(list)

        self.rules = []

    def load_config(self, raw_config):
        if 'groups' not in raw_config:
            raise InvalidConfig("'groups' not defined in config")

        if 'rules' not in raw_config:
            raise InvalidConfig("'rules' not defined in config")

        for raw_group in raw_config['groups']:
            group = parsers.parse_group(raw_group)
            self.groups_by_name[group.name] = group

            for member in group.members:
                self.group_names_by_member[member].append(group.name)

        for raw_rule in raw_config['rules']:
            rule = parsers.parse_rule(raw_rule)
            if rule.group not in self.groups_by_name:
                raise InvalidConfig("Rule defined for group '{0}', but no such group is defined".format(rule.group))

            self.rules.append(rule)

        log.info("Successfully loaded %d groups: %s", len(self.groups_by_name), ", ".join(self.groups_by_name.keys()))
        log.info("Successfully loaded %d rules", len(self.rules))

    def has_access(self, request_context: 'RequestContnext') -> bool:
        if not self.has_been_initialized:
            raise UninitializedRuleStore("Cannot use un-initialized rule store")

        pass
