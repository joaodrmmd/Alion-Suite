import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QTreeWidget, QTreeWidgetItem, QStackedWidget, QPushButton, QTextEdit, QLineEdit, QTreeWidgetItemIterator
from PySide6.QtCore import Qt, Signal, QObject, QUrl, QTimer
from PySide6.QtGui import QFont, QPixmap, QDesktopServices
from pathlib import Path
import tools as alion_tools
import localization
import queue

class Worker(QObject):
    finished = Signal()
    output_received = Signal(str)

    def __init__(self, command_info):
        super().__init__()
        self.command_info = command_info

    def run(self):
        """Executa o comando e emite a saída."""
        for line in alion_tools.executar_comando(self.command_info):
            self.output_received.emit(line)
        self.finished.emit()

class ToolPage(QWidget):
    def __init__(self, tool_text, command_info, language):
        super().__init__()
        self.tool_text = tool_text
        self.command_info = command_info
        self.LANGUAGE = language
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel(tool_text)
        title.setObjectName("page_title")
        title.setAlignment(Qt.AlignCenter)
        
        self.run_button_text = localization.get_string("execute", lang=self.LANGUAGE, tool_name=self.tool_text)
        self.run_button = QPushButton(self.run_button_text)
        self.run_button.setObjectName("run_button")
        self.run_button.setMinimumHeight(40)
        self.run_button.clicked.connect(self.start_task)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setObjectName("console")
        
        layout.addWidget(title)
        layout.addWidget(self.run_button)
        layout.addWidget(self.console, 1)

        self.thread = None
        self.worker = None
    
    def start_task(self):
        self.console.clear()
        start_msg = localization.get_string("starting", lang=self.LANGUAGE, tool_name=self.tool_text)
        self.console.append(start_msg)
        
        executing_msg = localization.get_string("executing", lang=self.LANGUAGE)
        self.run_button.setText(executing_msg)
        self.run_button.setEnabled(False)
        
        self.thread = QObject()
        self.worker = Worker(self.command_info)
        self.worker.moveToThread(self.thread)
        self.worker.output_received.connect(self.update_console)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.task_finished)
        self.thread.start()
        
    def update_console(self, line):
        self.console.insertPlainText(line)
        self.console.verticalScrollBar().setValue(self.console.verticalScrollBar().maximum())
        
    def task_finished(self):
        complete_msg = localization.get_string("task_complete", lang=self.LANGUAGE)
        self.console.append(complete_msg)
        self.run_button.setText(self.run_button_text)
        self.run_button.setEnabled(True)
        self.thread.quit()
        self.thread.wait()

