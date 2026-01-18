"""
Create Entity Dialog.

Reusable dialog for creating entities (Genre, Artist, Album, etc).
"""

import logging
from typing import Callable, Dict, Optional

from PySide6.QtWidgets import QWidget, QMdiSubWindow, QMessageBox
from PySide6.QtCore import Qt, Signal, QObject

from ui.ui_create_dialog import Ui_CreateDialog

logger = logging.getLogger(__name__)


class CreateDialog(QObject):
    """
    Dialog for creating entities.

    Opens as MDI SubWindow with form from .ui file.
    """

    # Signals
    create = Signal(dict)  # Emitted when entity is created
    cancelled = Signal()  # Emitted when dialog is cancelled

    def __init__(self, entity_type: str, mdi_area, parent=None):
        """
        Initialize create dialog.

        Args:
            entity_type: Type of entity (genre, artist, album, etc)
            mdi_area: QMdiArea to add window to
            parent: Parent widget
        """
        super().__init__(parent)

        self.entity_type = entity_type
        self.mdi_area = mdi_area

        # Create widget and UI
        self.widget = QWidget()
        self.ui = Ui_CreateDialog()
        self.ui.setupUi(self.widget)

        # Setup UI elements
        self._setup_ui()

        # Create MDI SubWindow
        self.sub = QMdiSubWindow()
        self.sub.setWidget(self.widget)
        self.sub.setWindowTitle(f"Create {entity_type.title()}")
        self.sub.setAttribute(Qt.WA_DeleteOnClose)
        self.sub.resize(500, 150)

        # Connect signals
        self._connect_signals()

        logger.debug(f"CreateDialog initialized for {entity_type}")

    def _setup_ui(self):
        """Setup UI elements."""
        # Set label text based on entity type
        self.ui.label.setText(f"Enter {self.entity_type} name:")

        # Set placeholder
        self.ui.lineEdit.setPlaceholderText(f"{self.entity_type.title()} name...")

    def _connect_signals(self):
        """Connect signals and slots."""
        self.ui.okButton.clicked.connect(self._on_accept)
        self.ui.cancelButton.clicked.connect(self._on_reject)

    def show(self):
        """Show dialog in MDI area."""
        self.mdi_area.addSubWindow(self.sub)
        self.sub.show()
        self.ui.lineEdit.setFocus()

        logger.info(f"Create {self.entity_type} dialog opened")

    def _on_accept(self):
        """Handle accept button (OK/Create)."""
        name = self.ui.lineEdit.text().strip()

        # Validate
        if not name:
            QMessageBox.warning(
                self.widget,
                "Validation Error",
                "Name cannot be empty!"
            )
            return

        # Emit data
        data = {"name": name}
        self.create.emit(data)

        logger.info(f"Create {self.entity_type} accepted: {data}")

        # Close
        self.sub.close()

    def _on_reject(self):
        """Handle reject button (Cancel)."""
        self.cancelled.emit()
        self.sub.close()

        logger.info(f"Create {self.entity_type} cancelled")