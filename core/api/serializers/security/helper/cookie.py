from django.conf import settings
from django.http import HttpResponse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

def create_cookie(response, token):
    """Create a cookie with the provided token."""
    try:
        # Create AccessToken object from the token
        access_token = AccessToken(token)

        # Retrieve cookie settings from Django settings
        cookie_name = getattr(settings, 'COOKIE_NAME', 'jwt_cookie')
        cookie_max_age = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
        cookie_same_site = getattr(settings, 'COOKIE_SAMESITE', None)

        # Set the cookie on the response
        response.set_cookie(
            cookie_name,
            str(access_token),
            max_age=cookie_max_age,
            httponly=True,
            secure=True,
            samesite=cookie_same_site
        )
    except Exception as e:
        # Log the error if needed
        print(f"An error occurred while creating the cookie: {e}")
        raise ValueError("Unable to create cookie")

def delete_cookie(request, response):
    """Delete the cookie."""
    try:
        # Retrieve cookie name from Django settings
        cookie_name = getattr(settings , 'COOKIE_NAME' , 'jwt_cookie')

        # Retrieve cookies from the request
        cookies = request.META.get('HTTP_COOKIE' , '')
        cookie_list = cookies.split('; ')

        # Iterate through cookies to find the one with the specified name
        for cookie in cookie_list:
            if cookie.startswith(cookie_name):
                # Create a response object to delete the cookie
                response = HttpResponse()
                response.delete_cookie(cookie_name)
                return response

        # If the cookie is not found, return an empty response
        return HttpResponse(status = status.HTTP_204_NO_CONTENT)
    except Exception as e:
        # Log the error if needed
        print(f"An error occurred while deleting the cookie: {e}")
        raise ValueError("Unable to delete cookie")
