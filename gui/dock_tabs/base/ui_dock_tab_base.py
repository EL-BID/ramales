from PyQt5.QtWidgets import QWidget

from ....helpers.utils import Utils


class DockTab(QWidget):
    """
        The base class of all dock tabs.
    """
    def __init__(self, dock):
        super().__init__()
        self.dock = dock
        self.utils = Utils()
        self.should_reload = False  # Used by the dock to reload the tabs only when necessary, saves resources

    def dock_reload(self):
        self.reload()
        self.dock.reload()

    def tab_start_ui(self):
        """Method called inside dock to start the tab. All tabs must implement this
           and load your layout."""
        raise NotImplementedError

    def load_data(self):
        """
        Method called when generating the GUI, we load the information from the database and insert it into the tab.
        """
        pass

    def set_logic(self):
        """Method called to define user input logic."""
        pass

    def reload(self):
        """
            Method called by the dock to reload tab information, based on data
            current project.
        """
        pass
