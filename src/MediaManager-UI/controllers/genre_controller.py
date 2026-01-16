"""
Genre controller for MediaManager UI.

Manages genre-related operations and presentation logic.
"""

import logging
from typing import Dict, List, Optional

from .base_controller import BaseController
from backend.interface import BackendValidationError

logger = logging.getLogger(__name__)


class GenreController(BaseController):
    """Controller for Genre entity."""

    entity_name = "genre"
    entity_display_name = "Genre"

    # ========================================================================
    # GENRE-SPECIFIC OPERATIONS
    # ========================================================================

    def create_genre(self, name: str) -> Dict:
        """
        Create new genre.

        Args:
            name: Genre name

        Returns:
            Created genre

        Raises:
            BackendValidationError: If name is invalid
            BackendException: On other Backend errors
        """
        # Validate
        self.validate_required(name=name)

        # Additional validation
        name = name.strip()
        if len(name) < 2:
            raise BackendValidationError("Genre name must be at least 2 characters")
        if len(name) > 100:
            raise BackendValidationError("Genre name must be at most 100 characters")

        # Create
        return self.create(name=name)

    def update_genre(self, genre_id: int, name: str) -> Dict:
        """
        Update genre name.

        Args:
            genre_id: Genre ID
            name: New name

        Returns:
            Updated genre
        """
        # Validate
        self.validate_required(name=name)

        name = name.strip()
        if len(name) < 2:
            raise BackendValidationError("Genre name must be at least 2 characters")
        if len(name) > 100:
            raise BackendValidationError("Genre name must be at most 100 characters")

        # Update
        return self.update(genre_id, name=name)

    def search_genres(self, query: str) -> List[Dict]:
        """
        Search genres by name (client-side filtering).

        Args:
            query: Search query

        Returns:
            List of matching genres
        """
        if not query:
            return self.get_all()

        query_lower = query.lower().strip()
        all_genres = self.get_all()

        return [
            g for g in all_genres
            if query_lower in g.get("name", "").lower()
        ]

    def genre_exists(self, name: str) -> bool:
        """
        Check if genre with given name exists.

        Args:
            name: Genre name to check

        Returns:
            True if exists, False otherwise
        """
        name_lower = name.lower().strip()
        all_genres = self.get_all()

        return any(
            g.get("name", "").lower() == name_lower
            for g in all_genres
        )