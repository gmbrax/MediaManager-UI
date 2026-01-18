"""
MainWindow for MediaManager.

SAP-style interface with task tree and MDI area.
"""

import logging
from typing import Dict
from unittest import case

from PySide6.QtWidgets import (
    QMainWindow, QTreeWidgetItem, QMdiSubWindow, QListWidget
)
from PySide6.QtCore import Qt, Slot, Signal

from backend.interface import IMediaManagerBackend
from ui.ui_mainwindow import Ui_MediaManagerMain

from views.dialogs.create_dialog import CreateDialog


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
    data_changed = Signal(str)  # Signal com tipo de entidade que mudou
    def __init__(self, backend: IMediaManagerBackend, controllers: Dict):
        """
        Initialize main window.

        Args:
            backend: Backend instance
            controllers: Dictionary of controllers
        """



        super().__init__()

        self._open_windows = {}

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
        view_item = QTreeWidgetItem(library_root)
        view_item.setText(0,"View Library")
        view_item.setData(0,Qt.UserRole,{"action":"view"})

        # === ACTIONS Section ===
        actions_root = QTreeWidgetItem(self.ui.taskTreeWidget)
        actions_root.setText(0, "⚡ Actions")
        actions_root.setExpanded(True)

        genres_item = QTreeWidgetItem(actions_root)
        genres_item.setText(0,"Genres")
        genres_item.setExpanded(True)

        genres_create_item = QTreeWidgetItem(genres_item)
        genres_create_item.setText(0, "Create")
        genres_create_item.setData(0, Qt.UserRole, {"entity":"genre","action":"create"})

        genres_update_item = QTreeWidgetItem(genres_item)
        genres_update_item.setText(0, "Update")
        genres_update_item.setData(0, Qt.UserRole, {"entity":"genre","action":"update"})

        genres_delete_item = QTreeWidgetItem(genres_item)
        genres_delete_item.setText(0, "Delete")
        genres_delete_item.setData(0,Qt.UserRole, {"entity":"genre","action":"delete"})

        artists_item = QTreeWidgetItem(actions_root)
        artists_item.setText(0,"Artists")
        artists_item.setExpanded(True)

        artists_create_item = QTreeWidgetItem(artists_item)
        artists_create_item.setText(0, "Create")
        artists_create_item.setData(0, Qt.UserRole, {"entity":"artist","action":"create"})

        artists_update_item = QTreeWidgetItem(artists_item)
        artists_update_item.setText(0, "Update")
        artists_update_item.setData(0, Qt.UserRole, {"entity":"artist","action":"update"})

        artists_delete_item = QTreeWidgetItem(artists_item)
        artists_delete_item.setText(0, "Delete")
        artists_delete_item.setData(0, Qt.UserRole, {"entity":"artist","action":"delete"})

        albums_item = QTreeWidgetItem(actions_root)
        albums_item.setText(0,"Albums")
        albums_item.setExpanded(True)

        albums_create_item = QTreeWidgetItem(albums_item)
        albums_create_item.setText(0, "Create")
        albums_create_item.setData(0, Qt.UserRole, {"entity":"album","action":"create"})

        albums_update_item = QTreeWidgetItem(albums_item)
        albums_update_item.setText(0, "Update")
        albums_update_item.setData(0, Qt.UserRole, {"entity":"album","action":"update"})

        albums_delete_item = QTreeWidgetItem(albums_item)
        albums_delete_item.setText(0, "Delete")
        albums_delete_item.setData(0, Qt.UserRole, {"entity":"album","action":"delete"})


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

        data = item.data(0,Qt.UserRole)
        if not data:
            return
        action = data.get("action")
        entity = data.get("entity")
        logger.info(f"Task tree item clicked: {action} {entity}")
        if action == "view":
            self._on_open_library_viewer()

        match action:
            case "create":
                self._on_create_clicked(entity)
            case "update":
                self._on_update_clicked(entity)
            case "delete":
                self._on_delete_clicked(entity)

    def _on_create_clicked(self, entity):
        """Handle create button click."""

        # Define window key (unique per entity type)
        window_key = f"create_{entity}"

        # Check if window already exists
        if window_key in self._open_windows:
            existing = self._open_windows[window_key]
            if existing in self.ui.mdiArea.subWindowList():
                # Focus existing window
                self.ui.mdiArea.setActiveSubWindow(existing)
                existing.raise_()
                existing.setFocus()
                self.ui.statusbar.showMessage(f"Create {entity.title()} window already open", 2000)
                logger.info(f"Focused existing create window: {entity}")
                return
            else:
                # Window was closed - remove from tracking
                del self._open_windows[window_key]

        # Create new dialog
        dialog = CreateDialog(entity, self.ui.mdiArea, self)

        # Connect signal
        dialog.create.connect(lambda data: self._do_create(entity, data))

        # Show and track
        dialog.show()
        self._open_windows[window_key] = dialog.sub

        # Cleanup on close
        def on_closed():
            if window_key in self._open_windows:
                del self._open_windows[window_key]

        dialog.sub.destroyed.connect(on_closed)

        logger.info(f"Create dialog opened for: {entity}")

    def _on_update_clicked(self, entity):
        """Handle update button click."""
        match entity:
            case "genre":
                pass
            case "artist":
                pass
            case "album":
                pass
        logger.info(f"Update button clicked: {entity}")

    def _on_delete_clicked(self, entity):
        """Handle delete button click."""
        match entity:
            case "genre":
                pass
            case "artist":
                pass
            case "album":
                pass
        logger.info(f"Delete button clicked: {entity}")

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
    # MDI WINDOW MANAGEMENT
    # ========================================================================

    def _get_or_create_window(self, window_key: str, window_title: str, widget) -> QMdiSubWindow:
        """
        Get existing window or create new one.

        Prevents duplicate windows in MDI area.

        Args:
            window_key: Unique key for window (e.g., "create_genre", "list_artists")
            window_title: Title for window
            widget: Widget to display in window

        Returns:
            QMdiSubWindow instance
        """
        # Check if window already exists and is still open
        if window_key in self._open_windows:
            existing_window = self._open_windows[window_key]

            # Verify window is still in MDI area (not closed)
            if existing_window in self.ui.mdiArea.subWindowList():
                # Window exists - activate and focus it
                self.ui.mdiArea.setActiveSubWindow(existing_window)
                existing_window.raise_()
                existing_window.setFocus()
                logger.info(f"Activated existing window: {window_key}")
                return existing_window
            else:
                # Window was closed - remove from tracking
                del self._open_windows[window_key]

        # Create new window
        sub = QMdiSubWindow()
        sub.setWidget(widget)
        sub.setWindowTitle(window_title)
        sub.setAttribute(Qt.WA_DeleteOnClose)

        # Track window
        self._open_windows[window_key] = sub

        # Connect close event to cleanup tracking
        def on_window_closed():
            if window_key in self._open_windows:
                del self._open_windows[window_key]
                logger.info(f"Window closed and untracked: {window_key}")

        sub.destroyed.connect(on_window_closed)

        # Add to MDI area
        self.ui.mdiArea.addSubWindow(sub)

        logger.info(f"Created new window: {window_key}")
        return sub


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

        window_key = "library_viewer"

        # Check for existing window
        if window_key in self._open_windows:
            existing = self._open_windows[window_key]
            if existing in self.ui.mdiArea.subWindowList():
                self.ui.mdiArea.setActiveSubWindow(existing)
                existing.raise_()
                self.ui.statusbar.showMessage("Library Viewer already open", 2000)
                return
            else:
                del self._open_windows[window_key]

        self.ui.statusbar.showMessage("Opening Library Viewer...", 2000)

        # Create viewer widget
        from views.widgets.library_viewer_widget import LibraryViewerWidget
        viewer = LibraryViewerWidget(self.controllers)

        # CONECTA SIGNAL DE ATUALIZAÇÃO! ← IMPORTANTE!
        self.data_changed.connect(viewer.refresh)

        # Create MDI window
        sub = QMdiSubWindow()
        sub.setWidget(viewer)
        sub.setWindowTitle("📚 Library Viewer")
        sub.setAttribute(Qt.WA_DeleteOnClose)
        sub.resize(600, 500)

        # Track window
        self._open_windows[window_key] = sub

        def on_closed():
            # Desconecta signal quando fechar
            self.data_changed.disconnect(viewer.refresh)
            if window_key in self._open_windows:
                del self._open_windows[window_key]

        sub.destroyed.connect(on_closed)

        self.ui.mdiArea.addSubWindow(sub)
        sub.show()

        logger.info("Library viewer opened")

    @Slot()
    def _on_open_statistics(self):
        """Open statistics window."""
        from PySide6.QtWidgets import QTextEdit

        self.ui.statusbar.showMessage("Opening Statistics...", 2000)

        window_key = "Statistics"

        # Check for existing window
        if window_key in self._open_windows:
            existing = self._open_windows[window_key]
            if existing in self.ui.mdiArea.subWindowList():
                self.ui.mdiArea.setActiveSubWindow(existing)
                existing.raise_()
                self.ui.statusbar.showMessage("Statistics already open", 2000)
                return
            else:
                del self._open_windows[window_key]


        stats = QTextEdit()
        stats.setPlainText("Statistics\n\nTotal Albums: 5\nTotal Artists: 7\nTotal Genres: 8")
        stats.setReadOnly(True)

        sub = QMdiSubWindow()
        sub.setWidget(stats)
        sub.setWindowTitle("Statistics")
        sub.setAttribute(Qt.WA_DeleteOnClose)

        self.ui.mdiArea.addSubWindow(sub)
        sub.show()

        # Track window
        self._open_windows[window_key] = sub

        def on_closed():
            if window_key in self._open_windows:
                del self._open_windows[window_key]

        sub.destroyed.connect(on_closed)

        logger.info("Statistics opened")
        logger.info(self.ui.mdiArea.subWindowList())

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
            "<h1>MediaManager</h1>"
            "<p>Version 0.0.1</p>"
            "<p>Modern music library manager with SAP-style interface.</p>"
            "<p>Built with Python, Qt6, and Java.</p>"
        )

        logger.info("About dialog shown")

    # ========================================================================
    # CRUD OPERATIONS
    # ========================================================================

    def _do_create(self, entity: str, data: dict):
        """Actually create the entity via controller."""
        controller = self.controllers.get(entity)

        if not controller:
            logger.error(f"No controller found for {entity}")
            return

        try:
            result = controller.create(**data)
            logger.info(f"Created {entity}: {result}")
            self.ui.statusbar.showMessage(
                f"{entity.title()} '{data['name']}' created successfully!",
                3000
            )

            # EMITE SIGNAL! ← ADICIONA ISSO
            self.data_changed.emit(entity)

        except Exception as e:
            logger.error(f"Failed to create {entity}: {e}", exc_info=True)
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to create {entity}: {str(e)}"
            )

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