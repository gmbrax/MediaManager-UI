"""
MediaManager - Main entry point.

Modern music library manager with iTunes-style interface.
"""

import sys
import logging
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer, QThread, Signal

# Setup logging
from config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

# Import components
from views.splash_screen import SplashScreen
from backend.mock_backend import MockBackend
from controllers.genre_controller import GenreController
from controllers.artist_controller import ArtistController
from controllers.album_controller import AlbumController


class BackendInitThread(QThread):
    """Thread for initializing backend without blocking UI."""

    # Signals
    progress = Signal(str)  # Progress message
    finished = Signal()  # Initialization complete
    error = Signal(str)  # Error occurred

    def __init__(self, use_mock=True):
        super().__init__()
        self.use_mock = use_mock
        self.backend = None
        self.controllers = {}


    def run(self):
        """Initialize backend and controllers."""
        try:
            # Step 1: Initialize backend
            self.progress.emit("Initializing backend...")

            if self.use_mock:
                self.backend = MockBackend()
                logger.info("Using MockBackend")
            else:
                # TODO: Initialize JavaBackend
                from backend.java_backend import JavaBackend
                self.backend = JavaBackend()
                logger.info("Using JavaBackend")

            # CONECTA O BACKEND! ← FALTAVA ISSO!
            self.backend.connect()
            logger.info("Backend connected")

            QThread.msleep(500)  # Simulate work

            # Step 2: Initialize controllers
            self.progress.emit("Loading controllers...")

            self.controllers['genre'] = GenreController(self.backend)
            self.controllers['artist'] = ArtistController(self.backend)
            self.controllers['album'] = AlbumController(self.backend)

            logger.info("Controllers initialized")
            QThread.msleep(500)

            # Step 3: Load initial data
            self.progress.emit("Loading library data...")

            # Preload some data
            self.controllers['genre'].get_all()
            self.controllers['artist'].get_all()
            self.controllers['album'].get_all()

            logger.info("Initial data loaded")
            QThread.msleep(500)

            # Done!
            self.progress.emit("Ready!")
            self.finished.emit()

        except Exception as e:
            logger.error(f"Backend initialization failed: {e}", exc_info=True)
            self.error.emit(str(e))


def main():
    """Main entry point."""

    # Parse arguments
    import argparse
    parser = argparse.ArgumentParser(description='MediaManager - Music Library Manager')
    parser.add_argument('--mock', action='store_true', help='Use mock backend')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    args = parser.parse_args()

    # Set log level
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    logger.info("=" * 60)
    logger.info("MediaManager Starting")
    logger.info("=" * 60)

    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("MediaManager")
    app.setOrganizationName("MediaManager")

    # Show splash screen
    splash = SplashScreen()
    splash.show()

    # Process events to show splash immediately
    app.processEvents()

    logger.info("Splash screen displayed")

    # Initialize backend in thread
    init_thread = BackendInitThread(use_mock=args.mock or True)

    # Connect signals
    def on_progress(message):
        splash.showMessage(message)
        logger.info(f"Init progress: {message}")

    def on_finished():
        logger.info("Backend initialization complete")

        # Create and show main window
        from views.main_window import MainWindow

        # IMPORTANTE: Salvar referência pra não ser garbage collected!
        global main_window
        main_window = MainWindow(init_thread.backend, init_thread.controllers)
        main_window.show()

        # Close splash
        splash.finish(main_window)

        logger.info("Main window displayed")

    def on_error(error_msg):
        logger.error(f"Initialization error: {error_msg}")
        splash.showMessage(f"Error: {error_msg}")
        QTimer.singleShot(3000, lambda: app.quit())

    init_thread.progress.connect(on_progress)
    init_thread.finished.connect(on_finished)
    init_thread.error.connect(on_error)

    # Start initialization
    init_thread.start()

    # Run application
    exit_code = app.exec()

    logger.info("=" * 60)
    logger.info("MediaManager Shutdown")
    logger.info("=" * 60)

    return exit_code


if __name__ == '__main__':
    sys.exit(main())