from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Middleware to add security-related HTTP headers to responses.
    """

    def __init__(self, get_response: callable) -> None:
        """
        Initialize the middleware.

        Args:
            get_response (callable): The next middleware or view function in the chain.
        """
        super().__init__(get_response)

        # Define security-related headers with their default values
        self.headers: dict = {
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Handle the incoming request and add security-related headers to the response.

        Args:
            request (HttpRequest): The incoming request object.

        Returns:
            HttpResponse: The response object with security-related headers added.
        """
        response: HttpResponse = self.get_response(request)

        # Add security-related headers to the response
        for header, value in self.headers.items():
            response[header] = value

        return response
