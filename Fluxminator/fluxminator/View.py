
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QSpinBox, QDoubleSpinBox, QWidget, QRadioButton, \
    QPushButton, QMessageBox, QListWidget, QProgressBar, QLineEdit, \
    QLabel, QCheckBox, QComboBox

from PyQt5.QtGui import QRegExpValidator


from ui.Fluxminator_UI import FluxminatorLayout, ParameterSetCreatorLayout
from PyQt5.QtCore import QRegExp, pyqtSignal


class ParameterSetCreator(QWidget, ParameterSetCreatorLayout):
    """ Widget for creating the parameter set table required for simulations """

    signal = pyqtSignal()               # needed for emitting signal when closing the widget window

    def __init__(self):

        super(ParameterSetCreator, self).__init__()

        # Widgets for adding new parameters (newP) to the parameter set

        self.newP_title = QLabel("Add new parameter")

        self.newP_typeLabel = QLabel("Type:")
        self.newP_typeCombo = QComboBox()
        self.newP_typeCombo.addItem("GP")
        self.newP_typeCombo.addItem("PPS")
        self.newP_typeCombo.addItem("PPF")

        self.newP_nameLabel = QLabel("Name in Flux:")
        self.newP_nameLineEdit = QLineEdit()
        self.newP_nameLineEdit.setValidator(QRegExpValidator(QRegExp("[A-Za-z0-9_-]{0,255}")))

        self.newP_descLabel = QLabel("Description:")
        self.newP_descLineEdit = QLineEdit()

        self.newP_minLabel = QLabel("Min:")
        self.newP_minSpinbox = QDoubleSpinBox()
        self.newP_minSpinbox.setMaximum(10000)
        self.newP_minSpinbox.setSingleStep(0.01)

        self.newP_maxLabel = QLabel("Max:")
        self.newP_maxSpinbox = QDoubleSpinBox()
        self.newP_maxSpinbox.setMaximum(10000)
        self.newP_maxSpinbox.setSingleStep(0.01)

        self.newP_stepLabel = QLabel("Step:")
        self.newP_stepSpinbox = QDoubleSpinBox()
        self.newP_stepSpinbox.setMaximum(10000)
        self.newP_stepSpinbox.setSingleStep(0.01)

        self.newP_clearButton = QPushButton("Clear")
        self.newP_addButton = QPushButton("Add")

        # Widgets for displaying the actual parameter set (pSet):

        self.pSet_title = QLabel("Parameter Set")
        self.pSet_listWidget = QListWidget()

        # Widgets for adding customized combinations (rows) to the parameter table (customPSet):

        self.customRow_title = QLabel("Add specific parameter combinations")
        self.customRow_addButton = QPushButton("New")

        # Display and edit all customized parameter combinations TODO FUTURE DEVELOPMENT
        self.customRow_editButton = QPushButton("View all")
        self.customRow_editButton.setToolTip("FUTURE DEVELOPMENT")
        self.customRow_editButton.setDisabled(True)

        # Widgets for creating Excel file and displaying runtime information (create):

        self.create_title = QLabel("Create excel file")
        self.create_rowNumberLabel = QLabel("Number of rows: 0")

        self.create_runtimeLabel = QLabel("Estimated runtime of one simulation [min]:")
        self.create_runtimeSpinbox = QSpinBox()
        self.create_runtimeSpinbox.setMaximum(1000)

        self.create_sumRuntimeLabel = QLabel("Estimated runtime: -")

        # Edit the order of the parameters in the parameter table (Sets.xlsx) TODO FUTURE DEVELOPMENT
        self.create_orderEditorCheckBox = QCheckBox("Edit parameter order")
        self.create_orderEditorCheckBox.setToolTip("FUTURE DEVELOPMENT")
        self.create_orderEditorCheckBox.setDisabled(True)

        self.create_excelCreatorButton = QPushButton("Create")

        # Set up the layout for the widget (ParameterSetCreatorLayout):

        self.setup_layout(self)

        self.setWindowTitle("Parameter Table Creator")
        self.setWindowIcon((QtGui.QIcon("icon.ico")))

    def parameter_editor_message_box(self):
        """ The message box occurs when double-clicking on a list widget item for the parameter set """

        mB = QMessageBox(self)
        mB.setIcon(QMessageBox.Question)
        mB.setText("What to do?")
        mB.setWindowTitle("Edit parameter")

        mB.addButton(QPushButton('Edit'), QMessageBox.YesRole)
        mB.addButton(QPushButton('Delete'), QMessageBox.NoRole)
        mB.addButton(QPushButton('Cancel'), QMessageBox.RejectRole)

        return mB.exec_()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        """ Emit a signal caught by the presenter, used to enable the main window GUI """
        self.signal.emit()


