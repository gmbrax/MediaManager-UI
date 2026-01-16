"""
Category list model for displaying genres, artists, albums, composers.

This model is reusable for any simple list display (sidebar categories).
"""

import logging
from typing import Any, List, Dict, Optional

from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex

logger = logging.getLogger(__name__)


class CategoryListModel(QAbstractListModel):
    """
    Generic list model for categories.

    Used for displaying:
    - Genres list
    - Artists list
    - Albums list
    - Composers list

    Each category shows: "All (N items)" header + list of items
    """

    def __init__(self, category_name: str = "Items", parent=None):
        """
        Initialize category list model.

        Args:
            category_name: Display name (e.g., "Genres", "Artists")
            parent: Parent QObject
        """
        super().__init__(parent)
        self.category_name = category_name
        self._data: List[Dict[str, Any]] = []
        self.logger = logging.getLogger(f"{__name__}.{category_name}")

    # ========================================================================
    # QAbstractListModel INTERFACE
    # ========================================================================

    def rowCount(self, parent=QModelIndex()) -> int:
        """Return number of rows."""
        if parent.isValid():
            return 0
        # +1 for "All (N items)" header
        return len(self._data) + 1

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        """
        Get data for an item.

        Row 0: "All (N items)" header
        Row 1+: Individual items
        """
        if not index.isValid():
            return None

        row = index.row()

        # Row 0: "All (N items)" header
        if row == 0:
            if role == Qt.DisplayRole:
                count = len(self._data)
                return f"All ({count} {self.category_name})"
            elif role == Qt.FontRole:
                # Make header bold
                from PySide6.QtGui import QFont
                font = QFont()
                font.setBold(True)
                return font
            elif role == Qt.UserRole:
                # Store special marker for "All"
                return {"type": "all", "category": self.category_name}

        # Row 1+: Individual items
        else:
            item_index = row - 1
            if item_index < 0 or item_index >= len(self._data):
                return None

            item = self._data[item_index]

            if role == Qt.DisplayRole:
                # Display the name
                return item.get("name", "Unknown")

            elif role == Qt.UserRole:
                # Store the full item data
                return item

            elif role == Qt.TextAlignmentRole:
                return Qt.AlignLeft | Qt.AlignVCenter

        return None

    # ========================================================================
    # DATA MANAGEMENT
    # ========================================================================

    def setData(self, data: List[Dict[str, Any]]) -> None:
        """
        Set model data.

        Args:
            data: List of item dictionaries (must have 'name' key)
        """
        self.beginResetModel()
        self._data = data if data else []
        self.endResetModel()
        self.logger.debug(f"Category '{self.category_name}' data set: {len(self._data)} items")

    def getData(self) -> List[Dict[str, Any]]:
        """Get current model data (without header)."""
        return self._data

    def getItem(self, row: int) -> Optional[Dict[str, Any]]:
        """
        Get item at specific row.

        Args:
            row: Row index (0 = "All" header, 1+ = items)

        Returns:
            Item dictionary or None
        """
        if row == 0:
            return {"type": "all", "category": self.category_name}

        item_index = row - 1
        if 0 <= item_index < len(self._data):
            return self._data[item_index]

        return None

    def clear(self) -> None:
        """Clear all data."""
        self.setData([])

    def refresh(self, data: List[Dict[str, Any]]) -> None:
        """
        Refresh model with new data.

        Args:
            data: New list of items
        """
        self.setData(data)

    def getItemId(self, row: int) -> Optional[int]:
        """
        Get item ID at specific row.

        Args:
            row: Row index

        Returns:
            Item ID or None
        """
        item = self.getItem(row)
        if item and item.get("type") != "all":
            return item.get("id")
        return None