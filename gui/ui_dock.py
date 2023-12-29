from PyQt5.QtCore import QCoreApplication
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QScrollArea, QTabWidget
from qgis.core import QgsMessageLog

from .dock_tabs.base.ui_dock_tab_base import DockTab
from .dock_tabs.ui_dock_tab_about import DockTabAbout
from .dock_tabs.ui_dock_tab_home import DockTabHome
from ..helpers.utils import Utils


class DockUI:
    scroll = QScrollArea()

    utils = Utils()

    def tr(self, message):
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('SanihubRamales', message)

    def __init__(self, iface, title):
        self.tabWidget = QTabWidget()
        self.iface = iface
        self.title = title
        self.tab_home = DockTabHome(self, iface, title)
        self.tab_about = DockTabAbout(self)
        self.tabWidget.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, index):
        """Esse método é chamado para recarregar uma tab apenas quando necessário, evitando pedir dados
        sem necessidade"""
        widget: DockTab = self.tabWidget.widget(index)
        if not isinstance(widget, DockTab):
            return

        if widget.should_reload:
            QgsMessageLog.logMessage(f"Carregando aba {widget.__class__.__name__}", "on_tab_changed")
            widget.reload()

    def loadDock(self):

        self.scroll.ensureVisible(50, 50)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.add_tabs()
        self.scroll.setWidget(self.tabWidget)

        self.tab_home.tab_start_ui()
        self.tab_about.tab_start_ui()
        self.tab_home.load_data()

    def reload(self):
        self.tab_home.reload()
        self.tab_about.reload()

    def add_tabs(self):
        before = self.tabWidget.currentWidget()
        self.tabWidget.clear()
        self.tabWidget.clear()
        self.tabWidget.addTab(self.tab_home, self.tr('Início'))
        self.tabWidget.addTab(self.tab_about, self.tr('Sobre'))
        self.tabWidget.setCurrentWidget(before)
