"""
Java backend adapter for MediaManager UI.

This backend wraps the existing IPCManager to communicate with the Java core
via Unix socket + Protocol Buffers.
"""

import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from .interface import (
    IMediaManagerBackend,
    BackendConnectionError,
    BackendValidationError,
    BackendNotFoundError,
    BackendInternalError,
)

# Import IPC manager (seu código existente)
sys.path.insert(0, str(Path(__file__).parent.parent))
from ipc_manager import IPCManager

# Import protobuf messages
from proto import (
    genre_pb2,
    artist_pb2,
    album_pb2,
    composer_pb2,
    # Adicione outros conforme necessário
)

logger = logging.getLogger(__name__)


class JavaBackend(IMediaManagerBackend):
    """
    Java backend adapter using Unix socket + Protocol Buffers.

    This class wraps your existing IPCManager to conform to the
    IMediaManagerBackend interface.
    """

    def __init__(self, socket_path: Optional[str] = None):
        """
        Initialize Java backend.

        Args:
            socket_path: Path to Unix socket (default from config)
        """
        self._ipc = IPCManager(socket_path)
        logger.info(f"JavaBackend initialized (socket: {self._ipc.socket_path})")

    # ========================================================================
    # CONNECTION METHODS
    # ========================================================================

    def connect(self) -> None:
        """Connect to Java backend via Unix socket."""
        try:
            self._ipc.connect()
            logger.info("Connected to Java backend")
        except ConnectionError as e:
            raise BackendConnectionError(f"Failed to connect: {e}") from e
        except Exception as e:
            raise BackendConnectionError(f"Unexpected error: {e}") from e

    def disconnect(self) -> None:
        """Disconnect from Java backend."""
        try:
            self._ipc.disconnect()
            logger.info("Disconnected from Java backend")
        except Exception as e:
            logger.warning(f"Error during disconnect: {e}")

    def is_connected(self) -> bool:
        """Check if connected to Java backend."""
        return self._ipc.connected

    # ========================================================================
    # MAIN CALL METHOD
    # ========================================================================

    def call(self, action: str, **params) -> Any:
        """
        Execute action on Java backend.

        Args:
            action: Action name (e.g., "genre.create", "artist.getAll")
            **params: Action parameters

        Returns:
            Parsed result (dict or list)

        Raises:
            BackendConnectionError: Connection errors
            BackendValidationError: Validation errors (400)
            BackendNotFoundError: Not found (404)
            BackendInternalError: Internal errors (500)
        """
        if not self.is_connected():
            raise BackendConnectionError("Not connected to backend")

        logger.debug(f"JavaBackend.call({action}, {params})")

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
                f"Unsupported action: {action}",
                status_code=400,
                action=action
            )

        try:
            return handler(**params)
        except BackendConnectionError:
            raise
        except BackendValidationError:
            raise
        except BackendNotFoundError:
            raise
        except BackendInternalError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in {action}: {e}", exc_info=True)
            raise BackendInternalError(f"Unexpected error: {e}", action=action) from e

    # ========================================================================
    # GENRE HANDLERS
    # ========================================================================

    def _handle_genre_create(self, name: str) -> Dict[str, Any]:
        """Create genre via protobuf."""
        # Cria request protobuf
        request = genre_pb2.CreateGenreRequest()
        request.name = name

        # Envia via IPC
        request_id = self._ipc._send_request("genre.create", request.SerializeToString())
        response = self._ipc._receive_response()

        # Verifica status
        if response.status_code != 200:
            self._handle_error_response(response, "genre.create")

        # Parse response
        genre_response = genre_pb2.CreateGenreResponse()
        genre_response.ParseFromString(response.payload)

        # Converte pra dict
        return {
            "id": genre_response.genre.id,
            "name": genre_response.genre.name,
        }

    def _handle_genre_getAll(self) -> List[Dict[str, Any]]:
        """Get all genres via protobuf."""
        # Request vazio
        request = genre_pb2.GetGenreRequest()

        # Envia
        self._ipc._send_request("genre.getAll", request.SerializeToString())
        response = self._ipc._receive_response()

        # Verifica status
        if response.status_code != 200:
            self._handle_error_response(response, "genre.getAll")

        # Parse response
        genres_response = genre_pb2.GetGenreResponse()
        genres_response.ParseFromString(response.payload)

        # Converte lista
        return [
            {"id": g.id, "name": g.name}
            for g in genres_response.genres
        ]

    def _handle_genre_getById(self, id: int) -> Dict[str, Any]:
        """Get genre by ID via protobuf."""
        request = genre_pb2.GetGenreByIdRequest()
        request.id = id

        self._ipc._send_request("genre.getById", request.SerializeToString())
        response = self._ipc._receive_response()

        if response.status_code == 404:
            raise BackendNotFoundError(f"Genre with ID {id} not found", status_code=404)
        elif response.status_code != 200:
            self._handle_error_response(response, "genre.getById")

        genre_response = genre_pb2.GetGenreByIdResponse()
        genre_response.ParseFromString(response.payload)

        return {
            "id": genre_response.genre.id,
            "name": genre_response.genre.name,
        }

    def _handle_genre_update(self, id: int, name: str) -> Dict[str, Any]:
        """Update genre via protobuf."""
        request = genre_pb2.UpdateGenreRequest()
        request.id = id
        request.name = name

        self._ipc._send_request("genre.update", request.SerializeToString())
        response = self._ipc._receive_response()

        if response.status_code == 404:
            raise BackendNotFoundError(f"Genre with ID {id} not found", status_code=404)
        elif response.status_code != 200:
            self._handle_error_response(response, "genre.update")

        genre_response = genre_pb2.UpdateGenreResponse()
        genre_response.ParseFromString(response.payload)

        return {
            "id": genre_response.genre.id,
            "name": genre_response.genre.name,
        }

    def _handle_genre_delete(self, id: int) -> Dict[str, Any]:
        """Delete genre via protobuf."""
        request = genre_pb2.DeleteGenreRequest()
        request.id = id

        self._ipc._send_request("genre.delete", request.SerializeToString())
        response = self._ipc._receive_response()

        if response.status_code == 404:
            raise BackendNotFoundError(f"Genre with ID {id} not found", status_code=404)
        elif response.status_code != 200:
            self._handle_error_response(response, "genre.delete")

        delete_response = genre_pb2.DeleteGenreResponse()
        delete_response.ParseFromString(response.payload)

        return {
            "success": delete_response.success,
            "id": id,
        }

    # ========================================================================
    # ARTIST HANDLERS (similar pattern)
    # ========================================================================

    def _handle_artist_create(self, name: str) -> Dict[str, Any]:
        """Create artist via protobuf."""
        request = artist_pb2.CreateArtistRequest()
        request.name = name

        self._ipc._send_request("artist.create", request.SerializeToString())
        response = self._ipc._receive_response()

        if response.status_code != 200:
            self._handle_error_response(response, "artist.create")

        artist_response = artist_pb2.CreateArtistResponse()
        artist_response.ParseFromString(response.payload)

        return {
            "id": artist_response.artist.id,
            "name": artist_response.artist.name,
        }

    def _handle_artist_getAll(self) -> List[Dict[str, Any]]:
        """Get all artists via protobuf."""
        request = artist_pb2.GetArtistRequest()

        self._ipc._send_request("artist.getAll", request.SerializeToString())
        response = self._ipc._receive_response()

        if response.status_code != 200:
            self._handle_error_response(response, "artist.getAll")

        artists_response = artist_pb2.GetArtistResponse()
        artists_response.ParseFromString(response.payload)

        return [
            {"id": a.id, "name": a.name}
            for a in artists_response.artists
        ]

    def _handle_artist_getById(self, id: int) -> Dict[str, Any]:
        """Get artist by ID via protobuf."""
        request = artist_pb2.GetArtistByIdRequest()
        request.id = id

        self._ipc._send_request("artist.getById", request.SerializeToString())
        response = self._ipc._receive_response()

        if response.status_code == 404:
            raise BackendNotFoundError(f"Artist with ID {id} not found", status_code=404)
        elif response.status_code != 200:
            self._handle_error_response(response, "artist.getById")

        artist_response = artist_pb2.GetArtistByIdResponse()
        artist_response.ParseFromString(response.payload)

        return {
            "id": artist_response.artist.id,
            "name": artist_response.artist.name,
        }

    def _handle_artist_update(self, id: int, name: str) -> Dict[str, Any]:
        """Update artist via protobuf."""
        request = artist_pb2.UpdateArtistRequest()
        request.id = id
        request.name = name

        self._ipc._send_request("artist.update", request.SerializeToString())
        response = self._ipc._receive_response()

        if response.status_code == 404:
            raise BackendNotFoundError(f"Artist with ID {id} not found", status_code=404)
        elif response.status_code != 200:
            self._handle_error_response(response, "artist.update")

        artist_response = artist_pb2.UpdateArtistResponse()
        artist_response.ParseFromString(response.payload)

        return {
            "id": artist_response.artist.id,
            "name": artist_response.artist.name,
        }

    def _handle_artist_delete(self, id: int) -> Dict[str, Any]:
        """Delete artist via protobuf."""
        request = artist_pb2.DeleteArtistRequest()
        request.id = id

        self._ipc._send_request("artist.delete", request.SerializeToString())
        response = self._ipc._receive_response()

        if response.status_code == 404:
            raise BackendNotFoundError(f"Artist with ID {id} not found", status_code=404)
        elif response.status_code != 200:
            self._handle_error_response(response, "artist.delete")

        delete_response = artist_pb2.DeleteArtistResponse()
        delete_response.ParseFromString(response.payload)

        return {
            "success": delete_response.success,
            "id": id,
        }

    # ========================================================================
    # ALBUM HANDLERS (basic implementation)
    # ========================================================================

    def _handle_album_getAll(self) -> List[Dict[str, Any]]:
        """Get all albums via protobuf."""
        request = album_pb2.GetAlbumRequest()

        self._ipc._send_request("album.getAll", request.SerializeToString())
        response = self._ipc._receive_response()

        if response.status_code != 200:
            self._handle_error_response(response, "album.getAll")

        albums_response = album_pb2.GetAlbumResponse()
        albums_response.ParseFromString(response.payload)

        return [
            {
                "id": a.id,
                "name": a.name,
                "year": a.year if a.HasField("year") else None,
            }
            for a in albums_response.albums
        ]

    # TODO: Adicionar mais handlers conforme necessário
    # - album.create, album.update, album.delete, album.getById
    # - composer.*, track.*, disc.*, etc.

    # ========================================================================
    # TEST COMMANDS
    # ========================================================================

    def echo(self, message: str) -> str:
        """Echo test command (usa seu método existente)."""
        return self._ipc.echo(message)

    def heartbeat(self) -> int:
        """Heartbeat test command (usa seu método existente)."""
        return self._ipc.heartbeat()

    def _handle_echo(self, message: str) -> Dict[str, Any]:
        """Handler for echo via call()."""
        result = self.echo(message)
        return {"message": result}

    def _handle_heartbeat(self) -> Dict[str, Any]:
        """Handler for heartbeat via call()."""
        rtt = self.heartbeat()
        return {"rtt": rtt}

    # ========================================================================
    # ERROR HANDLING
    # ========================================================================

    def _handle_error_response(self, response, action: str) -> None:
        """
        Handle error response from Java backend.

        Args:
            response: Protocol buffer response
            action: Action that failed

        Raises:
            BackendValidationError: For 400 errors
            BackendNotFoundError: For 404 errors
            BackendInternalError: For 500 errors
        """
        status_code = response.status_code
        error_message = response.payload.decode('utf-8', errors='ignore')

        if status_code == 400:
            raise BackendValidationError(
                error_message,
                status_code=status_code,
                action=action
            )
        elif status_code == 404:
            raise BackendNotFoundError(
                error_message,
                status_code=status_code,
                action=action
            )
        elif status_code >= 500:
            raise BackendInternalError(
                error_message,
                status_code=status_code,
                action=action
            )
        else:
            raise BackendInternalError(
                f"Unexpected status code {status_code}: {error_message}",
                status_code=status_code,
                action=action
            )

    # ========================================================================
    # CONTEXT MANAGER
    # ========================================================================

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()