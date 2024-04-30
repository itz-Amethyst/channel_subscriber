try:
    from kernel.settings.production.configs import *
except ImportError:
    pass
from .settings import *
