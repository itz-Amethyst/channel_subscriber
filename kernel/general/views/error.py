from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from core.errors import all_errors


class get_all_errors(ViewSet):
    def list( self, request ):
        serialized_errors = [
            {
                'code': error.code ,
                'title': error.title ,
                'detail': error.detail ,
                'status': error.status ,
                **({'extra': error.extra} if hasattr(error , 'extra') and bool(error.extra) else {}) ,
            }
            for error in all_errors if isinstance(error , object)
        ]
        return Response(serialized_errors , status = status.HTTP_200_OK)