from core.errors.client.main import all_client_errors
from core.errors.external.main import all_external_errors
all_errors = all_client_errors | all_external_errors