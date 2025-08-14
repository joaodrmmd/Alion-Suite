import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QPushButton, QComboBox
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QObject, Signal, QParallelAnimationGroup
from PySide6.QtGui import QMovie, QPixmap
from pathlib import Path
import app as alion_app
import tools as alion_tools
import localization

class VersionPanel(QFrame):
    # Sinais para comunicar com a janela principal
    mouse_entered = Signal(QFrame)
    mouse_left = Signal()

    def __init__(self, version_id, logo_filename, gif_filename, description, language):
        super().__init__()
        self.setObjectName("version_panel")
        self.setMinimumHeight(400)
        
        self.gif_label = QLabel(self)
        self.gif_label.setObjectName("gif_label")
        if gif_filename:
            self.movie = QMovie(str(Path(__file__).parent / "media" / gif_filename))
            self.gif_label.setMovie(self.movie)
            self.gif_label.setScaledContents(True)
            self.movie.start()
            self.movie.setPaused(True)

        self.overlay = QFrame(self)
        self.overlay.setObjectName("overlay")

        content_layout = QVBoxLayout(self)
        content_layout.setAlignment(Qt.AlignCenter)
        content_layout.setSpacing(20)
        
        logo_label = QLabel()
        try:
            pixmap = QPixmap(str(Path(__file__).parent / "media" / logo_filename))
            logo_label.setPixmap(pixmap.scaledToWidth(150, Qt.SmoothTransformation))
        except Exception:
            logo_label.setText(version_id)
        
        self.description_label = QLabel(description)
        self.description_label.setObjectName("panel_subtitle")
        self.description_label.setVisible(False)

        self.access_button = QPushButton(localization.get_string("access_button", lang=language))
        self.access_button.setObjectName("access_button")
        self.access_button.setFixedSize(150, 40)
        
        content_layout.addStretch()
        content_layout.addWidget(logo_label)
        content_layout.addWidget(self.description_label)
        content_layout.addWidget(self.access_button)
        content_layout.addStretch()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.gif_label.setGeometry(self.rect())
        self.overlay.setGeometry(self.rect())

    def enterEvent(self, event):
        self.mouse_entered.emit(self)
        if hasattr(self, 'movie'): self.movie.setPaused(False)
        self.description_label.setVisible(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.mouse_left.emit()
        if hasattr(self, 'movie'): self.movie.setPaused(True)
        self.description_label.setVisible(False)
        super().leaveEvent(event)

class LauncherWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_language = "en"
        self.setWindowTitle(localization.get_string("launcher_title", lang=self.current_language))
        self.setGeometry(100, 100, 1280, 720)
        self.main_app_window = None

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        panels_container = QWidget()
        self.panels_layout = QHBoxLayout(panels_container)
        self.panels_layout.setSpacing(20)
        self.panels_layout.setContentsMargins(20, 20, 20, 20)

        versions = alion_tools.get_version_config()
        self.panels = []
        for version_id, config in versions.items():
            panel = VersionPanel(version_id, config['logo'], config.get('gif', ''), config.get('description', ''), self.current_language)
            panel.access_button.clicked.connect(lambda checked, v=version_id: self.launch_app(v))
            
            panel.mouse_entered.connect(self.animate_panels)
            panel.mouse_left.connect(self.reset_animations)

            self.panels_layout.addWidget(panel)
            self.panels.append(panel)
        
        self.reset_animations(animated=False)

        footer = QFrame()
        footer.setObjectName("launcher_footer")
        footer.setFixedHeight(40)
        footer_layout = QHBoxLayout(footer)
        
        self.lang_label = QLabel(localization.get_string("language", lang=self.current_language))
        self.lang_label.setObjectName("lang_label")
        self.lang_selector = QComboBox()
        self.lang_selector.setObjectName("lang_selector")
        self.lang_selector.addItems(["English", "Português"])
        self.lang_selector.currentTextChanged.connect(self._on_language_changed)
        
        footer_layout.addStretch()
        footer_layout.addWidget(self.lang_label)
        footer_layout.addWidget(self.lang_selector)
        footer_layout.setContentsMargins(20, 0, 20, 0)

        main_layout.addWidget(panels_container, 1)
        main_layout.addWidget(footer)
        self._load_stylesheet("style.qss")

    def animate_panels(self, hovered_panel):
        """Anima a largura máxima dos painéis para criar um efeito de zoom."""
        self.animation_group = QParallelAnimationGroup()
        for panel in self.panels:
            anim = QPropertyAnimation(panel, b"maximumWidth")
            anim.setDuration(400)
            anim.setEasingCurve(QEasingCurve.InOutCubic)
            if panel is hovered_panel:
                anim.setEndValue(2000) # Permite que ele se expanda muito
            else:
                anim.setEndValue(150) # Força os outros a encolherem
            self.animation_group.addAnimation(anim)
        self.animation_group.start()
    
    def reset_animations(self, animated=True):
        """Restaura a largura máxima de todos os painéis."""
        self.animation_group = QParallelAnimationGroup()
        for panel in self.panels:
            anim = QPropertyAnimation(panel, b"maximumWidth")
            anim.setDuration(400 if animated else 0)
            anim.setEasingCurve(QEasingCurve.InOutCubic)
            anim.setEndValue(400) # Restaura para um tamanho padrão
            self.animation_group.addAnimation(anim)
        self.animation_group.start()

    def _on_language_changed(self, text):
        self.current_language = "pt" if text == "Português" else "en"
        self.setWindowTitle(localization.get_string("launcher_title", lang=self.current_language))
        self.lang_label.setText(localization.get_string("language", lang=self.current_language))
        for panel in self.panels:
            panel.access_button.setText(localization.get_string("access_button", lang=self.current_language))

    def _load_stylesheet(self, file_name):
        try:
            with open(file_name, "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Erro: Arquivo de estilo '{file_name}' não encontrado.")

    def launch_app(self, version_name):
        self.main_app_window = alion_app.MainWindow(version=version_name, launcher=self, language=self.current_language)
        self.main_app_window.show()
        self.hide()

    def closeEvent(self, event):
        QApplication.quit()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
# 1. Importa a classe QIcon
    from PySide6.QtGui import QIcon 

    # 2. Define o caminho para o ícone
    script_dir = Path(__file__).parent
    icon_path = script_dir / "media" / "icon.png"

    # 3. Aplica o ícone à aplicação inteira
    app.setWindowIcon(QIcon(str(icon_path)))
    window = LauncherWindow()
    window.show()
    sys.exit(app.exec())