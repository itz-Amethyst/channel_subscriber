from typing import Optional , Dict , Any

from drf_spectacular.utils import inline_serializer
from rest_framework.fields import CharField


class CustomErrorSerializer:
    def __init__(self, code: int, title: str, detail: str, status: int = 400, extra: Optional[Dict[str, Any]] = None):
        self.code = code
        self.title = title
        self.detail = detail
        self.status = status
        # Can add a logic here to only shows extra if there was data otherwise not {} -> none
        self.extra = extra or {}

        self.fields = {
            'code': CharField(default=self.code),
            'title': CharField(default=self.title),
            'detail': CharField(default=self.detail),
            'status': CharField(default = self.status),
            **{key: CharField(default=str(value)) for key, value in self.extra.items()}
        }

    def __call__(self):
        return inline_serializer(name=self.title, fields=self.fields)