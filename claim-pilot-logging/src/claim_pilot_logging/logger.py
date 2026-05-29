"""
Claim Pilot Logging - Logger

Main logger interface with enhanced functionality.
"""

from functools import lru_cache
from typing import Any, Dict, Optional

import structlog

from .config import get_config, setup_logging


class Logger:
    """
    Enhanced logger wrapper with structured event logging,
    request/response helpers, audit logging, and tool/LLM tracking.
    """

    def __init__(self, name: str):
        self.name = name
        self._logger: Optional[structlog.stdlib.BoundLogger] = None

    @property
    def logger(self) -> structlog.stdlib.BoundLogger:
        if self._logger is None:
            config = get_config()
            if not hasattr(config, '_configured'):
                setup_logging()
            self._logger = structlog.get_logger(self.name)
        return self._logger

    # Standard log methods
    def debug(self, event: str, **kwargs: Any) -> None:
        self.logger.debug(event, **kwargs)

    def info(self, event: str, **kwargs: Any) -> None:
        self.logger.info(event, **kwargs)

    def warning(self, event: str, **kwargs: Any) -> None:
        self.logger.warning(event, **kwargs)

    def error(self, event: str, exc_info: bool = False, **kwargs: Any) -> None:
        self.logger.error(event, exc_info=exc_info, **kwargs)

    def critical(self, event: str, exc_info: bool = False, **kwargs: Any) -> None:
        self.logger.critical(event, exc_info=exc_info, **kwargs)

    def exception(self, event: str, **kwargs: Any) -> None:
        self.logger.exception(event, **kwargs)

    # Structured event logging
    def event(self, event_type: str, event_name: str, level: str = "info", **kwargs: Any) -> None:
        log_method = getattr(self.logger, level, self.logger.info)
        log_method(f"{event_type}.{event_name}", event_type=event_type, event_name=event_name, **kwargs)

    # Request/response logging
    def request(self, method: str, path: str, **kwargs: Any) -> None:
        self.info("request.incoming", http_method=method, http_path=path, log_category="request", **kwargs)

    def response(self, status_code: int, duration_ms: float, **kwargs: Any) -> None:
        level = "info" if status_code < 400 else "error" if status_code >= 500 else "warning"
        log_method = getattr(self.logger, level)
        log_method("response.outgoing", http_status=status_code, duration_ms=round(duration_ms, 2), log_category="response", **kwargs)

    # Audit logging
    def audit(self, action: str, resource_type: str, resource_id: str, actor_id: Optional[str] = None, result: str = "success", **kwargs: Any) -> None:
        self.info("audit.action", audit_action=action, audit_resource_type=resource_type, audit_resource_id=resource_id, audit_actor_id=actor_id, audit_result=result, log_category="audit", **kwargs)

    # Metric logging
    def metric(self, name: str, value: float, unit: str = "count", tags: Optional[Dict[str, str]] = None, **kwargs: Any) -> None:
        self.info("metric.recorded", metric_name=name, metric_value=value, metric_unit=unit, metric_tags=tags or {}, log_category="metric", **kwargs)

    # Tool logging
    def tool_start(self, tool_name: str, **kwargs: Any) -> None:
        self.debug("tool.start", tool_name=tool_name, **kwargs)

    def tool_success(self, tool_name: str, duration_ms: float, **kwargs: Any) -> None:
        self.info("tool.success", tool_name=tool_name, duration_ms=round(duration_ms, 2), tool_result="success", **kwargs)

    def tool_error(self, tool_name: str, error: str, duration_ms: Optional[float] = None, **kwargs: Any) -> None:
        self.error("tool.error", tool_name=tool_name, tool_error=error, tool_result="error", duration_ms=round(duration_ms, 2) if duration_ms else None, **kwargs)

    # LLM logging
    def llm_request(self, model: str, prompt_tokens: Optional[int] = None, **kwargs: Any) -> None:
        self.debug("llm.request", llm_model=model, llm_prompt_tokens=prompt_tokens, **kwargs)

    def llm_response(self, model: str, completion_tokens: Optional[int] = None, total_tokens: Optional[int] = None, duration_ms: Optional[float] = None, **kwargs: Any) -> None:
        self.info("llm.response", llm_model=model, llm_completion_tokens=completion_tokens, llm_total_tokens=total_tokens, duration_ms=round(duration_ms, 2) if duration_ms else None, **kwargs)

    # Binding
    def bind(self, **kwargs: Any) -> "Logger":
        new_logger = Logger(self.name)
        new_logger._logger = self.logger.bind(**kwargs)
        return new_logger


@lru_cache(maxsize=256)
def get_logger(name: str) -> Logger:
    """Get a logger instance (cached per name)."""
    return Logger(name)
