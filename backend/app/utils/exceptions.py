from fastapi import HTTPException, status

class BusinessError(HTTPException):
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)

class NotFoundError(BusinessError):
    def __init__(self, resource: str):
        super().__init__(
            detail=f"{resource}不存在",
            status_code=status.HTTP_404_NOT_FOUND
        )

class ValidationError(BusinessError):
    pass

class PermissionError(BusinessError):
    def __init__(self):
        super().__init__(
            detail="权限不足",
            status_code=status.HTTP_403_FORBIDDEN
        ) 