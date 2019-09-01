"""Config file that contains the configuration dictionary"""

import math
import logging

# Config dictionary
config = {
    "screen": {
        "dimensions": (400, 400),
        "focal": 200,
        # Black background
        "color": (0, 0, 0),
        # Window title
        "name": "Model",
    },
    "ui": {
        "panSpeed": 5,
        "rotateSpeed": math.pi/90,
    },
    "app": {
        "tps": 60,
    },
    "logging": {
        "level": logging.WARNING,
    },
}
