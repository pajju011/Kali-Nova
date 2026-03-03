"""
Kalinova custom exception hierarchy.

All exceptions inherit from KalinovaError for unified
error handling across the application.
"""


class KalinovaError(Exception):
    """Base exception for all Kalinova errors."""
    pass


class ToolNotFoundError(KalinovaError):
    """Raised when a CLI tool binary cannot be found on the system."""

    def __init__(self, tool_name: str, expected_path: str = ""):
        self.tool_name = tool_name
        self.expected_path = expected_path
        msg = f"Tool '{tool_name}' not found on this system."
        if expected_path:
            msg += f" Expected at: {expected_path}"
        msg += " Please install it using: sudo apt install " + tool_name
        super().__init__(msg)


class ExecutionError(KalinovaError):
    """Raised when a tool execution fails."""

    def __init__(self, tool_name: str, exit_code: int, stderr: str = ""):
        self.tool_name = tool_name
        self.exit_code = exit_code
        self.stderr = stderr
        msg = f"Tool '{tool_name}' failed with exit code {exit_code}."
        if stderr:
            msg += f"\nError output: {stderr[:500]}"
        super().__init__(msg)


class ParsingError(KalinovaError):
    """Raised when tool output cannot be parsed."""

    def __init__(self, tool_name: str, reason: str = ""):
        self.tool_name = tool_name
        self.reason = reason
        msg = f"Failed to parse output from '{tool_name}'."
        if reason:
            msg += f" Reason: {reason}"
        super().__init__(msg)


class ModelLoadError(KalinovaError):
    """Raised when the ML model cannot be loaded."""

    def __init__(self, model_path: str, reason: str = ""):
        self.model_path = model_path
        self.reason = reason
        msg = f"Failed to load ML model from '{model_path}'."
        if reason:
            msg += f" Reason: {reason}"
        super().__init__(msg)


class ValidationError(KalinovaError):
    """Raised when user input validation fails."""

    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"Validation error on '{field}': {message}")


class PluginError(KalinovaError):
    """Raised when a tool plugin definition is invalid."""

    def __init__(self, plugin_name: str, reason: str = ""):
        self.plugin_name = plugin_name
        self.reason = reason
        msg = f"Invalid plugin definition: '{plugin_name}'."
        if reason:
            msg += f" Reason: {reason}"
        super().__init__(msg)


class PermissionError_(KalinovaError):
    """Raised when a tool requires elevated privileges."""

    def __init__(self, tool_name: str):
        self.tool_name = tool_name
        msg = (
            f"Tool '{tool_name}' requires elevated privileges. "
            "Please run with: sudo kalinova"
        )
        super().__init__(msg)
