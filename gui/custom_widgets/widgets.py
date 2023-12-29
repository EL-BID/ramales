from typing import Optional, Union

from PyQt5.QtCore import QLocale, Qt
from PyQt5.QtWidgets import (QDoubleSpinBox, QSpinBox, QLabel, QWidget, QStackedWidget, QPushButton, QGridLayout,
                             QLayout, QLayoutItem, QSizePolicy)


class HalfPrecisionDoubleSpinBox(QDoubleSpinBox):
    """
        This widget is a QDoubleSpinBox that approximates to values closer to a decimal multiple of 5

         For example,
         - With an accuracy of 2, 0.03 will become 0.05
         - With an accuracy of 3, 0.013 will become 0.015
    """

    def __init__(self):
        super().__init__()
        self.setDecimals(2)
        self.setSingleStep(0.05)
        super().valueChanged.connect(self.valueChanged)

    def valueChanged(self, value):
        self.setValue(
            round(value * 2, self.decimals() - 1) / 2
        )


class ThousandsSeparatorSpinBox(QSpinBox):
    """
        This widget is a QDoubleSpinBox that formats the entire incoming text to the thousands
        division appropriate for the selected location
    """

    def __init__(self, loc=QLocale()):
        super().__init__()
        self.loc = loc

    def textFromValue(self, v: int) -> str:
        self.loc.setNumberOptions(QLocale.DefaultNumberOptions)

        return self.loc.toString(v)


class ThousandsSeparatorLabel(QLabel):
    def __init__(self, loc=QLocale()):
        super().__init__()
        self.loc = loc

    def setText(self, s: str) -> None:
        # To avoid errors, we first check if the added string is an integer
        if s.isdigit() or s.startswith('-') and s[1:].isdigit():
            self.loc.setNumberOptions(QLocale.DefaultNumberOptions)
            v = int(s)
            super().setText(
                self.loc.toString(v)
            )
        else:
            super().setText(s)


class NextPreviousStackedWidget(QWidget):
    def __init__(self, should_hide_last=True):
        super().__init__()
        self.gl = QGridLayout()
        self.sw_images = QStackedWidget()
        self.pb_previous_image = QPushButton()
        self.pb_next_image = QPushButton()
        self.should_hide_last = should_hide_last  # Used in case the last button is not needed

        self.pb_previous_image.setText('<<')
        self.pb_previous_image.setFixedSize(100, 25)
        self.pb_next_image.setText('>>')
        self.pb_next_image.setFixedSize(100, 25)
        self.pb_previous_image.clicked.connect(self.go_for_previous_image)
        self.pb_next_image.clicked.connect(self.go_for_next_image)
        self.gl.addWidget(self.sw_images, 0, 0, 1, 2, Qt.AlignCenter)
        self.gl.addWidget(self.pb_previous_image, 1, 0, Qt.AlignRight)
        self.gl.addWidget(self.pb_next_image, 1, 1, Qt.AlignLeft)

        sp_retain = self.pb_previous_image.sizePolicy()
        sp_retain.setRetainSizeWhenHidden(True)
        self.pb_previous_image.setSizePolicy(sp_retain)
        self.pb_next_image.setSizePolicy(sp_retain)

        self.pb_previous_image.hide()
        self.pb_next_image.hide()
        self.setLayout(self.gl)

    def add_widget(self, w: QWidget):
        self.sw_images.addWidget(w)
        self.__show_hide_buttons()

    def clear(self):
        for i in reversed(range(self.sw_images.count())):
            widget = self.sw_images.widget(i)
            self.sw_images.removeWidget(widget)
            widget.deleteLater()

    def go_for_next_image(self):
        self.skip_n_images(+1)
        pass

    def go_for_previous_image(self):
        self.skip_n_images(-1)
        pass

    def skip_n_images(self, n):
        if self.sw_images.count() == 0:
            return
        next_index = self.sw_images.currentIndex() + n
        next_index = max(0, next_index)
        next_index = min(self.sw_images.count() - 1, next_index)
        self.sw_images.setCurrentIndex(
            next_index
        )
        self.__show_hide_buttons()

    def __show_hide_buttons(self):
        if self.sw_images.currentIndex() == self.sw_images.count() - 1 and self.should_hide_last:
            self.pb_next_image.hide()
        else:
            self.pb_next_image.show()

        if self.sw_images.currentIndex() == 0:
            self.pb_previous_image.hide()
        else:
            self.pb_previous_image.show()


class FormLayoutWithIcon(QGridLayout):
    """
         Class used to generate forms with an additional optional icon as needed

         Only adding items at the end is supported.
    """

    def __init__(self):
        super().__init__()
        self.current_index = 0
        self.setColumnMinimumWidth(0, 300)
        self.setColumnMinimumWidth(1, 100)
        self.first_focus = False
        self.first_field = None

    def add_row(self, label: Union[QWidget, str],
                field: Optional[Union[QWidget, QLayout]] = None, icon: Optional[QWidget] = None):
        if isinstance(label, str):
            label = QLabel(label)

        if field is None:
            self.addWidget(label, self.current_index, 0, 1, 2)
            self.current_index += 1
            return

        if isinstance(field, QLayout):
            w = QWidget()
            w.setLayout(field)
            field = w

        self.addWidget(label, self.current_index, 0)
        self.addWidget(field, self.current_index, 1)

        if icon is not None:
            self.addWidget(icon, self.current_index, 2)

        if not self.first_focus and field is not None:
            self.first_focus = True
            self.first_field = field

        self.current_index += 1

    def add_stretch(self):
        widget = QWidget()
        size_policy = widget.sizePolicy()
        size_policy.setVerticalPolicy(QSizePolicy.Expanding)
        widget.setSizePolicy(size_policy)
        self.addWidget(widget, self.current_index, 0, 1, 3)

    def takeAt(self, a0: int) -> QLayoutItem:
        self.current_index -= 1
        if self.current_index < 0:
            self.current_index = 0

        return super().takeAt(a0)

    def focus_first(self):
        if self.first_field is not None:
            self.first_field.selectAll()
            self.first_field.setFocus()
