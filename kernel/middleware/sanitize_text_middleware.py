from django.db.models import Model
from django.db.models.fields import TextField
from django.utils.html import mark_safe
from django.utils.deprecation import MiddlewareMixin
import bleach

class SanitizeTextFieldMiddleware(MiddlewareMixin):
    """
    Middleware to sanitize text in TextField fields to prevent XSS attacks.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Handle the incoming request and sanitize text in TextField fields.

        Args:
            request: The incoming request object.

        Returns:
            Response: The response object.
        """
        response = self.get_response(request)

        # Process model instances in response
        if isinstance(response, Model):
            self.process_model_instance(response)
        elif hasattr(response, '__iter__') and not isinstance(response, (str, bytes)):
            for instance in response:
                if isinstance(instance, Model):
                    self.process_model_instance(instance)

        return response

    def process_model_instance(self, instance):
        """
        Sanitize text in TextField fields of a model instance.

        Args:
            instance: The model instance.

        Returns:
            Model instance with sanitized text.
        """
        for field in instance._meta.fields:
            if isinstance(field, TextField):
                value = getattr(instance, field.attname)
                setattr(instance, field.attname, self.sanitize_text(value))
        return instance

    def sanitize_text(self, value):
        """
        Sanitize text to prevent XSS attacks.

        Args:
            value (str): The text to sanitize.

        Returns:
            str: Sanitized text.
        """
        allowed_tags = [
            'a', 'abbr', 'acronym', 'address', 'b', 'bdo', 'big', 'blockquote', 'br', 'caption', 'cite',
            'code',
            'col', 'colgroup', 'dd', 'del', 'dfn', 'div', 'dl', 'dt', 'em', 'h1', 'h2', 'h3', 'h4', 'h5',
            'h6',
            'hr', 'i', 'img', 'ins', 'kbd', 'li', 'ol', 'p', 'pre', 'q', 'samp', 'small', 'span',
            'strike',
            'strong', 'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th', 'thead', 'tr', 'tt', 'u', 'ul',
            'var'
        ]
        allowed_attributes = {
            '*': ['title', 'style'],
            'a': ['href', 'title'],
            'img': ['src', 'alt'],
        }
        return mark_safe(bleach.clean(value, tags=allowed_tags, attributes=allowed_attributes))
