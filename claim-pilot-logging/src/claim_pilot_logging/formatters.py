"""
Claim Pilot Logging - Formatters

Output formatters for different targets and aggregators.
"""

import json
import logging
from typing import Any, Dict, Optional

import structlog

try:
    import orjson
    HAS_ORJSON = True
except ImportError:
    HAS_ORJSON = False


class JSONFormatter(structlog.stdlib.ProcessorFormatter):
    """JSON formatter optimized for log aggregators."""

    def __init__(self, **kwargs):
        super().__init__(processor=self._json_renderer, **kwargs)

    def _json_renderer(self, logger: logging.Logger, method_name: str, event_dict: Dict[str, Any]) -> str:
        ordered = self._order_fields(event_dict)
        if HAS_ORJSON:
            return orjson.dumps(ordered).decode("utf-8")
        return json.dumps(ordered, default=str, ensure_ascii=False)

    def _order_fields(self, event_dict: Dict[str, Any]) -> Dict[str, Any]:
        priority = ["timestamp", "level", "event", "service", "env", "correlation_id", "trace_id"]
        ordered = {}
        for key in priority:
            if key in event_dict:
                ordered[key] = event_dict[key]
        for key in sorted(event_dict.keys()):
            if key not in ordered:
                ordered[key] = event_dict[key]
        return ordered


class ConsoleFormatter(structlog.stdlib.ProcessorFormatter):
    """Pretty console formatter for development."""

    def __init__(self, colors: bool = True, **kwargs):
        super().__init__(processor=structlog.dev.ConsoleRenderer(colors=colors), **kwargs)


class AggregatorFormatter(structlog.stdlib.ProcessorFormatter):
    """Formatter optimized for specific aggregators (ELK, Datadog, CloudWatch)."""

    AGGREGATOR_MAPPINGS = {
        "elk": {
            "timestamp": "@timestamp", "level": "log.level", "event": "message",
            "service": "service.name", "env": "deployment.environment", "correlation_id": "trace.id",
        },
        "datadog": {
            "timestamp": "timestamp", "level": "status", "event": "message",
            "service": "service", "env": "env", "correlation_id": "dd.trace_id",
        },
        "cloudwatch": {
            "timestamp": "timestamp", "level": "level", "event": "message",
            "service": "service", "env": "environment", "correlation_id": "requestId",
        },
    }

    def __init__(self, aggregator: str = "elk", **kwargs):
        self.aggregator = aggregator
        self.field_mapping = self.AGGREGATOR_MAPPINGS.get(aggregator, {})
        super().__init__(processor=self._aggregator_renderer, **kwargs)

    def _aggregator_renderer(self, logger: logging.Logger, method_name: str, event_dict: Dict[str, Any]) -> str:
        mapped = {}
        for key, value in event_dict.items():
            new_key = self.field_mapping.get(key, key)
            mapped[new_key] = value
        if HAS_ORJSON:
            return orjson.dumps(mapped).decode("utf-8")
        return json.dumps(mapped, default=str, ensure_ascii=False)


def get_formatter(output_format: str, config: Optional[Any] = None) -> logging.Formatter:
    """Get formatter based on output format."""
    from .config import OutputFormat

    if isinstance(output_format, OutputFormat):
        output_format = output_format.value
    output_format = output_format.lower()

    if output_format == "json":
        return JSONFormatter()
    elif output_format == "console":
        return ConsoleFormatter()
    elif output_format in ("elk", "datadog", "cloudwatch", "splunk"):
        return AggregatorFormatter(aggregator=output_format)
    else:
        return JSONFormatter()