class FluxminatorView(QWidget, FluxminatorLayout):
    """ MVP - View class (GUI) """

    def __init__(self):

        super().__init__()

        # Widgets for main settings:

        self.newSessionButton = QRadioButton("New project")
        self.oldSessionButton = QRadioButton("Continue existing project")
        self.summarySessionButton = QRadioButton("Create summary from existing data")

        self.settingsTitle = QLabel("Settings")

        self.deleteCheckBox = QCheckBox("Delete the scenario solutions")

        # Batch mode and price calculation TODO FUTURE DEVELOPMENT
        self.batchModeCheckBox = QCheckBox("Run in batch mode")
        self.priceCalcCheckBox = QCheckBox("Calculate price")
        self.batchModeCheckBox.setToolTip("FUTURE DEVELOPMENT")
        self.priceCalcCheckBox.setToolTip("FUTURE DEVELOPMENT")
        self.batchModeCheckBox.setDisabled(True)
        self.priceCalcCheckBox.setDisabled(True)

        # Widgets for simulation settings:

        self.gammaNameLabel = QLabel("Gamma name:")
        self.gammaNameLineEdit = QLineEdit("GAMMA")

        self.currentNameLabel = QLabel("Current name:")
        self.currentNameLineEdit = QLineEdit("IMAX")

        self.currentSourceNameLabel = QLabel("Current source name:")
        self.currentSourceNameLineEdit = QLineEdit("IPH_U")

        self.modelTitle = QLabel("Model setup")

        self.fluxModelButton = QPushButton("Select Flux model")
        self.fluxModelLabel = QLabel("Missing!")

        self.pixMap = QPixmap("ikon.jpg")
        self.pixLabel = QLabel()
        self.pixLabel.setPixmap(self.pixMap)

        self.slotNumLabel = QLabel("Slot number:")
        self.slotNumSpinBox = QSpinBox()

        self.poleNumLabel = QLabel("Pole number:")
        self.poleNumSpinBox = QSpinBox()

        self.motorParamExcelButton = QPushButton("Create parameter set")

        # Batch mode and price calculation TODO FUTURE DEVELOPMENT
        self.priceCalcButton = QPushButton("Price calculation setup")
        self.priceCalcButton.setToolTip("FUTURE DEVELOPMENT")
        self.priceCalcButton.setDisabled(True)

        # Widgets for scenario settings:

        self.scenarioTitle = QLabel("Scenario setup")

        self.coggingScenarioCheckBox = QCheckBox("Cogging && BEMF scenario")
        self.rippleScenarioCheckBox = QCheckBox("Ripple scenario")

        self.loadDepCheckBox = QCheckBox("Load dependency")
        self.gammaDepCheckBox = QCheckBox("Gamma dependency")

        self.coggingMin = QDoubleSpinBox()
        self.coggingMax = QDoubleSpinBox()
        self.coggingStep = QDoubleSpinBox()

        self.rippleMin = QDoubleSpinBox()
        self.rippleMax = QDoubleSpinBox()
        self.rippleStep = QDoubleSpinBox()

        self.currentMin = QDoubleSpinBox()
        self.currentMax = QDoubleSpinBox()
        self.currentStep = QDoubleSpinBox()

        self.gammaMin = QDoubleSpinBox()
        self.gammaMax = QDoubleSpinBox()
        self.gammaStep = QDoubleSpinBox()

        # Widgets for starting the simulation, progress state

        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)

        self.progressLabel = QLabel()
        self.progressLabel.setText("Calculation: 0/0, estimated finish time: -")

        self.runButton = QPushButton("Run")
        self.clearButton = QPushButton("Clear")

        # Set up layout for the View (FluxminatorLayout):

        self.setup_layout(self)

        # Special widgets for parameter set table creation:

        self.parameterSetCreatorWidget = ParameterSetCreator()
        self.specialParameterSetCreatorWidget = None

        # Bindings for functions that do not involve model changes
        self._GUI_interactor()

        self.show()

    def stop_simulation_message_box(self):
        """ The message box occurs when the stop button is pushed """

        mB = QMessageBox(self)
        mB.setIcon(QMessageBox.Question)
        mB.setText("If you press 'STOP', you'll have to wait for the current calculation to finish"
                   " before resuming the session!")
        mB.setWindowTitle("Message")

        mB.addButton(QPushButton('Stop'), QMessageBox.YesRole)
        mB.addButton(QPushButton('Cancel'), QMessageBox.NoRole)

        return mB.exec_()

    def _GUI_interactor(self):
        """ GUI bindings for functions that do not involve model changes """

        self.gammaNameLineEdit.textChanged.connect(self._letters_up)
        self.currentNameLineEdit.textChanged.connect(self._letters_up)
        self.currentSourceNameLineEdit.textChanged.connect(self._letters_up)

        self.parameterSetCreatorWidget.newP_nameLineEdit.textChanged.connect(self._letters_up)
        
    def _letters_up(self):
        """ Set capital letters """
        sender_object = self.sender()
        sender_object.setText(sender_object.text().upper().strip())