class MainWindow(QMainWindow):
    def __init__(self, version="APEX", launcher=None, language="en"):
        super().__init__()
        
        self.version = version
        self.launcher_instance = launcher
        self.LANGUAGE = language

        version_configs = alion_tools.get_version_config()
        self.current_config = version_configs.get(self.version, version_configs["APEX"])
        self.theme_color = self.current_config['theme_color']

        self.setWindowTitle(localization.get_string("app_title", lang=self.LANGUAGE, version=self.version))
        self.setGeometry(100, 100, 1280, 720)

        self.app_font = QFont("Courier New", 11, QFont.Bold)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(280)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(10, 10, 10, 10)
        self.sidebar_layout.setAlignment(Qt.AlignTop)
        
        content_container = QFrame()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0,0,0,0)
        content_layout.setSpacing(0)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setObjectName("content_area")
        
        self.footer = self._create_footer()

        content_layout.addWidget(self.stacked_widget, 1)
        content_layout.addWidget(self.footer)

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(content_container, 1)

        self.page_map = {}
        self._load_stylesheet("style.qss") 
        self._populate_sidebar()
        
        self.queue = queue.Queue()
        self.queue_timer = QTimer(self)
        self.queue_timer.timeout.connect(self.process_queue)
        self.queue_timer.start(100)

    def _populate_sidebar(self):
    # O código para criar o logo, botão voltar e busca continua o mesmo
        try:
            script_dir = Path(__file__).parent
            logo_path = script_dir / "media" / self.current_config['logo']
            logo_pixmap = QPixmap(str(logo_path))
            logo_label = QLabel()
            logo_label.setObjectName("sidebar_logo")
            logo_label.setPixmap(logo_pixmap.scaledToWidth(180, Qt.SmoothTransformation))
            logo_label.setAlignment(Qt.AlignCenter)
            self.sidebar_layout.addWidget(logo_label)
        except Exception as e:
            print(f"Erro ao carregar o logo da sidebar: {e}")

        back_button = QPushButton(localization.get_string("back_to_launcher", lang=self.LANGUAGE))
        back_button.setObjectName("back_button")
        back_button.clicked.connect(self._go_back_to_launcher)
        self.sidebar_layout.addWidget(back_button)

        self.search_bar = QLineEdit()
        self.search_bar.setObjectName("search_bar")
        self.search_bar.setPlaceholderText(localization.get_string("search_tools", lang=self.LANGUAGE))
        self.search_bar.textChanged.connect(self._on_search_text_changed)
        self.sidebar_layout.addWidget(self.search_bar)
        
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        tools_data = alion_tools.get_tools(self.version)
        
        welcome_text = localization.get_string("welcome_message", lang=self.LANGUAGE, version=self.version)
        welcome_page = QLabel(welcome_text)
        welcome_page.setObjectName("page_title")
        welcome_page.setAlignment(Qt.AlignCenter)
        self.stacked_widget.addWidget(welcome_page)

        for category_key, tool_list in tools_data.items():
            category_text = localization.get_string(category_key, lang=self.LANGUAGE)
            category_item = QTreeWidgetItem([category_text.upper()])
            category_item.setFlags(category_item.flags() & ~Qt.ItemIsSelectable)
            for tool in tool_list:
                tool_text = localization.get_string(tool['text_key'], lang=self.LANGUAGE)
                tool_item = QTreeWidgetItem([tool_text])
                category_item.addChild(tool_item)
                page = ToolPage(tool_text, tool['command'], self.LANGUAGE)
                page_index = self.stacked_widget.addWidget(page)
                self.page_map[tool_item] = page_index
            self.tree.addTopLevelItem(category_item)
        self.tree.itemClicked.connect(self._on_tree_item_clicked)
        self.sidebar_layout.addWidget(self.tree)
        
        # Adiciona um espaço flexível que empurra tudo que vem depois para o fundo
        self.sidebar_layout.addStretch()

        # Botão de avaliação do GitHub
        github_button = QPushButton(localization.get_string("evaluate_github", lang=self.LANGUAGE))
        github_button.setObjectName("github_button")
        github_button.clicked.connect(self._open_github)
        self.sidebar_layout.addWidget(github_button)

        # --- NOVO: Label de crédito adicionado aqui ---
        dev_credit_label = QLabel("Developed by r3du0x")
        dev_credit_label.setObjectName("dev_credit_label")
        dev_credit_label.setAlignment(Qt.AlignCenter)
        self.sidebar_layout.addWidget(dev_credit_label)

        # --- LINHA REMOVIDA: A árvore já foi adicionada anteriormente e estava duplicada ---
        # self.sidebar_layout.addWidget(self.tree)

    def _create_footer(self):
        """Rodapé sem o elemento central."""
        footer_frame = QFrame()
        footer_frame.setObjectName("footer")
        footer_layout = QHBoxLayout(footer_frame)
        footer_layout.setContentsMargins(15, 5, 15, 5)
        
        os_ver_text = f'{localization.get_string("os_ver", lang=self.LANGUAGE)}: {alion_tools.detectar_distro()}'
        pkg_mgr_text = f'{localization.get_string("pkg_manager", lang=self.LANGUAGE)}: {alion_tools.detectar_gerenciador_pacotes()}'

        label_os = QLabel(os_ver_text)
        label_os.setObjectName("footer_label")
        
        label_pkg = QLabel(pkg_mgr_text)
        label_pkg.setObjectName("footer_label")
        label_pkg.setAlignment(Qt.AlignRight)
        
        # Layout simplificado com apenas os elementos da esquerda e direita
        footer_layout.addWidget(label_os)
        footer_layout.addStretch() # Espaçador flexível no meio
        footer_layout.addWidget(label_pkg)
        
        return footer_frame

    def _go_back_to_launcher(self):
        if self.launcher_instance:
            self.launcher_instance.show()
        self.close()

    def _open_github(self):
        url = QUrl("https://github.com/joaodrmmd/Alion-Suite")
        QDesktopServices.openUrl(url)

    def _on_tree_item_clicked(self, item, column):
        if item in self.page_map:
            self.stacked_widget.setCurrentIndex(self.page_map[item])

    def _on_search_text_changed(self, text):
        search_text = text.lower().strip()
        visible_tools = []
        it = QTreeWidgetItemIterator(self.tree)
        while it.value():
            item = it.value()
            if item.parent():
                item_text = item.text(0).lower()
                is_visible = search_text in item_text
                item.setHidden(not is_visible)
                if is_visible:
                    visible_tools.append(item)
            it += 1
        it = QTreeWidgetItemIterator(self.tree)
        while it.value():
            item = it.value()
            if not item.parent():
                visible_children = sum(1 for i in range(item.childCount()) if not item.child(i).isHidden())
                item.setHidden(visible_children == 0)
            it += 1
        if len(visible_tools) == 1:
            item_to_select = visible_tools[0]
            self.tree.setCurrentItem(item_to_select)
            self._on_tree_item_clicked(item_to_select, 0)

    def _load_stylesheet(self, file_name):
        try:
            with open(file_name, "r") as f:
                stylesheet = f.read()
            themed_stylesheet = stylesheet.replace("THEME_COLOR_PLACEHOLDER", self.theme_color)
            self.setStyleSheet(themed_stylesheet)
        except FileNotFoundError:
            print(f"Erro: Arquivo de estilo '{file_name}' não encontrado.")
            
    def process_queue(self):
        try:
            while True:
                line = self.queue.get_nowait()
                current_page = self.stacked_widget.currentWidget()
                if isinstance(current_page, ToolPage):
                    current_page.update_console(line)
        except queue.Empty:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(version="APEX", language="en")
    window.show()
    sys.exit(app.exec())