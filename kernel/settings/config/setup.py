from pathlib import Path

import environ
# Load environment variables
env = environ.Env()
BASE_DIR = Path(__file__).resolve().parents[3]
BASE_DIR_FOR_UPLOAD = Path(__file__).resolve().parents[4]
env_file = BASE_DIR / '.env'
environ.Env.read_env(env_file)