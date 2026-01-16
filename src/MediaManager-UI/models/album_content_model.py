"""
Album content model for displaying albums and tracks in iTunes-style layout.

This model displays:
- Album covers in grid mode
- Album info + track list when album is selected
"""

import logging
from typing import Any, List, Dict, Optional

from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex, QSize
from PySide6.QtGui import QPixmap, QIcon

logger = logging.getLogger(__name__)


class AlbumContentModel(QAbstractListModel):
    """
    Model for displaying album content.

    Two display modes:
    1. Grid mode: Shows album covers in a grid (IconMode)
    2. Track mode: Shows album + track list (ListMode)
    """

    # Display modes
    MODE_GRID = "grid"  # Album covers grid
    MODE_TRACKS = "tracks"  # Album + track list

    def __init__(self, parent=None):
        """Initialize album content model."""
        super().__init__(parent)
        self._data: List[Dict[str, Any]] = []
        self._mode = self.MODE_GRID
        self._selected_album: Optional[Dict[str, Any]] = None
        self._tracks: List[Dict[str, Any]] = []
        self.logger = logging.getLogger(__name__)

    # ========================================================================
    # QAbstractListModel INTERFACE
    # ========================================================================

    def rowCount(self, parent=QModelIndex()) -> int:
        """Return number of rows based on mode."""
        if parent.isValid():
            return 0

        if self._mode == self.MODE_GRID:
            # Show albums
            return len(self._data)
        else:
            # Show tracks of selected album
            return len(self._tracks)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        """Get data for an item based on display mode."""
        if not index.isValid():
            return None

        row = index.row()

        if self._mode == self.MODE_GRID:
            return self._getAlbumData(row, role)
        else:
            return self._getTrackData(row, role)

    def _getAlbumData(self, row: int, role: int) -> Any:
        """Get album data for grid display."""
        if row < 0 or row >= len(self._data):
            return None

        album = self._data[row]

        if role == Qt.DisplayRole:
            # Album name + artist
            name = album.get("name", "Unknown Album")
            # Could add artist here if available
            return name

        elif role == Qt.DecorationRole:
            # Album cover icon
            # TODO: Load actual album art from file/database
            # For now, return placeholder
            return self._getAlbumIcon(album)

        elif role == Qt.SizeHintRole:
            # Size of album tile (200x240: 200 for cover + 40 for text)
            return QSize(200, 240)

        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        elif role == Qt.UserRole:
            # Store full album data
            return album

        return None

    def _getTrackData(self, row: int, role: int) -> Any:
        """Get track data for list display."""
        if row < 0 or row >= len(self._tracks):
            return None

        track = self._tracks[row]

        if role == Qt.DisplayRole:
            # Track number and name
            track_num = track.get("track_number", row + 1)
            name = track.get("name", "Unknown Track")
            duration = track.get("duration", "0:00")
            return f"{track_num}  {name}  {duration}"

        elif role == Qt.DecorationRole:
            # Small checkmark icon if track is available
            # TODO: Implement checkmark icon
            return None

        elif role == Qt.UserRole:
            # Store full track data
            return track

        return None

    def _getAlbumIcon(self, album: Dict[str, Any]) -> QIcon:
        """
        Get album cover icon.

        TODO: Implement actual album art loading
        For now returns placeholder.
        """
        # Placeholder - return empty icon
        # In real implementation:
        # 1. Check if album has 'cover_path'
        # 2. Load image from file
        # 3. Create QPixmap
        # 4. Return QIcon(pixmap)
        return QIcon()

    # ========================================================================
    # MODE MANAGEMENT
    # ========================================================================

    def setMode(self, mode: str) -> None:
        """
        Set display mode.

        Args:
            mode: MODE_GRID or MODE_TRACKS
        """
        if mode not in (self.MODE_GRID, self.MODE_TRACKS):
            self.logger.warning(f"Invalid mode: {mode}")
            return

        if self._mode != mode:
            self.beginResetModel()
            self._mode = mode
            self.endResetModel()
            self.logger.debug(f"Display mode changed to: {mode}")

    def getMode(self) -> str:
        """Get current display mode."""
        return self._mode

    # ========================================================================
    # DATA MANAGEMENT
    # ========================================================================

    def setAlbums(self, albums: List[Dict[str, Any]]) -> None:
        """
        Set album data (grid mode).

        Args:
            albums: List of album dictionaries
        """
        self.beginResetModel()
        self._data = albums if albums else []
        self._mode = self.MODE_GRID
        self._selected_album = None
        self._tracks = []
        self.endResetModel()
        self.logger.debug(f"Albums set: {len(self._data)} albums")

    def setTracks(self, album: Dict[str, Any], tracks: List[Dict[str, Any]]) -> None:
        """
        Set track data for an album (track mode).

        Args:
            album: Selected album dictionary
            tracks: List of track dictionaries
        """
        self.beginResetModel()
        self._mode = self.MODE_TRACKS
        self._selected_album = album
        self._tracks = tracks if tracks else []
        self.endResetModel()
        self.logger.debug(f"Tracks set for album '{album.get('name')}': {len(self._tracks)} tracks")

    def getSelectedAlbum(self) -> Optional[Dict[str, Any]]:
        """Get currently selected album (in track mode)."""
        return self._selected_album

    def getAlbum(self, row: int) -> Optional[Dict[str, Any]]:
        """
        Get album at specific row (grid mode).

        Args:
            row: Row index

        Returns:
            Album dictionary or None
        """
        if self._mode == self.MODE_GRID and 0 <= row < len(self._data):
            return self._data[row]
        return None

    def getTrack(self, row: int) -> Optional[Dict[str, Any]]:
        """
        Get track at specific row (track mode).

        Args:
            row: Row index

        Returns:
            Track dictionary or None
        """
        if self._mode == self.MODE_TRACKS and 0 <= row < len(self._tracks):
            return self._tracks[row]
        return None

    def clear(self) -> None:
        """Clear all data and reset to grid mode."""
        self.beginResetModel()
        self._data = []
        self._tracks = []
        self._selected_album = None
        self._mode = self.MODE_GRID
        self.endResetModel()