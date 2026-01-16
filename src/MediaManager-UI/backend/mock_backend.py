"""
Mock backend for MediaManager UI development.

This backend provides fake data for development and testing without
requiring the Java core to be running.
"""

import logging
import time
from typing import Any, Dict, List, Optional

from .interface import (
    IMediaManagerBackend,
    BackendConnectionError,
    BackendValidationError,
    BackendNotFoundError,
    BackendInternalError,
)

logger = logging.getLogger(__name__)


class MockBackend(IMediaManagerBackend):
    """
    Mock backend with in-memory fake data.

    This allows UI development without the Java backend running.
    Data is reset on each restart (not persistent).
    """

    def __init__(self):
        """Initialize mock backend with fake data."""
        self._connected = False
        self._next_id = 100  # Start IDs at 100 to avoid conflicts

        # In-memory "database"
        self._data = {
            "genres": self._init_genres(),
            "artists": self._init_artists(),
            "composers": self._init_composers(),
            "albums": self._init_albums(),
            "tracks": self._init_tracks(),
            "bit_depths": self._init_bit_depths(),
            "bit_rates": self._init_bit_rates(),
            "sampling_rates": self._init_sampling_rates(),
            "album_types": self._init_album_types(),
        }

        logger.info("MockBackend initialized with fake data")

    # ========================================================================
    # CONNECTION METHODS
    # ========================================================================

    def connect(self) -> None:
        """Simula conexão (sempre sucesso)."""
        logger.info("MockBackend: connect() - simulated")
        time.sleep(0.1)  # Simula delay de rede
        self._connected = True

    def disconnect(self) -> None:
        """Simula desconexão."""
        logger.info("MockBackend: disconnect() - simulated")
        self._connected = False

    def is_connected(self) -> bool:
        """Sempre conectado no mock."""
        return self._connected

    # ========================================================================
    # MAIN CALL METHOD
    # ========================================================================

    def call(self, action: str, **params) -> Any:
        """
        Execute mock action.

        Args:
            action: Action name (e.g., "genre.create", "artist.getAll")
            **params: Action parameters

        Returns:
            Mock result

        Raises:
            BackendConnectionError: If not connected
            BackendValidationError: If validation fails
            BackendNotFoundError: If entity not found
        """
        if not self._connected:
            raise BackendConnectionError("Not connected to backend")

        logger.debug(f"MockBackend.call({action}, {params})")

        # Parse action
        parts = action.split(".")
        if len(parts) != 2:
            raise BackendValidationError(f"Invalid action format: {action}")

        entity_type, operation = parts

        # Route to handler
        handler_name = f"_handle_{entity_type}_{operation}"
        handler = getattr(self, handler_name, None)

        if not handler:
            raise BackendValidationError(
                f"Unknown action: {action}",
                status_code=400,
                action=action
            )

        # Simula delay de rede
        time.sleep(0.05)

        return handler(**params)

    # ========================================================================
    # GENRE HANDLERS
    # ========================================================================

    def _handle_genre_create(self, name: str) -> Dict[str, Any]:
        """Create genre."""
        if not name:
            raise BackendValidationError("Genre name is required")

        genre = {
            "id": self._next_id,
            "name": name,
        }
        self._next_id += 1

        self._data["genres"].append(genre)
        logger.info(f"Created genre: {genre}")
        return genre

    def _handle_genre_getAll(self) -> List[Dict[str, Any]]:
        """Get all genres."""
        return self._data["genres"]

    def _handle_genre_getById(self, id: int) -> Dict[str, Any]:
        """Get genre by ID."""
        for genre in self._data["genres"]:
            if genre["id"] == id:
                return genre

        raise BackendNotFoundError(f"Genre with ID {id} not found", status_code=404)

    def _handle_genre_update(self, id: int, name: str) -> Dict[str, Any]:
        """Update genre."""
        for genre in self._data["genres"]:
            if genre["id"] == id:
                genre["name"] = name
                logger.info(f"Updated genre: {genre}")
                return genre

        raise BackendNotFoundError(f"Genre with ID {id} not found", status_code=404)

    def _handle_genre_delete(self, id: int) -> Dict[str, Any]:
        """Delete genre."""
        for i, genre in enumerate(self._data["genres"]):
            if genre["id"] == id:
                deleted = self._data["genres"].pop(i)
                logger.info(f"Deleted genre: {deleted}")
                return {"success": True, "id": id}

        raise BackendNotFoundError(f"Genre with ID {id} not found", status_code=404)

    # ========================================================================
    # ARTIST HANDLERS
    # ========================================================================

    def _handle_artist_create(self, name: str) -> Dict[str, Any]:
        """Create artist."""
        if not name:
            raise BackendValidationError("Artist name is required")

        artist = {
            "id": self._next_id,
            "name": name,
        }
        self._next_id += 1

        self._data["artists"].append(artist)
        logger.info(f"Created artist: {artist}")
        return artist

    def _handle_artist_getAll(self) -> List[Dict[str, Any]]:
        """Get all artists."""
        return self._data["artists"]

    def _handle_artist_getById(self, id: int) -> Dict[str, Any]:
        """Get artist by ID."""
        for artist in self._data["artists"]:
            if artist["id"] == id:
                return artist

        raise BackendNotFoundError(f"Artist with ID {id} not found", status_code=404)

    def _handle_artist_update(self, id: int, name: str) -> Dict[str, Any]:
        """Update artist."""
        for artist in self._data["artists"]:
            if artist["id"] == id:
                artist["name"] = name
                logger.info(f"Updated artist: {artist}")
                return artist

        raise BackendNotFoundError(f"Artist with ID {id} not found", status_code=404)

    def _handle_artist_delete(self, id: int) -> Dict[str, Any]:
        """Delete artist."""
        for i, artist in enumerate(self._data["artists"]):
            if artist["id"] == id:
                deleted = self._data["artists"].pop(i)
                logger.info(f"Deleted artist: {deleted}")
                return {"success": True, "id": id}

        raise BackendNotFoundError(f"Artist with ID {id} not found", status_code=404)

    # ========================================================================
    # ALBUM HANDLERS
    # ========================================================================

    def _handle_album_create(
            self,
            name: str,
            year: Optional[int] = None,
            **kwargs
    ) -> Dict[str, Any]:
        """Create album."""
        if not name:
            raise BackendValidationError("Album name is required")

        album = {
            "id": self._next_id,
            "name": name,
            "year": year,
        }
        self._next_id += 1

        self._data["albums"].append(album)
        logger.info(f"Created album: {album}")
        return album

    def _handle_album_getAll(self) -> List[Dict[str, Any]]:
        """Get all albums."""
        return self._data["albums"]

    def _handle_album_getById(self, id: int) -> Dict[str, Any]:
        """Get album by ID."""
        for album in self._data["albums"]:
            if album["id"] == id:
                return album

        raise BackendNotFoundError(f"Album with ID {id} not found", status_code=404)

    def _handle_album_update(
            self,
            id: int,
            name: Optional[str] = None,
            year: Optional[int] = None,
            **kwargs
    ) -> Dict[str, Any]:
        """Update album."""
        for album in self._data["albums"]:
            if album["id"] == id:
                if name is not None:
                    album["name"] = name
                if year is not None:
                    album["year"] = year
                logger.info(f"Updated album: {album}")
                return album

        raise BackendNotFoundError(f"Album with ID {id} not found", status_code=404)

    def _handle_album_delete(self, id: int) -> Dict[str, Any]:
        """Delete album."""
        for i, album in enumerate(self._data["albums"]):
            if album["id"] == id:
                deleted = self._data["albums"].pop(i)
                logger.info(f"Deleted album: {deleted}")
                return {"success": True, "id": id}

        raise BackendNotFoundError(f"Album with ID {id} not found", status_code=404)

    # ========================================================================
    # TEST COMMANDS
    # ========================================================================

    def _handle_echo(self, message: str) -> Dict[str, Any]:
        """Echo command."""
        logger.debug(f"Echo: {message}")
        return {"message": message}

    def _handle_heartbeat(self) -> Dict[str, Any]:
        """Heartbeat command."""
        import time
        start = time.time()
        time.sleep(0.001)  # Simula processamento
        rtt = int((time.time() - start) * 1000)
        logger.debug(f"Heartbeat: {rtt}ms")
        return {"rtt": rtt}

    # ========================================================================
    # INITIAL FAKE DATA
    # ========================================================================

    def _init_genres(self) -> List[Dict[str, Any]]:
        """Initialize fake genres."""
        return [
            {"id": 1, "name": "Rock"},
            {"id": 2, "name": "Jazz"},
            {"id": 3, "name": "Classical"},
            {"id": 4, "name": "Electronic"},
            {"id": 5, "name": "Metal"},
            {"id": 6, "name": "Pop"},
            {"id": 7, "name": "Hip Hop"},
            {"id": 8, "name": "Blues"},
        ]

    def _init_artists(self) -> List[Dict[str, Any]]:
        """Initialize fake artists."""
        return [
            {"id": 10, "name": "Pink Floyd"},
            {"id": 11, "name": "The Beatles"},
            {"id": 12, "name": "Led Zeppelin"},
            {"id": 13, "name": "Miles Davis"},
            {"id": 14, "name": "Bach"},
            {"id": 15, "name": "Metallica"},
            {"id": 16, "name": "Daft Punk"},
        ]

    def _init_composers(self) -> List[Dict[str, Any]]:
        """Initialize fake composers."""
        return [
            {"id": 20, "name": "David Gilmour"},
            {"id": 21, "name": "Roger Waters"},
            {"id": 22, "name": "John Lennon"},
            {"id": 23, "name": "Paul McCartney"},
        ]

    def _init_albums(self) -> List[Dict[str, Any]]:
        """Initialize fake albums."""
        return [
            {"id": 30, "name": "The Dark Side of the Moon", "year": 1973},
            {"id": 31, "name": "Abbey Road", "year": 1969},
            {"id": 32, "name": "Led Zeppelin IV", "year": 1971},
            {"id": 33, "name": "Kind of Blue", "year": 1959},
            {"id": 34, "name": "Master of Puppets", "year": 1986},
        ]

    def _init_tracks(self) -> List[Dict[str, Any]]:
        """Initialize fake tracks."""
        return [
            {"id": 40, "name": "Speak to Me", "track_number": 1, "duration": 90},
            {"id": 41, "name": "Breathe", "track_number": 2, "duration": 163},
            {"id": 42, "name": "Time", "track_number": 4, "duration": 413},
            {"id": 43, "name": "Money", "track_number": 6, "duration": 382},
        ]

    def _init_bit_depths(self) -> List[Dict[str, Any]]:
        """Initialize fake bit depths."""
        return [
            {"id": 50, "value": 16},
            {"id": 51, "value": 24},
            {"id": 52, "value": 32},
        ]

    def _init_bit_rates(self) -> List[Dict[str, Any]]:
        """Initialize fake bit rates."""
        return [
            {"id": 60, "value": 128},
            {"id": 61, "value": 192},
            {"id": 62, "value": 256},
            {"id": 63, "value": 320},
        ]

    def _init_sampling_rates(self) -> List[Dict[str, Any]]:
        """Initialize fake sampling rates."""
        return [
            {"id": 70, "value": 44100},
            {"id": 71, "value": 48000},
            {"id": 72, "value": 96000},
            {"id": 73, "value": 192000},
        ]

    def _init_album_types(self) -> List[Dict[str, Any]]:
        """Initialize fake album types."""
        return [
            {"id": 80, "type": "Studio Album"},
            {"id": 81, "type": "Live Album"},
            {"id": 82, "type": "Compilation"},
            {"id": 83, "type": "EP"},
            {"id": 84, "type": "Single"},
        ]