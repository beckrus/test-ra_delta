from fastapi import HTTPException


class BaseException(Exception):
    detail = "Unexpected error"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class BaseHTTPException(HTTPException):
    status_code = 500
    detail = "Something went wrong"

    def __init__(self, *args, **kwargs):
        super().__init__(status_code=self.status_code, detail=self.detail, *args, **kwargs)


class SessionNotFoundException(BaseException):
    detail = "Session not found"


class SessionNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Session not found"


class ParcelNotFoundException(BaseException):
    detail = "Parcel not found"


class ParcelNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Parcel not found"


class RateProviderError(BaseException):
    detail = "Something went wrong"


class RateCacheError(BaseException):
    detail = "Something went wrong"

class TaskNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Task not found"

class FKObjectNotFoundException(BaseException):
    detail = "Foreign Key not found"

class TypeNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Parcel Type not found"
