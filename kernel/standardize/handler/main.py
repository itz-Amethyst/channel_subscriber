import requests
from drf_standardized_errors.handler import ExceptionHandler

from kernel.standardize.exceptions import ServiceUnavailable


class MainExceptionHandler(ExceptionHandler):
    def convert_known_exceptions(self, exc: Exception) -> Exception:
        if isinstance(exc, requests.Timeout):
            return ServiceUnavailable()
        else:
            return super().convert_known_exceptions(exc)