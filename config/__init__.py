"""
load default config and overwrite with
environment variable.
"""

import os
from .default import default_config

CONFIG = default_config

for key in default_config.keys():
    if key in os.environ:
        env_option = os.environ.get(key)
        origin_type = type(default_config.get(key))
        CONFIG[key] = origin_type(env_option)
