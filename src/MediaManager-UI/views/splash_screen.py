"""
SplashScreen for MediaManager.

Displays a loading screen while the application initializes.
3ds Max 5 style with manually drawn 3D borders and sunken status bar.
"""

import logging
from pathlib import Path

from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt, QTimer, QCoreApplication
from PySide6.QtGui import QPixmap, QFont, QPainter, QColor, QPen, QLinearGradient

logger = logging.getLogger(__name__)


class SplashScreen(QWidget):
    """
    Splash screen with manually drawn 3D borders (3ds Max 5 style).
    """

    def __init__(self):
        """Initialize splash screen."""
        super().__init__()

        # Window flags: frameless, stay on top
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.SplashScreen
        )

        # Fixed size
        self.setFixedSize(600, 430)

        # Setup UI
        self._setup_ui()

        # Center on screen
        self._center_on_screen()

        logger.info("SplashScreen initialized")

    def _setup_ui(self):
        """Setup UI components - 3ds Max style com bordas MANUAIS."""

        # Background cinza (base)
        self.setStyleSheet("background-color: #D4D0C8;")

        # Image label
        self.image_label = QLabel(self)
        self.image_label.setGeometry(2, 2, 596, 396)
        self.image_label.setStyleSheet("border: none; background: black;")

        # Load and set image
        pixmap = self._create_background()
        self.image_label.setPixmap(pixmap)

        # Status bar
        self.status_bar = QWidget(self)
        self.status_bar.setGeometry(4, 400, 592, 24)
        self.status_bar.setStyleSheet("background-color: #D4D0C8; border: none;")

        # Status label
        self.status_label = QLabel("Initializing MediaManager...", self.status_bar)
        self.status_label.setGeometry(4, 5, 584, 14)
        self.status_label.setFont(QFont("Tahoma", 8))
        self.status_label.setStyleSheet("border: none; background: transparent; color: black;")

    def paintEvent(self, event):
        """Draw borders manually (3ds Max style)."""
        painter = QPainter(self)

        # ===== BORDA EXTERNA (toda janela) =====

        # Outer border (dark shadow)
        painter.setPen(QPen(QColor(64, 64, 64), 1))
        painter.drawRect(0, 0, 599, 429)

        # Inner light border (highlight - top/left)
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        painter.drawLine(1, 1, 598, 1)  # Top
        painter.drawLine(1, 1, 1, 428)  # Left

        # Inner dark border (shadow - bottom/right)
        painter.setPen(QPen(QColor(128, 128, 128), 1))
        painter.drawLine(1, 428, 598, 428)  # Bottom
        painter.drawLine(598, 1, 598, 428)  # Right

        # ===== STATUS BAR SUNKEN =====

        # Outer dark border (top/left = escuro pra parecer afundado)
        painter.setPen(QPen(QColor(128, 128, 128), 1))
        painter.drawLine(2, 398, 597, 398)  # Top dark
        painter.drawLine(2, 398, 2, 425)  # Left dark

        # Inner darker line (mais afundado)
        painter.setPen(QPen(QColor(64, 64, 64), 1))
        painter.drawLine(3, 399, 596, 399)  # Top darker
        painter.drawLine(3, 399, 3, 424)  # Left darker

        # Bottom/right light (highlight pra efeito 3D)
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        painter.drawLine(3, 424, 596, 424)  # Bottom light
        painter.drawLine(596, 399, 596, 424)  # Right light

        # Outer light (mais destaque)
        painter.setPen(QPen(QColor(223, 223, 223), 1))
        painter.drawLine(2, 425, 597, 425)  # Bottom outer
        painter.drawLine(597, 398, 597, 425)  # Right outer

        painter.end()

    def _create_background(self) -> QPixmap:
        """
        Create splash background.

        Returns:
            QPixmap with background (596x396)
        """

        # Try to load image
        img_path = Path(__file__).parent.parent / "resources" / "images" / "splash_bg.jpg"

        if img_path.exists():
            # Load image
            pixmap = QPixmap(str(img_path))

            # Scale to fit
            pixmap = pixmap.scaled(
                596, 396,
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )

            # Crop to center if needed
            if pixmap.width() > 596 or pixmap.height() > 396:
                x = (pixmap.width() - 596) // 2
                y = (pixmap.height() - 396) // 2
                pixmap = pixmap.copy(x, y, 596, 396)

            logger.info(f"Loaded splash background from {img_path}")

        else:
            # Create gradient placeholder
            pixmap = self._create_gradient_background()
            logger.warning(f"Splash image not found at {img_path}, using gradient")

        # Draw title on image
        self._draw_title(pixmap)

        return pixmap

    def _create_gradient_background(self) -> QPixmap:
        """Create gradient background as fallback."""
        pixmap = QPixmap(596, 396)
        painter = QPainter(pixmap)

        gradient = QLinearGradient(0, 0, 0, 396)
        gradient.setColorAt(0, QColor(0, 120, 180))
        gradient.setColorAt(1, QColor(0, 60, 100))

        painter.fillRect(pixmap.rect(), gradient)
        painter.end()

        return pixmap

    def _draw_title(self, pixmap: QPixmap):
        """Draw 'MediaManager' title on splash."""
        painter = QPainter(pixmap)

        # Font: large, bold, white
        font = QFont("Arial", 36, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))

        # Draw text in top-left
        painter.drawText(20, 60, "MediaManager")

        painter.end()

    def _center_on_screen(self):
        """Center splash screen on screen."""
        from PySide6.QtGui import QGuiApplication

        screen = QGuiApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def showMessage(self, message: str):
        """
        Show status message in status bar.

        Args:
            message: Message to display
        """
        self.status_label.setText(message)
        self.status_label.repaint()
        QCoreApplication.processEvents()
        logger.debug(f"Splash message: {message}")

    def finish(self, main_window):
        """
        Close splash and show main window.

        Args:
            main_window: Main window to show
        """
        self.close()
        if main_window:
            main_window.show()