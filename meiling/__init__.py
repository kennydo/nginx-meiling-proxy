import os
import logging
from typing import (
    Any,
    Dict,
)

import toml
from flask import Flask

from meiling.rule_engine.store import RuleStore

log = logging.getLogger(__name__)

MEILING_CONFIG_ENV_VAR_NAME = 'MEILING_CONFIG'

rule_db = RuleStore()


def load_config_from_env_var_path(env_var_name: str) -> Dict[str, Any]:
    if env_var_name not in os.environ:
        log.info("Environment variable '%s' not defined", env_var_name)
        raise ValueError("Config must be loaded from file specified in env var {0}".format(env_var_name))

    config_path = os.environ[env_var_name]
    if not os.path.isfile(config_path):
        raise ValueError("Could not load config from {0} because no such file exists".format(config_path))

    with open(config_path) as f:
        return toml.load(f)


def create_app() -> Flask:
    app = Flask(__name__)

    config_from_env_var = load_config_from_env_var_path(MEILING_CONFIG_ENV_VAR_NAME)
    app.config.update(config_from_env_var)

    if 'logging' in app.config:
        logging.config.dictConfig(app.config['logging'])

    if 'rule_store' not in app.config:
        raise ValueError('Config did not define any rules')

    rule_db.load_config(app.config['rule_store'])

    @app.route('/')
    def index():
        return 'OK'

    from meiling.oauth import oauth_bp

    app.register_blueprint(oauth_bp, url_prefix='/oauth')

    return app
