
# The custom schemas file

from drf_spectacular.utils import extend_schema
from core.errors.client.main import bad_args


# Define the base schema with 400 response
base_responses = {
    400: bad_args
}

teacher_schema_base = extend_schema(
    methods=("GET", "POST", "DELETE"),
    responses=base_responses
)

# teacher_schema_get = extend_schema(
#    methods = ("GET",),
#     responses = {
#         200: Serializer(many = True),
#         **base_responses
#     }
# )
