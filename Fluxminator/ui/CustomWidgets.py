
from PyQt5 import QtGui
from PyQt5.QtWidgets import QDoubleSpinBox, QWidget, QPushButton, QLabel, QVBoxLayout, QFrame, QHBoxLayout
from PyQt5.Qt import QPalette
from PyQt5.QtCore import Qt, pyqtSignal


class SpecialParameterSetCreator(QWidget):
    """ Widget for creating customized parameter combinations (extended portion of the View) """

    signal = pyqtSignal()

    def __init__(self, parameter_list):

        super(SpecialParameterSetCreator, self).__init__()

        self.setWindowTitle("Add customized parameter combinations")
        self.setWindowIcon((QtGui.QIcon("icon.ico")))

        # Containers for later usage:

        self.labels = []
        self.spinBoxes = []

        # Layout for Add & Done buttons:

        self.addButton = QPushButton("Add")
        self.doneButton = QPushButton("Done")

        self.buttonHBox = QHBoxLayout()
        self.buttonHBox.addWidget(self.addButton)
        self.buttonHBox.addWidget(self.doneButton)

        self.vBox = self._set_layout(parameter_list)
        self.setLayout(self.vBox)

        self._GUI_interactor()

    def get_parameter_labels(self): return self.labels
    def get_parameter_value_containers(self): return self.spinBoxes

    def reset_background(self):
        """ Set the default yellow background for the unedited spin boxes """
        color = self.spinBoxes[0].palette()
        color.setColor(QPalette.Base, Qt.yellow)

        for spinbox in self.spinBoxes:
            spinbox.setPalette(color)

    def _set_layout(self, parameter_list):                      # parameter_list[type: Parameter] (from Model.py)
        """ Set up the layout with the spin boxes for the widget """

        layoutVBox = QVBoxLayout()

        if len(parameter_list) == 0:
            no_params_frame = QFrame()
            no_params_frame.setFrameStyle(QFrame.StyledPanel)
            no_params_box = QVBoxLayout(no_params_frame)
            no_params_box.addWidget(QLabel("No parameters yet"))

            layoutVBox.addWidget(no_params_frame)

        else:
            # LAYOUT: Spin boxes arranged in columns, with a maximum of 5 spin boxes in each column

            column_box = QHBoxLayout()                          # container for all the columns

            column_number = len(parameter_list) / 5             # max 5 spin boxes (parameters) / column
            column_number = int(column_number) if column_number == int(column_number) else int(column_number) + 1

            i = 0
            for column in range(column_number):

                vbox = QVBoxLayout()                            # container for one column
                vbox.setAlignment(Qt.AlignTop)

                for row in range(5):

                    if i == len(parameter_list):                # break if there are no parameters left
                        break

                    parameter_label = QLabel(parameter_list[i].get_name())

                    spinbox = QDoubleSpinBox()
                    spinbox.setFixedWidth(75)
                    spinbox.setMaximum(10000)
                    spinbox.setSingleStep(0.01)
                    spinbox.setValue(parameter_list[i].range.get_min())     # set the minimum value for the parameters

                    self.labels.append(parameter_label)         # store the parameter names
                    self.spinBoxes.append(spinbox)              # store the spin boxes with the default value

                    frame = QFrame()
                    frame.setFrameStyle(QFrame.StyledPanel)

                    hbox = QHBoxLayout(frame)
                    hbox.addWidget(parameter_label)
                    hbox.addWidget(spinbox)

                    vbox.addWidget(frame)
                    i += 1

                column_box.addLayout(vbox)                      # add the column to the container of columns

            layoutVBox.addLayout(column_box)                    # add the container of columns to the final layout

            self.reset_background()                             # set the yellow background color

        layoutVBox.addLayout(self.buttonHBox)                   # add the buttons to the final layout

        return layoutVBox

    def _GUI_interactor(self):
        """ GUI bindings for functions that do not involve model changes """
        for spinbox in self.spinBoxes:
            spinbox.valueChanged.connect(self._white_background)

        self.doneButton.clicked.connect(self.close)

    def _white_background(self):
        """ Set the background color to white (after editing the original value in the spin boxes) """
        spinbox = self.sender()                                 # edited spinbox

        new_color = spinbox.palette()                           # white background after editing
        new_color.setColor(QPalette.Base, Qt.white)
        spinbox.setPalette(new_color)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        """ Emit a signal caught by the presenter, used to enable the parameter set creator GUI """
        self.signal.emit()
