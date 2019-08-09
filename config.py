"""Config file that contains the configuration dictionary"""

import logging

# Config dictionary
config = {
    "screen": {
        "dimensions": (400, 400),
        # Black background
        "color": (0, 0, 0),
        # Window title
        "name": "Model",
    },
    "app": {
        "tps": 60,
    },
    "logging": {
        "level": logging.WARNING,
    },
}
