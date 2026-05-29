"""
Claim Pilot Logging

Comprehensive structured logging for Claim Pilot platform.
Designed for log aggregation systems (ELK, Datadog, CloudWatch, etc.)

Features:
- Structured JSON output for aggregators
- Correlation IDs for distributed tracing
- Request-scoped context propagation
- Performance timing and metrics
- Sensitive data masking
- Multiple output targets
- Async-safe using contextvars
"""

__version__ = "2026.05.1"

# Core exports
from .config import (
    LogConfig,
    LogLevel,
    OutputFormat,
    configure_logging,
    setup_logging,
)
from .context import (
    LogContext,
    bind_context,
    clear_context,
    get_context,
    get_correlation_id,
    new_correlation_id,
    set_correlation_id,
    unbind_context,
)
from .formatters import (
    AggregatorFormatter,
    ConsoleFormatter,
    JSONFormatter,
)
from .logger import (
    Logger,
    get_logger,
)
from .metrics import (
    MetricType,
    count,
    log_metric,
    timed,
)
# Middleware imports (lazy - starlette is optional)
from .middleware import (
    RequestLoggingMiddleware,
    correlation_id_middleware,
    create_request_logging_middleware,
)

__all__ = [
    # Version
    "__version__",
    # Config
    "setup_logging",
    "configure_logging",
    "LogConfig",
    "LogLevel",
    "OutputFormat",
    # Logger
    "get_logger",
    "Logger",
    # Context
    "LogContext",
    "bind_context",
    "unbind_context",
    "clear_context",
    "get_context",
    "get_correlation_id",
    "set_correlation_id",
    "new_correlation_id",
    # Metrics
    "timed",
    "count",
    "log_metric",
    "MetricType",
    # Middleware (requires starlette)
    "RequestLoggingMiddleware",
    "correlation_id_middleware",
    "create_request_logging_middleware",
    # Formatters
    "JSONFormatter",
    "ConsoleFormatter",
    "AggregatorFormatter",
]
