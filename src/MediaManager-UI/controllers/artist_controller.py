"""
Artist controller for MediaManager UI.

Manages artist-related operations and presentation logic.
"""

import logging
from typing import Dict, List, Optional

from .base_controller import BaseController
from backend.interface import BackendValidationError

logger = logging.getLogger(__name__)


class ArtistController(BaseController):
    """Controller for Artist entity."""

    entity_name = "artist"
    entity_display_name = "Artist"

    # ========================================================================
    # ARTIST-SPECIFIC OPERATIONS
    # ========================================================================

    def create_artist(self, name: str) -> Dict:
        """
        Create new artist.

        Args:
            name: Artist name

        Returns:
            Created artist

        Raises:
            BackendValidationError: If name is invalid
            BackendException: On other backend errors
        """
        # Validate
        self.validate_required(name=name)

        # Additional validation
        name = name.strip()
        if len(name) < 2:
            raise BackendValidationError("Artist name must be at least 2 characters")
        if len(name) > 200:
            raise BackendValidationError("Artist name must be at most 200 characters")

        # Create
        return self.create(name=name)

    def update_artist(self, artist_id: int, name: str) -> Dict:
        """
        Update artist name.

        Args:
            artist_id: Artist ID
            name: New name

        Returns:
            Updated artist
        """
        # Validate
        self.validate_required(name=name)

        name = name.strip()
        if len(name) < 2:
            raise BackendValidationError("Artist name must be at least 2 characters")
        if len(name) > 200:
            raise BackendValidationError("Artist name must be at most 200 characters")

        # Update
        return self.update(artist_id, name=name)

    def search_artists(self, query: str) -> List[Dict]:
        """
        Search artists by name (client-side filtering).

        Args:
            query: Search query

        Returns:
            List of matching artists
        """
        if not query:
            return self.get_all()

        query_lower = query.lower().strip()
        all_artists = self.get_all()

        return [
            a for a in all_artists
            if query_lower in a.get("name", "").lower()
        ]

    def artist_exists(self, name: str) -> bool:
        """
        Check if artist with given name exists.

        Args:
            name: Artist name to check

        Returns:
            True if exists, False otherwise
        """
        name_lower = name.lower().strip()
        all_artists = self.get_all()

        return any(
            a.get("name", "").lower() == name_lower
            for a in all_artists
        )

    def get_artists_sorted(self, reverse: bool = False) -> List[Dict]:
        """
        Get all artists sorted by name.

        Args:
            reverse: If True, sort Z-A. If False, sort A-Z

        Returns:
            Sorted list of artists
        """
        artists = self.get_all()
        return sorted(
            artists,
            key=lambda a: a.get("name", "").lower(),
            reverse=reverse
        )