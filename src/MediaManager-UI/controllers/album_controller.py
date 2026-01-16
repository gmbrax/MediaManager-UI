"""
Album controller for MediaManager UI.

Manages album-related operations and presentation logic.
"""

import logging
from typing import Dict, List, Optional

from .base_controller import BaseController
from backend.interface import BackendValidationError

logger = logging.getLogger(__name__)


class AlbumController(BaseController):
    """Controller for Album entity."""

    entity_name = "album"
    entity_display_name = "Album"

    # ========================================================================
    # ALBUM-SPECIFIC OPERATIONS
    # ========================================================================

    def create_album(
            self,
            name: str,
            year: Optional[int] = None,
            **kwargs
    ) -> Dict:
        """
        Create new album.

        Args:
            name: Album name
            year: Release year (optional)
            **kwargs: Additional album attributes

        Returns:
            Created album

        Raises:
            BackendValidationError: If validation fails
            BackendException: On other backend errors
        """
        # Validate required
        self.validate_required(name=name)

        # Validate name
        name = name.strip()
        if len(name) < 1:
            raise BackendValidationError("Album name cannot be empty")
        if len(name) > 255:
            raise BackendValidationError("Album name must be at most 255 characters")

        # Validate year
        if year is not None:
            if not isinstance(year, int):
                raise BackendValidationError("Year must be an integer")
            if year < 1900 or year > 2100:
                raise BackendValidationError("Year must be between 1900 and 2100")

        # Create
        return self.create(name=name, year=year, **kwargs)

    def update_album(
            self,
            album_id: int,
            name: Optional[str] = None,
            year: Optional[int] = None,
            **kwargs
    ) -> Dict:
        """
        Update album.

        Args:
            album_id: Album ID
            name: New name (optional)
            year: New year (optional)
            **kwargs: Additional attributes to update

        Returns:
            Updated album
        """
        # Validate name if provided
        if name is not None:
            name = name.strip()
            if len(name) < 1:
                raise BackendValidationError("Album name cannot be empty")
            if len(name) > 255:
                raise BackendValidationError("Album name must be at most 255 characters")

        # Validate year if provided
        if year is not None:
            if not isinstance(year, int):
                raise BackendValidationError("Year must be an integer")
            if year < 1900 or year > 2100:
                raise BackendValidationError("Year must be between 1900 and 2100")

        # Build update dict
        update_data = {}
        if name is not None:
            update_data['name'] = name
        if year is not None:
            update_data['year'] = year
        update_data.update(kwargs)

        # Update
        return self.update(album_id, **update_data)

    def search_albums(self, query: str) -> List[Dict]:
        """
        Search albums by name (client-side filtering).

        Args:
            query: Search query

        Returns:
            List of matching albums
        """
        if not query:
            return self.get_all()

        query_lower = query.lower().strip()
        all_albums = self.get_all()

        return [
            a for a in all_albums
            if query_lower in a.get("name", "").lower()
        ]

    def get_albums_by_year(self, year: int) -> List[Dict]:
        """
        Get albums released in specific year.

        Args:
            year: Release year

        Returns:
            List of albums from that year
        """
        all_albums = self.get_all()
        return [
            a for a in all_albums
            if a.get("year") == year
        ]

    def get_albums_sorted(
            self,
            sort_by: str = "name",
            reverse: bool = False
    ) -> List[Dict]:
        """
        Get albums sorted by specified field.

        Args:
            sort_by: Field to sort by ("name" or "year")
            reverse: If True, sort descending

        Returns:
            Sorted list of albums
        """
        albums = self.get_all()

        if sort_by == "name":
            return sorted(
                albums,
                key=lambda a: a.get("name", "").lower(),
                reverse=reverse
            )
        elif sort_by == "year":
            # Albums without year go to end
            return sorted(
                albums,
                key=lambda a: (a.get("year") is None, a.get("year") or 0),
                reverse=reverse
            )
        else:
            return albums

    def album_exists(self, name: str, year: Optional[int] = None) -> bool:
        """
        Check if album exists.

        Args:
            name: Album name
            year: Optional year to match

        Returns:
            True if exists, False otherwise
        """
        name_lower = name.lower().strip()
        all_albums = self.get_all()

        for album in all_albums:
            if album.get("name", "").lower() == name_lower:
                if year is None or album.get("year") == year:
                    return True

        return False