"""
Controllers for MediaManager UI.

Controllers manage presentation logic and coordinate between
the UI layer and the Backend layer.
"""

from .base_controller import BaseController
from .genre_controller import GenreController
from .artist_controller import ArtistController
from .album_controller import AlbumController

__all__ = [
    'BaseController',
    'GenreController',
    'ArtistController',
    'AlbumController',
]