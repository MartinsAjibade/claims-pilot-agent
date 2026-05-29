"""
Claim Pilot Logging - Metrics

Decorators and utilities for timing and counting operations.
"""

import functools
import time
from enum import Enum
from typing import Any, Callable, Dict, Optional, TypeVar

from .logger import get_logger

logger = get_logger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


class MetricType(str, Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"


def log_metric(
    name: str,
    value: float,
    metric_type: MetricType = MetricType.GAUGE,
    unit: str = "count",
    tags: Optional[Dict[str, str]] = None,
    **kwargs: Any,
) -> None:
    """Log a metric event for aggregation."""
    logger.info(
        f"metric.{metric_type.value}",
        metric_name=name,
        metric_value=value,
        metric_type=metric_type.value,
        metric_unit=unit,
        metric_tags=tags or {},
        log_category="metric",
        **kwargs,
    )


def timed(
    name: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    log_args: bool = False,
    log_result: bool = False,
) -> Callable[[F], F]:
    """Decorator to time function execution (sync and async)."""
    def decorator(func: F) -> F:
        metric_name = name or f"{func.__module__}.{func.__name__}"

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            func_logger = get_logger(func.__module__)
            start_data = {"function": func.__name__}
            if log_args:
                start_data["args"] = str(args)[:200]
                start_data["kwargs"] = str(kwargs)[:200]
            func_logger.debug("function.start", **start_data)

            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                duration_ms = (time.perf_counter() - start) * 1000
                end_data = {"function": func.__name__, "duration_ms": round(duration_ms, 2), "success": True}
                if log_result:
                    end_data["result"] = str(result)[:200]
                func_logger.info("function.complete", **end_data)
                log_metric(metric_name, duration_ms, MetricType.TIMER, unit="ms", tags={**(tags or {}), "status": "success"})
                return result
            except Exception as e:
                duration_ms = (time.perf_counter() - start) * 1000
                func_logger.error("function.error", function=func.__name__, duration_ms=round(duration_ms, 2), error=str(e), success=False, exc_info=True)
                log_metric(metric_name, duration_ms, MetricType.TIMER, unit="ms", tags={**(tags or {}), "status": "error"})
                raise

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            func_logger = get_logger(func.__module__)
            start_data = {"function": func.__name__}
            if log_args:
                start_data["args"] = str(args)[:200]
                start_data["kwargs"] = str(kwargs)[:200]
            func_logger.debug("function.start", **start_data)

            start = time.perf_counter()
            try:
                result = await func(*args, **kwargs)
                duration_ms = (time.perf_counter() - start) * 1000
                end_data = {"function": func.__name__, "duration_ms": round(duration_ms, 2), "success": True}
                if log_result:
                    end_data["result"] = str(result)[:200]
                func_logger.info("function.complete", **end_data)
                log_metric(metric_name, duration_ms, MetricType.TIMER, unit="ms", tags={**(tags or {}), "status": "success"})
                return result
            except Exception as e:
                duration_ms = (time.perf_counter() - start) * 1000
                func_logger.error("function.error", function=func.__name__, duration_ms=round(duration_ms, 2), error=str(e), success=False, exc_info=True)
                log_metric(metric_name, duration_ms, MetricType.TIMER, unit="ms", tags={**(tags or {}), "status": "error"})
                raise

        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper  # type: ignore
        return sync_wrapper  # type: ignore

    return decorator


def count(name: str, tags: Optional[Dict[str, str]] = None, value: float = 1) -> Callable[[F], F]:
    """Decorator to count function calls."""
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            log_metric(name, value, MetricType.COUNTER, tags=tags)
            return func(*args, **kwargs)

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            log_metric(name, value, MetricType.COUNTER, tags=tags)
            return await func(*args, **kwargs)

        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper  # type: ignore
        return sync_wrapper  # type: ignore

    return decorator


class Timer:
    """Context manager for timing code blocks."""

    def __init__(self, name: str, tags: Optional[Dict[str, str]] = None, auto_log: bool = True):
        self.name = name
        self.tags = tags or {}
        self.auto_log = auto_log
        self._start: Optional[float] = None
        self._end: Optional[float] = None

    @property
    def duration_ms(self) -> float:
        if self._start is None:
            return 0.0
        end = self._end or time.perf_counter()
        return (end - self._start) * 1000

    def start(self) -> "Timer":
        self._start = time.perf_counter()
        return self

    def stop(self) -> float:
        self._end = time.perf_counter()
        if self.auto_log:
            log_metric(self.name, self.duration_ms, MetricType.TIMER, unit="ms", tags=self.tags)
        return self.duration_ms

    def __enter__(self) -> "Timer":
        self.start()
        return self

    def __exit__(self, *args) -> None:
        self.stop()

    async def __aenter__(self) -> "Timer":
        self.start()
        return self

    async def __aexit__(self, *args) -> None:
        self.stop()
