"""
MainWindow for MediaManager.

SAP-style interface with task tree and MDI area.
"""

import logging
from typing import Dict

from PySide6.QtWidgets import (
    QMainWindow, QTreeWidgetItem, QMdiSubWindow, QListWidget
)
from PySide6.QtCore import Qt, Slot

from backend.interface import IMediaManagerBackend
from ui.ui_mainwindow import Ui_MediaManagerMain


logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Main application window.

    Layout (from .ui file):
    - Left: Task tree (QTreeWidget)
    - Right: MDI Area (QMdiArea)
    - Top: Menu bar
    - Bottom: Status bar
    """

    def __init__(self, backend: IMediaManagerBackend, controllers: Dict):
        """
        Initialize main window.

        Args:
            backend: Backend instance
            controllers: Dictionary of controllers
        """
        super().__init__()

        self.backend = backend
        self.controllers = controllers

        # Setup UI from generated file
        self.ui = Ui_MediaManagerMain()
        self.ui.setupUi(self)

        # Setup task tree
        self._setup_task_tree()

        # Connect signals
        self._connect_signals()

        logger.info("MainWindow initialized")

    def _setup_task_tree(self):
        """Setup task tree with Library and Actions."""

        # Clear existing items
        self.ui.taskTreeWidget.clear()

        # === LIBRARY Section ===
        library_root = QTreeWidgetItem(self.ui.taskTreeWidget)
        library_root.setText(0, "📚 Library")
        library_root.setExpanded(True)

        # Library items
        genres_item = QTreeWidgetItem(library_root)
        genres_item.setText(0, "🎸 Genres")
        genres_item.setData(0, Qt.UserRole, "genres")

        artists_item = QTreeWidgetItem(library_root)
        artists_item.setText(0, "🎤 Artists")
        artists_item.setData(0, Qt.UserRole, "artists")

        albums_item = QTreeWidgetItem(library_root)
        albums_item.setText(0, "💿 Albums")
        albums_item.setData(0, Qt.UserRole, "albums")

        tracks_item = QTreeWidgetItem(library_root)
        tracks_item.setText(0, "🎵 Tracks")
        tracks_item.setData(0, Qt.UserRole, "tracks")

        # === ACTIONS Section ===
        actions_root = QTreeWidgetItem(self.ui.taskTreeWidget)
        actions_root.setText(0, "⚡ Actions")
        actions_root.setExpanded(True)

        # Action items
        create_item = QTreeWidgetItem(actions_root)
        create_item.setText(0, "➕ Create")
        create_item.setData(0, Qt.UserRole, "create")

        update_item = QTreeWidgetItem(actions_root)
        update_item.setText(0, "✏️ Update")
        update_item.setData(0, Qt.UserRole, "update")

        delete_item = QTreeWidgetItem(actions_root)
        delete_item.setText(0, "🗑️ Delete")
        delete_item.setData(0, Qt.UserRole, "delete")

        # Connect click signal
        self.ui.taskTreeWidget.itemClicked.connect(self._on_task_clicked)

        logger.info("Task tree populated")

    def _connect_signals(self):
        """Connect signals and slots."""

        # === Library Menu ===
        self.ui.actionFolder.triggered.connect(self._on_ingest_folder)
        self.ui.actionFiles.triggered.connect(self._on_ingest_files)
        self.ui.actionExport.triggered.connect(self._on_export_library)

        # === View Menu ===
        self.ui.actionLIbrary_Viewer.triggered.connect(self._on_open_library_viewer)
        self.ui.actionStatistics_View.triggered.connect(self._on_open_statistics)
        self.ui.actionSettings.triggered.connect(self._on_open_settings)

        # === Window Menu ===
        self.ui.actionTile.triggered.connect(self.ui.mdiArea.tileSubWindows)
        self.ui.actionCascade.triggered.connect(self.ui.mdiArea.cascadeSubWindows)
        self.ui.actionClose_All.triggered.connect(self.ui.mdiArea.closeAllSubWindows)
        self.ui.actionClose_Current.triggered.connect(self._on_close_current_window)

        # === Help Menu ===
        self.ui.actionAbout_Media_Manager.triggered.connect(self._on_about)

        logger.info("Signals connected")

    # ========================================================================
    # TASK TREE CLICKS
    # ========================================================================

    @Slot(QTreeWidgetItem, int)
    def _on_task_clicked(self, item, column):
        """Handle task tree item click."""

        task = item.data(0, Qt.UserRole)

        if not task:
            return

        logger.info(f"Task clicked: {task}")

        if task == "genres":
            self.ui.statusbar.showMessage("Opening Genres...", 2000)
            self._open_genres_window()

        elif task == "artists":
            self.ui.statusbar.showMessage("Opening Artists...", 2000)
            self._open_artists_window()

        elif task == "albums":
            self.ui.statusbar.showMessage("Opening Albums...", 2000)
            self._open_albums_window()

        elif task == "tracks":
            self.ui.statusbar.showMessage("Opening Tracks...", 2000)
            # TODO

        elif task == "create":
            self.ui.statusbar.showMessage("Create action", 2000)
            # TODO

        elif task == "update":
            self.ui.statusbar.showMessage("Update action", 2000)
            # TODO

        elif task == "delete":
            self.ui.statusbar.showMessage("Delete action", 2000)
            # TODO

    # ========================================================================
    # MDI WINDOWS
    # ========================================================================

    def _open_genres_window(self):
        """Open genres MDI window."""
        genres = self.controllers['genre'].get_all()

        list_widget = QListWidget()
        for genre in genres:
            list_widget.addItem(f"{genre['name']} (ID: {genre['id']})")

        sub = QMdiSubWindow()
        sub.setWidget(list_widget)
        sub.setWindowTitle("Genres")
        sub.setAttribute(Qt.WA_DeleteOnClose)
        sub.resize(400, 300)

        self.ui.mdiArea.addSubWindow(sub)
        sub.show()

        logger.info("Genres window opened")

    def _open_artists_window(self):
        """Open artists MDI window."""
        artists = self.controllers['artist'].get_all()

        list_widget = QListWidget()
        for artist in artists:
            list_widget.addItem(f"{artist['name']} (ID: {artist['id']})")

        sub = QMdiSubWindow()
        sub.setWidget(list_widget)
        sub.setWindowTitle("Artists")
        sub.setAttribute(Qt.WA_DeleteOnClose)
        sub.resize(400, 300)

        self.ui.mdiArea.addSubWindow(sub)
        sub.show()

        logger.info("Artists window opened")

    def _open_albums_window(self):
        """Open albums MDI window."""
        albums = self.controllers['album'].get_all()

        list_widget = QListWidget()
        for album in albums:
            list_widget.addItem(f"{album['name']} (ID: {album['id']})")

        sub = QMdiSubWindow()
        sub.setWidget(list_widget)
        sub.setWindowTitle("Albums")
        sub.setAttribute(Qt.WA_DeleteOnClose)
        sub.resize(400, 300)

        self.ui.mdiArea.addSubWindow(sub)
        sub.show()

        logger.info("Albums window opened")

    # ========================================================================
    # MENU ACTIONS - Library
    # ========================================================================

    @Slot()
    def _on_ingest_folder(self):
        """Ingest music from folder."""
        self.ui.statusbar.showMessage("Ingest Folder - TODO", 3000)
        logger.info("Ingest folder clicked")

    @Slot()
    def _on_ingest_files(self):
        """Ingest music files."""
        self.ui.statusbar.showMessage("Ingest Files - TODO", 3000)
        logger.info("Ingest files clicked")

    @Slot()
    def _on_export_library(self):
        """Export/backup library."""
        self.ui.statusbar.showMessage("Export Library - TODO", 3000)
        logger.info("Export library clicked")

    # ========================================================================
    # MENU ACTIONS - View
    # ========================================================================

    @Slot()
    def _on_open_library_viewer(self):
        """Open library viewer window."""
        from PySide6.QtWidgets import QTextEdit

        self.ui.statusbar.showMessage("Opening Library Viewer...", 2000)

        viewer = QTextEdit()
        viewer.setPlainText("Library Viewer\n\nGenres:\n- Rock\n- Jazz\n- Blues")
        viewer.setReadOnly(True)

        sub = QMdiSubWindow()
        sub.setWidget(viewer)
        sub.setWindowTitle("Library Viewer")
        sub.setAttribute(Qt.WA_DeleteOnClose)

        self.ui.mdiArea.addSubWindow(sub)
        sub.show()

        logger.info("Library viewer opened")

    @Slot()
    def _on_open_statistics(self):
        """Open statistics window."""
        from PySide6.QtWidgets import QTextEdit

        self.ui.statusbar.showMessage("Opening Statistics...", 2000)

        stats = QTextEdit()
        stats.setPlainText("Statistics\n\nTotal Albums: 5\nTotal Artists: 7\nTotal Genres: 8")
        stats.setReadOnly(True)

        sub = QMdiSubWindow()
        sub.setWidget(stats)
        sub.setWindowTitle("Statistics")
        sub.setAttribute(Qt.WA_DeleteOnClose)

        self.ui.mdiArea.addSubWindow(sub)
        sub.show()

        logger.info("Statistics opened")

    @Slot()
    def _on_open_settings(self):
        """Open settings window."""
        self.ui.statusbar.showMessage("Settings - TODO", 3000)
        logger.info("Settings clicked")

    # ========================================================================
    # MENU ACTIONS - Window
    # ========================================================================

    @Slot()
    def _on_close_current_window(self):
        """Close current active MDI window."""
        current = self.ui.mdiArea.activeSubWindow()
        if current:
            current.close()
            logger.info("Closed current window")

    # ========================================================================
    # MENU ACTIONS - Help
    # ========================================================================

    @Slot()
    def _on_about(self):
        """Show about dialog."""
        from PySide6.QtWidgets import QMessageBox

        QMessageBox.about(
            self,
            "About MediaManager",
            "<h2>MediaManager</h2>"
            "<p>Version 0.1.0</p>"
            "<p>Modern music library manager with SAP-style interface.</p>"
            "<p>Built with Python, Qt6, and Java.</p>"
        )

        logger.info("About dialog shown")

    # ========================================================================
    # CLEANUP
    # ========================================================================

    def closeEvent(self, event):
        """Handle window close event."""
        logger.info("MainWindow closing")

        # Disconnect backend
        if self.backend:
            self.backend.disconnect()

        event.accept()