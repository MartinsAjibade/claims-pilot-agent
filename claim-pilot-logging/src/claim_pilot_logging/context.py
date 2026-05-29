"""
Claim Pilot Logging - Context Management

Request-scoped context propagation using contextvars.
Thread-safe and async-safe.
"""

import uuid
from contextvars import ContextVar, Token
from typing import Any, Dict, Optional

import structlog

_request_context: ContextVar[Dict[str, Any]] = ContextVar("claim_pilot_logging_context", default={})
_correlation_id: ContextVar[Optional[str]] = ContextVar("claim_pilot_logging_correlation_id", default=None)


def new_correlation_id() -> str:
    return str(uuid.uuid4())


def get_correlation_id() -> Optional[str]:
    return _correlation_id.get()


def set_correlation_id(correlation_id: str) -> Token:
    return _correlation_id.set(correlation_id)


def reset_correlation_id(token: Token) -> None:
    _correlation_id.reset(token)


def get_context() -> Dict[str, Any]:
    return _request_context.get().copy()


def bind_context(**kwargs: Any) -> None:
    current = _request_context.get().copy()
    current.update(kwargs)
    _request_context.set(current)
    structlog.contextvars.bind_contextvars(**kwargs)


def unbind_context(*keys: str) -> None:
    current = _request_context.get().copy()
    for key in keys:
        current.pop(key, None)
    _request_context.set(current)
    structlog.contextvars.unbind_contextvars(*keys)


def clear_context() -> None:
    _request_context.set({})
    _correlation_id.set(None)
    structlog.contextvars.clear_contextvars()


class LogContext:
    """
    Context manager for scoped logging context.
    Thread-safe and async-safe.

    Usage:
        with LogContext(user_id="123"):
            logger.info("Processing")

        with LogContext.request(claim_id="CLM-1001"):
            # correlation_id is automatically set
            logger.info("Handling request")
    """

    def __init__(self, correlation_id: Optional[str] = None, **kwargs: Any):
        self._context = kwargs
        self._correlation_id = correlation_id
        self._context_token: Optional[Token] = None
        self._corr_token: Optional[Token] = None
        self._previous_context: Dict[str, Any] = {}

    @classmethod
    def request(cls, **kwargs: Any) -> "LogContext":
        return cls(correlation_id=new_correlation_id(), **kwargs)

    def __enter__(self) -> "LogContext":
        self._previous_context = _request_context.get().copy()
        if self._correlation_id:
            self._corr_token = set_correlation_id(self._correlation_id)
        new_context = self._previous_context.copy()
        new_context.update(self._context)
        self._context_token = _request_context.set(new_context)
        structlog.contextvars.bind_contextvars(**self._context)
        if self._correlation_id:
            structlog.contextvars.bind_contextvars(correlation_id=self._correlation_id)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        _request_context.set(self._previous_context)
        if self._corr_token:
            reset_correlation_id(self._corr_token)
        structlog.contextvars.unbind_contextvars(*self._context.keys())
        if self._correlation_id:
            structlog.contextvars.unbind_contextvars("correlation_id")

    async def __aenter__(self) -> "LogContext":
        return self.__enter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        self.__exit__(exc_type, exc_val, exc_tb)

    def bind(self, **kwargs: Any) -> None:
        bind_context(**kwargs)
        self._context.update(kwargs)


def with_context(**kwargs: Any):
    """Decorator to add context to all logs within a function."""
    def decorator(func):
        def wrapper(*args, **func_kwargs):
            with LogContext(**kwargs):
                return func(*args, **func_kwargs)

        async def async_wrapper(*args, **func_kwargs):
            async with LogContext(**kwargs):
                return await func(*args, **func_kwargs)

        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return wrapper

    return decorator
