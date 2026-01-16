"""
Backend abstraction layer for MediaManager UI.

This package provides an abstract interface for backend communication,
allowing easy switching between MockBackend (development/testing) and
JavaBackend (production with real Java core).
"""

from .interface import (
    IMediaManagerBackend,
    BackendException,
    BackendConnectionError,
    BackendValidationError,
    BackendNotFoundError,
    BackendInternalError,
)
from .mock_backend import MockBackend

# JavaBackend importado só quando necessário (evita erro se Java não tiver rodando)
__all__ = [
    'IMediaManagerBackend',
    'BackendException',
    'BackendConnectionError',
    'BackendValidationError',
    'BackendNotFoundError',
    'BackendInternalError',
    'MockBackend',
]