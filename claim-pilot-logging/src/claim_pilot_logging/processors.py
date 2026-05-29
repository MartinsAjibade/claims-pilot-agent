"""
Claim Pilot Logging - Processors

Custom structlog processors for comprehensive logging.
"""

import inspect
import re
from datetime import datetime
from typing import Any, Callable, Dict, List

from .context import get_correlation_id


def add_service_context(service_name: str, environment: str, version: str) -> Callable:
    """Processor factory that adds service metadata to all logs."""
    def processor(logger, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
        event_dict["service"] = service_name
        event_dict["env"] = environment
        event_dict["version"] = version
        return event_dict
    return processor


def add_correlation_id(logger, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Add correlation/trace ID for distributed tracing."""
    corr_id = get_correlation_id()
    if corr_id:
        event_dict["correlation_id"] = corr_id
        event_dict["trace_id"] = corr_id
    return event_dict


def add_timestamp_fields(logger, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Add additional timestamp fields for aggregators."""
    now = datetime.utcnow()
    event_dict["timestamp_epoch"] = int(now.timestamp())
    event_dict["timestamp_epoch_ms"] = int(now.timestamp() * 1000)
    event_dict["date"] = now.strftime("%Y-%m-%d")
    event_dict["hour"] = now.hour
    return event_dict


def add_caller_info(logger, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Add caller information (file, function, line)."""
    frame = inspect.currentframe()
    try:
        skip_modules = {"structlog", "logging", "claim_pilot_logging"}
        for _ in range(20):
            if frame is None:
                break
            frame = frame.f_back
            if frame is None:
                break
            module = frame.f_globals.get("__name__", "")
            if any(module.startswith(skip) for skip in skip_modules):
                continue
            event_dict["caller_file"] = frame.f_code.co_filename.split("/")[-1]
            event_dict["caller_func"] = frame.f_code.co_name
            event_dict["caller_line"] = frame.f_lineno
            event_dict["caller_module"] = module
            break
    finally:
        del frame
    return event_dict


def censor_sensitive_data(sensitive_fields: List[str]) -> Callable:
    """Processor factory that censors sensitive data."""
    patterns = [re.compile(f".*{field}.*", re.IGNORECASE) for field in sensitive_fields]

    def _censor_value(value: Any) -> Any:
        if isinstance(value, str) and len(value) > 0:
            if len(value) > 8:
                return f"{value[:2]}***{value[-2:]}"
            return "***"
        return "***"

    def _process_dict(d: Dict[str, Any], depth: int = 0) -> Dict[str, Any]:
        if depth > 10:
            return d
        result = {}
        for key, value in d.items():
            is_sensitive = any(p.match(key) for p in patterns)
            if is_sensitive:
                result[key] = _censor_value(value)
            elif isinstance(value, dict):
                result[key] = _process_dict(value, depth + 1)
            elif isinstance(value, list):
                result[key] = [_process_dict(item, depth + 1) if isinstance(item, dict) else item for item in value]
            else:
                result[key] = value
        return result

    def processor(logger, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
        return _process_dict(event_dict)

    return processor


def truncate_long_values(max_length: int) -> Callable:
    """Processor factory that truncates long string values."""
    def _truncate(value: Any, depth: int = 0) -> Any:
        if depth > 10:
            return value
        if isinstance(value, str) and len(value) > max_length:
            truncated = len(value) - max_length
            return f"{value[:max_length]}... [{truncated} chars truncated]"
        elif isinstance(value, dict):
            return {k: _truncate(v, depth + 1) for k, v in value.items()}
        elif isinstance(value, list):
            if len(value) > 100:
                return _truncate(value[:100], depth + 1) + [f"... [{len(value) - 100} items truncated]"]
            return [_truncate(item, depth + 1) for item in value]
        return value

    def processor(logger, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
        return {k: _truncate(v) for k, v in event_dict.items()}

    return processor


def flatten_nested_dicts(logger, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Flatten nested dictionaries for aggregators."""
    def _flatten(d: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
        result = {}
        for key, value in d.items():
            new_key = f"{prefix}.{key}" if prefix else key
            skip_flatten = {"event", "timestamp", "level", "logger"}
            if isinstance(value, dict) and key not in skip_flatten:
                result.update(_flatten(value, new_key))
            else:
                result[new_key] = value
        return result
    return _flatten(event_dict)
