"""
Abstract backend interface for MediaManager.

This module defines the contract that all backend implementations must follow.
Controllers depend on this interface, not concrete implementations.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class IMediaManagerBackend(ABC):
    """
    Abstract interface for MediaManager backend communication.

    All backend implementations (Mock, Java) must implement this interface.
    This allows Controllers to work with any backend without knowing the implementation.

    Design Pattern: Strategy Pattern + Dependency Injection
    """

    @abstractmethod
    def connect(self) -> None:
        """
        Connect to backend.

        For MockBackend: Does nothing (always "connected")
        For JavaBackend: Opens Unix socket connection

        Raises:
            BackendConnectionError: If connection fails
        """
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """
        Disconnect from backend.

        For MockBackend: Does nothing
        For JavaBackend: Closes socket connection
        """
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """
        Check if backend is connected.

        Returns:
            True if connected and ready, False otherwise
        """
        pass

    @abstractmethod
    def call(self, action: str, **params) -> Any:
        """
        Generic call to backend action.

        This is the main method for all backend operations.

        Args:
            action: Action name (e.g., "genre.create", "artist.getAll", "album.getById")
            **params: Action parameters as keyword arguments

        Returns:
            Action result (dict for single entity, list for multiple)

        Raises:
            BackendException: Base exception for all backend errors
            BackendConnectionError: Connection/communication errors
            BackendValidationError: Validation errors (400)
            BackendNotFoundError: Entity not found (404)
            BackendInternalError: Internal backend errors (500)

        Examples:
            >>> # Create genre
            >>> result = backend.call("genre.create", name="Rock")
            >>> # Returns: {"id": 1, "name": "Rock"}

            >>> # Get all genres
            >>> results = backend.call("genre.getAll")
            >>> # Returns: [{"id": 1, "name": "Rock"}, {"id": 2, "name": "Jazz"}]

            >>> # Get by ID
            >>> result = backend.call("genre.getById", id=1)
            >>> # Returns: {"id": 1, "name": "Rock"}

            >>> # Update
            >>> result = backend.call("genre.update", id=1, name="Hard Rock")
            >>> # Returns: {"id": 1, "name": "Hard Rock"}

            >>> # Delete
            >>> result = backend.call("genre.delete", id=1)
            >>> # Returns: {"success": True}
        """
        pass

    # Métodos de conveniência (podem ser implementados na base ou deixar pros filhos)

    def echo(self, message: str) -> str:
        """
        Test command: echo.

        Args:
            message: Message to echo

        Returns:
            Echoed message
        """
        result = self.call("echo", message=message)
        return result.get("message", message)

    def heartbeat(self) -> int:
        """
        Test command: heartbeat.

        Returns:
            Round-trip time in milliseconds
        """
        result = self.call("heartbeat")
        return result.get("rtt", 0)


# ============================================================================
# EXCEPTIONS
# ============================================================================

class BackendException(Exception):
    """
    Base exception for all backend errors.

    Attributes:
        message: Error message
        status_code: HTTP-like status code (200, 400, 404, 500, etc)
        action: Action that caused the error
        details: Additional error details
    """

    def __init__(
            self,
            message: str,
            status_code: Optional[int] = None,
            action: Optional[str] = None,
            details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.action = action
        self.details = details or {}

    def __str__(self) -> str:
        parts = [self.message]
        if self.action:
            parts.append(f"(action: {self.action})")
        if self.status_code:
            parts.append(f"[{self.status_code}]")
        return " ".join(parts)


class BackendConnectionError(BackendException):
    """
    Raised when backend connection/communication fails.

    Examples:
        - Socket not found
        - Connection refused
        - Connection timeout
        - Connection closed unexpectedly
    """
    pass


class BackendValidationError(BackendException):
    """
    Raised when backend validation fails (HTTP 400).

    Examples:
        - Invalid parameters
        - Missing required fields
        - Data format errors
        - Constraint violations
    """
    pass


class BackendNotFoundError(BackendException):
    """
    Raised when requested entity not found (HTTP 404).

    Examples:
        - Genre ID not found
        - Artist ID not found
        - Album ID not found
    """
    pass


class BackendInternalError(BackendException):
    """
    Raised when backend has internal error (HTTP 500).

    Examples:
        - Database errors
        - Unexpected exceptions
        - Service unavailable
    """
    pass
    pass