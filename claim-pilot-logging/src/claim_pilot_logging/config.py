"""
Claim Pilot Logging - Configuration

Central configuration for logging setup.
"""

import logging
import os
import sys
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Union

import structlog

from .processors import (
    add_caller_info,
    add_correlation_id,
    add_service_context,
    add_timestamp_fields,
    censor_sensitive_data,
    flatten_nested_dicts,
    truncate_long_values,
)


class LogLevel(str, Enum):
    """Log levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class OutputFormat(str, Enum):
    """Output format options."""
    JSON = "json"           # For aggregators (production)
    CONSOLE = "console"     # Pretty print (development)
    LOGFMT = "logfmt"       # Key=value format


@dataclass
class LogConfig:
    """
    Logging configuration.

    Attributes:
        service_name: Name of the service (appears in all logs)
        environment: Deployment environment (dev, staging, prod)
        version: Service version
        log_level: Minimum log level
        output_format: Output format (json, console, logfmt)
        include_caller: Include file/line info
        include_timestamp: Include ISO timestamp
        include_trace_id: Include trace/correlation ID
        sensitive_fields: Fields to mask in output
        max_field_length: Truncate fields longer than this
        flatten_nested: Flatten nested dicts for aggregators
        output_file: Optional file output path
        async_safe: Use contextvars for async safety
    """
    service_name: str = "claim-pilot-service"
    environment: str = "development"
    version: str = "0.0.0"
    log_level: LogLevel = LogLevel.INFO
    output_format: OutputFormat = OutputFormat.JSON
    include_caller: bool = True
    include_timestamp: bool = True
    include_trace_id: bool = True
    sensitive_fields: List[str] = field(default_factory=lambda: [
        "password", "token", "api_key", "secret", "authorization",
        "ssn", "social_security", "credit_card", "card_number",
        "cvv", "pin", "private_key", "access_token", "refresh_token",
    ])
    max_field_length: int = 1000
    flatten_nested: bool = True
    output_file: Optional[str] = None
    async_safe: bool = True

    @classmethod
    def from_env(cls) -> "LogConfig":
        """Create config from environment variables."""
        return cls(
            service_name=os.getenv("SERVICE_NAME", "claim-pilot-service"),
            environment=os.getenv("ENVIRONMENT", "development"),
            version=os.getenv("SERVICE_VERSION", "0.0.0"),
            log_level=LogLevel(os.getenv("LOG_LEVEL", "INFO").upper()),
            output_format=OutputFormat(os.getenv("LOG_FORMAT", "json").lower()),
            include_caller=os.getenv("LOG_INCLUDE_CALLER", "true").lower() == "true",
            include_timestamp=os.getenv("LOG_INCLUDE_TIMESTAMP", "true").lower() == "true",
            include_trace_id=os.getenv("LOG_INCLUDE_TRACE_ID", "true").lower() == "true",
            max_field_length=int(os.getenv("LOG_MAX_FIELD_LENGTH", "1000")),
            flatten_nested=os.getenv("LOG_FLATTEN_NESTED", "true").lower() == "true",
            output_file=os.getenv("LOG_FILE"),
        )


# Global config instance
_config: Optional[LogConfig] = None
_configured: bool = False


def get_config() -> LogConfig:
    """Get current logging configuration."""
    global _config
    if _config is None:
        _config = LogConfig.from_env()
    return _config


def setup_logging(
    service_name: Optional[str] = None,
    environment: Optional[str] = None,
    log_level: Optional[Union[str, LogLevel]] = None,
    output_format: Optional[Union[str, OutputFormat]] = None,
    **kwargs,
) -> LogConfig:
    """
    Quick setup for logging with sensible defaults.

    Args:
        service_name: Service name for logs
        environment: Environment (dev, staging, prod)
        log_level: Minimum log level
        output_format: Output format (json, console)
        **kwargs: Additional LogConfig options

    Returns:
        LogConfig instance
    """
    config_kwargs = {}

    if service_name:
        config_kwargs["service_name"] = service_name
    if environment:
        config_kwargs["environment"] = environment
    if log_level:
        if isinstance(log_level, str):
            config_kwargs["log_level"] = LogLevel(log_level.strip().upper())
        else:
            config_kwargs["log_level"] = log_level
    if output_format:
        if isinstance(output_format, str):
            config_kwargs["output_format"] = OutputFormat(output_format.strip().lower())
        else:
            config_kwargs["output_format"] = output_format

    config_kwargs.update(kwargs)

    config = LogConfig(**config_kwargs)
    return configure_logging(config)


def configure_logging(config: LogConfig) -> LogConfig:
    """
    Configure logging with full control.

    Args:
        config: LogConfig instance

    Returns:
        The applied LogConfig
    """
    global _config, _configured

    if _configured:
        return _config

    _config = config

    # Build processor chain
    processors = _build_processors(config)

    # Configure structlog
    structlog.configure(
        processors=processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
        context_class=dict,
    )

    # Configure stdlib logging
    _configure_stdlib_logging(config)

    _configured = True
    return config


def _build_processors(config: LogConfig) -> List:
    """Build the processor chain based on config."""
    processors = []

    # Context merging (async-safe)
    if config.async_safe:
        processors.append(structlog.contextvars.merge_contextvars)

    # Add standard fields
    processors.append(structlog.stdlib.add_log_level)
    processors.append(structlog.stdlib.add_logger_name)

    # Service context (service_name, environment, version)
    processors.append(add_service_context(
        service_name=config.service_name,
        environment=config.environment,
        version=config.version,
    ))

    # Correlation ID
    if config.include_trace_id:
        processors.append(add_correlation_id)

    # Timestamp
    if config.include_timestamp:
        processors.append(structlog.processors.TimeStamper(fmt="iso"))
        processors.append(add_timestamp_fields)

    # Caller info
    if config.include_caller:
        processors.append(add_caller_info)

    # Data processing
    processors.append(censor_sensitive_data(config.sensitive_fields))
    processors.append(truncate_long_values(config.max_field_length))

    # Flatten for aggregators
    if config.flatten_nested:
        processors.append(flatten_nested_dicts)

    # Stack info and unicode
    processors.append(structlog.processors.StackInfoRenderer())
    processors.append(structlog.processors.UnicodeDecoder())

    return processors


def _configure_stdlib_logging(config: LogConfig):
    """Configure Python stdlib logging."""
    from .formatters import get_formatter

    formatter = get_formatter(config.output_format, config)

    handlers = []

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    handlers.append(console_handler)

    if config.output_file:
        file_handler = logging.FileHandler(config.output_file)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    root = logging.getLogger()
    root.handlers = handlers
    root.setLevel(getattr(logging, config.log_level.value))

    # Quiet noisy loggers
    for noisy in ["httpx", "httpcore", "urllib3", "asyncio"]:
        logging.getLogger(noisy).setLevel(logging.WARNING)
