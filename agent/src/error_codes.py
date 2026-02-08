"""
Global error code registry for agent service
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorCode:
    code: str
    message: str
    http_status: int


INTERNAL_ERROR = ErrorCode(code="E500", message="Internal server error", http_status=500)
VALIDATION_ERROR = ErrorCode(code="E400", message="Invalid request", http_status=400)
NOT_FOUND = ErrorCode(code="E404", message="Not found", http_status=404)
UNAUTHORIZED = ErrorCode(code="E401", message="Unauthorized", http_status=401)
FORBIDDEN = ErrorCode(code="E403", message="Forbidden", http_status=403)
CONFLICT = ErrorCode(code="E409", message="Conflict", http_status=409)
EXTERNAL_DEPENDENCY = ErrorCode(code="E502", message="Bad gateway", http_status=502)


ERROR_REGISTRY = {
    INTERNAL_ERROR.code: INTERNAL_ERROR,
    VALIDATION_ERROR.code: VALIDATION_ERROR,
    NOT_FOUND.code: NOT_FOUND,
    UNAUTHORIZED.code: UNAUTHORIZED,
    FORBIDDEN.code: FORBIDDEN,
    CONFLICT.code: CONFLICT,
    EXTERNAL_DEPENDENCY.code: EXTERNAL_DEPENDENCY,
}
