"""
Library Viewer Widget.

Auto-refreshing library overview.
"""

import logging
from PySide6.QtWidgets import QTextEdit
from PySide6.QtCore import Slot

logger = logging.getLogger(__name__)


class LibraryViewerWidget(QTextEdit):
    """
    Library viewer with auto-refresh capability.
    """

    def __init__(self, controllers, parent=None):
        """
        Initialize library viewer.

        Args:
            controllers: Dictionary of controllers
            parent: Parent widget
        """
        super().__init__(parent)

        self.controllers = controllers
        self.setReadOnly(True)

        # Initial load
        self.refresh()

        logger.info("LibraryViewerWidget initialized")

    @Slot()
    @Slot(str)
    def refresh(self, entity_type=None):
        """
        Refresh library data.

        Args:
            entity_type: Optional - specific entity that changed
        """
        try:
            # Get fresh data
            genres = self.controllers['genre'].get_all()
            artists = self.controllers['artist'].get_all()
            albums = self.controllers['album'].get_all()

            # Build display text
            text = "📚 Library Viewer\n"
            text += "=" * 60 + "\n\n"

            text += f"🎸 Genres ({len(genres)}):\n"
            for genre in sorted(genres, key=lambda x: x['name']):
                text += f"  • {genre['name']}\n"

            text += f"\n🎤 Artists ({len(artists)}):\n"
            for artist in sorted(artists, key=lambda x: x['name']):
                text += f"  • {artist['name']}\n"

            text += f"\n💿 Albums ({len(albums)}):\n"
            for album in sorted(albums, key=lambda x: x['name']):
                year = f" ({album.get('year', 'N/A')})" if album.get('year') else ""
                text += f"  • {album['name']}{year}\n"

            # Update display
            self.setPlainText(text)

            if entity_type:
                logger.info(f"Library viewer refreshed (triggered by {entity_type})")
            else:
                logger.info("Library viewer refreshed")

        except Exception as e:
            logger.error(f"Failed to refresh library viewer: {e}", exc_info=True)
            self.setPlainText(f"Error loading library data:\n{e}")