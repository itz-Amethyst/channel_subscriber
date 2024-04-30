from kernel.settings.config.setup import env
# Should be imported
from kernel.settings.third_party import *

# Determine project status (Development or Production)
project_status = env("PROJECT_STATUS")

match project_status:
    case "Development":
        print("DEV")
        # Note in fist run it will run this script 2 times and then when you apply changes and hot reload it will change back to normal
        from kernel.settings.development import *
        # print(settings.ROOT_URLCONF)
    case "Production":
        print("PRO")
        from kernel.settings.production import *
    case _:
        raise ValueError("Invalid PROJECT_STATUS value in .env file")