import os

if os.environ.get("env", "dev") == "prod":
    from .prod import *
else:
    from .dev import *
