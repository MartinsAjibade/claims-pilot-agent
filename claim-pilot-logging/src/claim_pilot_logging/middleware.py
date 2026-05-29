"""
Claim Pilot Logging - Middleware

Request logging middleware for FastAPI/Starlette.
Requires 'starlette' — install with: pip install claim-pilot-logging[fastapi]
"""

import time
from typing import Callable, Optional, Any

from .context import LogContext, new_correlation_id, set_correlation_id
from .logger import get_logger

logger = get_logger(__name__)

CORRELATION_HEADERS = ["X-Correlation-ID", "X-Request-ID", "X-Trace-ID", "traceparent"]


def _import_starlette():
    try:
        from starlette.middleware.base import BaseHTTPMiddleware
        from starlette.requests import Request
        from starlette.responses import Response
        return BaseHTTPMiddleware, Request, Response
    except ImportError:
        raise ImportError("starlette is required for middleware support. Install with: pip install claim-pilot-logging[fastapi]")


def create_request_logging_middleware(
    log_request_body: bool = False,
    log_response_body: bool = False,
    skip_paths: Optional[list] = None,
):
    """Create a request logging middleware class for FastAPI/Starlette."""
    BaseHTTPMiddleware, Request, Response = _import_starlette()
    _skip_paths = skip_paths or ["/health", "/ready", "/metrics", "/favicon.ico"]

    class _RequestLoggingMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next: Callable) -> Response:
            if request.url.path in _skip_paths:
                return await call_next(request)

            correlation_id = _get_correlation_id_from_request(request)

            async with LogContext.request(
                correlation_id=correlation_id,
                http_method=request.method,
                http_path=request.url.path,
                http_query=str(request.query_params) if request.query_params else None,
                client_ip=_get_client_ip(request),
                user_agent=request.headers.get("user-agent"),
            ):
                start_time = time.perf_counter()

                request_data = {"http_method": request.method, "http_path": request.url.path}
                if log_request_body and request.method in ("POST", "PUT", "PATCH"):
                    try:
                        body = await request.body()
                        request_data["request_body"] = body.decode()[:1000]
                    except Exception:
                        pass
                logger.request(**request_data)

                try:
                    response = await call_next(request)
                    duration_ms = (time.perf_counter() - start_time) * 1000
                    logger.response(status_code=response.status_code, duration_ms=duration_ms)
                    response.headers["X-Correlation-ID"] = correlation_id
                    return response
                except Exception as e:
                    duration_ms = (time.perf_counter() - start_time) * 1000
                    logger.error("request.error", error=str(e), error_type=type(e).__name__, duration_ms=round(duration_ms, 2), exc_info=True)
                    raise

    return _RequestLoggingMiddleware


def _get_correlation_id_from_request(request: Any) -> str:
    for header in CORRELATION_HEADERS:
        value = request.headers.get(header)
        if value:
            return value
    return new_correlation_id()


def _get_client_ip(request: Any) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip
    if request.client:
        return request.client.host
    return "unknown"


async def correlation_id_middleware(request: Any, call_next: Callable) -> Any:
    """Simple middleware that just sets correlation ID."""
    correlation_id = _get_correlation_id_from_request(request)
    token = set_correlation_id(correlation_id)
    try:
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        return response
    finally:
        from .context import reset_correlation_id
        reset_correlation_id(token)


class RequestLoggingMiddleware:
    """Request logging middleware (lazy-loaded). Requires starlette."""
    def __new__(cls, app, **kwargs):
        middleware_cls = create_request_logging_middleware(**kwargs)
        return middleware_cls(app)
