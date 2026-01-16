"""
Base controller for MediaManager UI.

This provides common functionality for all entity controllers.
"""


import logging
from typing import Any, Dict, List, Optional, Type

from backend.interface import (
    IMediaManagerBackend,
    BackendException,
    BackendConnectionError,
    BackendValidationError,
    BackendNotFoundError,
    BackendInternalError,
)

logger = logging.getLogger(__name__)


class BaseController:
    """
    Base controller for entity management.

    Subclasses should override:
    - entity_name: e.g., "genre", "artist", "album"
    - entity_display_name: e.g., "Genre", "Artist", "Album"
    """

    entity_name: str = ""  # Override in subclass (e.g., "genre")
    entity_display_name: str = ""  # Override in subclass (e.g., "Genre")

    def __init__(self, backend: IMediaManagerBackend):
        """
        Initialize controller.

        Args:
            backend: Backend instance (Mock or Java)
        """
        self.backend = backend
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

        if not self.entity_name:
            raise ValueError(f"{self.__class__.__name__} must define entity_name")
        if not self.entity_display_name:
            raise ValueError(f"{self.__class__.__name__} must define entity_display_name")

    # ========================================================================
    # CRUD OPERATIONS
    # ========================================================================

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Get all entities.

        Returns:
            List of entity dictionaries

        Raises:
            BackendException: On Backend errors
        """
        action = f"{self.entity_name}.getAll"
        self.logger.debug(f"Getting all {self.entity_display_name}s")

        try:
            result = self.backend.call(action)
            self.logger.info(f"Retrieved {len(result)} {self.entity_display_name}s")
            return result
        except BackendException as e:
            self.logger.error(f"Failed to get {self.entity_display_name}s: {e}")
            raise

    def get_by_id(self, entity_id: int) -> Optional[Dict[str, Any]]:
        """
        Get entity by ID.

        Args:
            entity_id: Entity ID

        Returns:
            Entity dictionary or None if not found
        """
        action = f"{self.entity_name}.getById"
        self.logger.debug(f"Getting {self.entity_display_name} #{entity_id}")

        try:
            result = self.backend.call(action, id=entity_id)
            self.logger.info(f"Retrieved {self.entity_display_name} #{entity_id}")
            return result
        except BackendNotFoundError:
            self.logger.warning(f"{self.entity_display_name} #{entity_id} not found")
            return None
        except BackendException as e:
            self.logger.error(f"Failed to get {self.entity_display_name} #{entity_id}: {e}")
            raise

    def create(self, **kwargs) -> Dict[str, Any]:
        """
        Create new entity.

        Args:
            **kwargs: Entity attributes

        Returns:
            Created entity dictionary

        Raises:
            BackendException: On Backend errors
        """
        action = f"{self.entity_name}.create"
        self.logger.debug(f"Creating {self.entity_display_name}: {kwargs}")

        try:
            result = self.backend.call(action, **kwargs)
            self.logger.info(f"Created {self.entity_display_name}: {result}")
            return result
        except BackendException as e:
            self.logger.error(f"Failed to create {self.entity_display_name}: {e}")
            raise

    def update(self, entity_id: int, **kwargs) -> Dict[str, Any]:
        """
        Update existing entity.

        Args:
            entity_id: Entity ID
            **kwargs: Attributes to update

        Returns:
            Updated entity dictionary

        Raises:
            BackendException: On Backend errors
        """
        action = f"{self.entity_name}.update"
        self.logger.debug(f"Updating {self.entity_display_name} #{entity_id}: {kwargs}")

        try:
            result = self.backend.call(action, id=entity_id, **kwargs)
            self.logger.info(f"Updated {self.entity_display_name} #{entity_id}")
            return result
        except BackendException as e:
            self.logger.error(f"Failed to update {self.entity_display_name} #{entity_id}: {e}")
            raise

    def delete(self, entity_id: int) -> bool:
        """
        Delete entity.

        Args:
            entity_id: Entity ID

        Returns:
            True if deleted successfully

        Raises:
            BackendException: On Backend errors
        """
        action = f"{self.entity_name}.delete"
        self.logger.debug(f"Deleting {self.entity_display_name} #{entity_id}")

        try:
            result = self.backend.call(action, id=entity_id)
            success = result.get("success", False)

            if success:
                self.logger.info(f"Deleted {self.entity_display_name} #{entity_id}")
            else:
                self.logger.warning(f"Delete {self.entity_display_name} #{entity_id} returned success=False")

            return success
        except BackendException as e:
            self.logger.error(f"Failed to delete {self.entity_display_name} #{entity_id}: {e}")
            raise

    def count(self) -> int:
        """
        Count total entities.

        Returns:
            Total count
        """
        try:
            entities = self.get_all()
            return len(entities)
        except BackendException:
            return 0

    # ========================================================================
    # VALIDATION HELPERS
    # ========================================================================

    def validate_required(self, **kwargs) -> None:
        """
        Validate required fields.

        Args:
            **kwargs: Field name -> value pairs

        Raises:
            BackendValidationError: If validation fails
        """
        missing = []

        for field, value in kwargs.items():
            if value is None or (isinstance(value, str) and not value.strip()):
                missing.append(field)

        if missing:
            raise BackendValidationError(
                f"Missing required fields for {self.entity_display_name}: {', '.join(missing)}"
            )