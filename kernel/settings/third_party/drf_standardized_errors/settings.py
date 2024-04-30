DRF_STANDARDIZED_ERRORS = {
    # class responsible for handling the exceptions. Can be subclassed to change
    # which exceptions are handled by default, to update which exceptions are
    # reported to error monitoring tools (like Sentry), ...
    "EXCEPTION_HANDLER_CLASS": "kernel.standardize.handler.main.MainExceptionHandler",
    # class responsible for generating error response output. Can be subclassed
    # to change the format of the error response.
    "EXCEPTION_FORMATTER_CLASS": "kernel.standardize.formatter.main.MainExceptionFormatter",
    # enable the standardized errors when DEBUG=True for unhandled exceptions.
    # By default, this is set to False so you're able to view the traceback in
    # the terminal and get more information about the exception.
    #! For testing purpose set to True
    "ENABLE_IN_DEBUG_FOR_UNHANDLED_EXCEPTIONS": False,


    # The below settings are for OpenAPI 3 schema generation

    # ONLY the responses that correspond to these status codes will appear
    # in the API schema.
    "ALLOWED_ERROR_STATUS_CODES": [
        "400",
        "401",
        "403",
        "404",
        "405",
        "406",
        "415",
        "429",
        "500",
    ],
}