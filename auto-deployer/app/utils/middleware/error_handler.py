"""Error handling middleware and utilities."""

import structlog
from fastapi import Request, status
from fastapi.responses import JSONResponse
from typing import Callable, Any

logger = structlog.get_logger()


class ErrorHandler:
    """Comprehensive error handling."""

    @staticmethod
    async def handle_exception(request: Request, exc: Exception) -> JSONResponse:
        """Handle exceptions and return appropriate response."""
        logger.error(
            "unhandled_exception",
            path=request.url.path,
            method=request.method,
            error=str(exc),
            exc_type=type(exc).__name__,
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal Server Error",
                "detail": str(exc),
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
        )

    @staticmethod
    async def handle_validation_error(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """Handle validation errors."""
        logger.error(
            "validation_error",
            path=request.url.path,
            error=str(exc),
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "Validation Error",
                "detail": str(exc),
                "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            },
        )

    @staticmethod
    async def handle_not_found(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """Handle 404 Not Found errors."""
        logger.warning(
            "not_found",
            path=request.url.path,
            method=request.method,
        )

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": "Not Found",
                "detail": f"Path {request.url.path} not found",
                "status_code": status.HTTP_404_NOT_FOUND,
            },
        )

    @staticmethod
    async def handle_unauthorized(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """Handle authentication errors."""
        logger.warning(
            "unauthorized_access",
            path=request.url.path,
            method=request.method,
        )

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "error": "Unauthorized",
                "detail": "Invalid or missing credentials",
                "status_code": status.HTTP_401_UNAUTHORIZED,
            },
        )

    @staticmethod
    async def handle_forbidden(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """Handle authorization errors."""
        logger.warning(
            "forbidden_access",
            path=request.url.path,
            method=request.method,
        )

        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "error": "Forbidden",
                "detail": "Access denied",
                "status_code": status.HTTP_403_FORBIDDEN,
            },
        )


class ErrorLogging:
    """Error logging utilities."""

    @staticmethod
    def log_api_error(
        endpoint: str,
        method: str,
        status_code: int,
        error: str,
        request_data: Any = None,
    ) -> None:
        """Log API error."""
        logger.error(
            "api_error",
            endpoint=endpoint,
            method=method,
            status_code=status_code,
            error=error,
            request_data=request_data,
        )

    @staticmethod
    def log_service_error(
        service: str,
        operation: str,
        error: str,
    ) -> None:
        """Log service error."""
        logger.error(
            "service_error",
            service=service,
            operation=operation,
            error=error,
        )

    @staticmethod
    def log_deployment_error(
        task_id: str,
        step: int,
        error: str,
        action: str,
    ) -> None:
        """Log deployment error."""
        logger.error(
            "deployment_error",
            task_id=task_id,
            step=step,
            error=error,
            action=action,
        )


# Singleton instance
error_handler = ErrorHandler()
error_logging = ErrorLogging()
