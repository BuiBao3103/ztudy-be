from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException

class CustomAPIException(APIException):
    """
    A custom exception to ensure all errors follow DRF's default format:
    {
        "detail": "Error message"
    }
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid request."
    default_code = "bad_request"

    def __init__(self, detail=None, status_code=None):
        if detail is not None:
            self.detail = {"detail": detail}  # Ensure error format is correct
        if status_code is not None:
            self.status_code = status_code

def custom_exception_handler(exc, context):
    """
    Custom exception handler to ensure consistent error responses in DRF.
    """
    response = exception_handler(exc, context)

    # If DRF's default exception handler returned a response, use it.
    if response is not None:
        return response

    # Handle CustomAPIException explicitly
    if isinstance(exc, CustomAPIException):
        return Response(exc.detail, status=exc.status_code)

    # Fallback for other unhandled exceptions
    return Response({"detail": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
