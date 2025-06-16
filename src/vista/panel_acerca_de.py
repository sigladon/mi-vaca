import webbrowser

from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QFrame)


class PanelAcercaDe(QWidget):
    """Panel 'Acerca de' con diseño estilo shadcn/ui"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(24, 24, 24, 24)

        # Header
        header_section = self.create_header()
        main_layout.addWidget(header_section)

        # Separator
        separator = self.create_separator()
        main_layout.addWidget(separator)

        # Grid de información
        info_grid = self.create_info_grid()
        main_layout.addWidget(info_grid)

        # Separator
        separator2 = self.create_separator()
        main_layout.addWidget(separator2)

        # Footer con botones
        footer_section = self.create_footer()
        main_layout.addWidget(footer_section)

        main_layout.addStretch()

        # Aplicar estilos
        self.apply_styles()

    def create_header(self):
        """Crea el header minimalista"""
        header = QFrame()
        layout = QVBoxLayout(header)
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 0)

        # Título principal
        title = QLabel("Mi Vaca")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: 600;
                letter-spacing: -0.025em;
                background: transparent;
                border: none;
            }
        """)

        # Descripción
        description = QLabel("Un proyecto universitario desarrollado con PyQt6")
        description.setStyleSheet("""
            QLabel {
                color: hsl(215.4, 16.3%, 46.9%);
                font-size: 14px;
                font-weight: 400;
                background: transparent;
                border: none;
            }
        """)

        layout.addWidget(title)
        layout.addWidget(description)

        return header

    def create_separator(self):
        """Crea un separador sutil"""
        separator = QFrame()
        separator.setFixedHeight(1)
        separator.setStyleSheet("""
            QFrame {
                background-color: hsl(214.3, 31.8%, 91.4%);
                border: none;
            }
        """)
        return separator

    def create_info_grid(self):
        """Crea la grilla de información"""
        container = QFrame()
        layout = QVBoxLayout(container)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)

        # Información del desarrollador
        dev_card = self.create_info_card(
            "Desarrollador",
            "Rafael Baculima"
        )
        layout.addWidget(dev_card)

        # Información académica
        academic_card = self.create_info_card(
            "Información Académica",
            "Universidad de Cuenca\nLenguajes de Programación\nProfesora: Ing. Magalí Mejía"
        )
        layout.addWidget(academic_card)

        # Grid de 2 columnas para detalles
        details_row = QHBoxLayout()
        details_row.setSpacing(16)

        # Columna izquierda - Fecha y versión
        left_card = self.create_info_card(
            "Proyecto",
            "Versión: 1.0.0\nJunio 2025"
        )
        details_row.addWidget(left_card)

        # Columna derecha - Tecnologías
        right_card = self.create_info_card(
            "Tecnologías",
            "Python 3.11+\nPyQt6"
        )
        details_row.addWidget(right_card)

        layout.addLayout(details_row)

        return container

    def create_info_card(self, title, content):
        """Crea una tarjeta de información estilo shadcn"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: hsl(0, 0%, 100%);
                border: 1px solid hsl(214.3, 31.8%, 91.4%);
                border-radius: 8px;
                padding: 0;
            }
            QFrame:hover {
                border-color: hsl(215.4, 16.3%, 86.9%);
            }
        """)

        layout = QVBoxLayout(card)
        layout.setSpacing(8)
        layout.setContentsMargins(16, 16, 16, 16)

        # Título de la tarjeta
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                padding: 0;
                font-size: 14px;
                font-weight: 500;
                background: transparent;
                border: none;
            }
        """)

        # Contenido
        content_label = QLabel(content)
        content_label.setStyleSheet("""
            QLabel {
                padding: 0;
                color: hsl(215.4, 16.3%, 46.9%);
                font-size: 13px;
                font-weight: 400;
                line-height: 1.5;
                background: transparent;
                border: none;
            }
        """)
        content_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(content_label)

        return card

    def create_footer(self):
        """Crea el footer con botones estilo shadcn"""
        footer = QFrame()
        layout = QVBoxLayout(footer)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)

        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)

        # Botón principal "Ver en GitHub"
        primary_btn: QPushButton = QPushButton("GitHub")
        primary_btn.setStyleSheet("""
            QPushButton {
                background-color: hsl(222.2, 84%, 4.9%);
                color: hsl(210, 40%, 98%);
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 500;
                min-height: 36px;
            }
            QPushButton:hover {
                background-color: hsla(222.2, 84%, 4.9%, 0.9);
            }
            QPushButton:pressed {
                background-color: hsla(222.2, 84%, 4.9%, 0.8);
            }
        """)
        primary_btn.clicked.connect(self.open_github_url)

        # Botón secundario
        secondary_btn = QPushButton("Contactar")
        secondary_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: hsl(222.2, 84%, 4.9%);
                border: 1px solid hsl(214.3, 31.8%, 91.4%);
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 500;
                min-height: 36px;
            }
            QPushButton:hover {
                background-color: hsl(210, 40%, 98%);
                border-color: hsl(215.4, 16.3%, 86.9%);
            }
            QPushButton:pressed {
                background-color: hsl(210, 40%, 96%);
            }
        """)
        buttons_layout.addWidget(primary_btn)
        buttons_layout.addStretch()

        # Copyright
        copyright_label = QLabel("© 2025 Rafael Baculima.")
        copyright_label.setStyleSheet("""
            QLabel {
                color: hsl(215.4, 16.3%, 56.9%);
                font-size: 12px;
                font-weight: 400;
                background: transparent;
                border: none;
            }
        """)

        layout.addLayout(buttons_layout)
        layout.addWidget(copyright_label)

        return footer

    def apply_styles(self):
        """Aplica estilos generales al widget"""
        self.setStyleSheet("""
            AboutPanel {
                background-color: hsl(0, 0%, 100%);
                border: 1px solid hsl(214.3, 31.8%, 91.4%);
                border-radius: 12px;
            }
        """)

    def open_github_url(self):
        github_url = "https://github.com/sigladon/mi-vaca"
        webbrowser.open_new_tab(github_url)
