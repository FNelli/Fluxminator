
import itertools

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import QSplitter, QSizePolicy, QFrame, QHBoxLayout, QGridLayout, QLabel, QVBoxLayout


class ParameterSetCreatorLayout:
    """ UI class for setting up the ParameterSetCreator widget GUI """

    @staticmethod
    def setup_layout(widget):           # ParameterSetCreator widget

        ParameterSetCreatorLayout._setup_new_parameter_layout(widget)
        ParameterSetCreatorLayout._setup_parameter_set_layout(widget)
        ParameterSetCreatorLayout._setup_custom_row_layout(widget)
        ParameterSetCreatorLayout._setup_excel_creator_layout(widget)

        widget.topSplitter = QSplitter(Qt.Horizontal)
        widget.topSplitter.addWidget(widget.newP_frame)
        widget.topSplitter.addWidget(widget.pSet_frame)

        widget.bottomSplitter = QSplitter(Qt.Horizontal)
        widget.bottomSplitter.addWidget(widget.customRow_frame)
        widget.bottomSplitter.addWidget(widget.create_frame)

        widget.splitter = QSplitter(Qt.Vertical)
        widget.splitter.addWidget(widget.topSplitter)
        widget.splitter.addWidget(widget.bottomSplitter)

        widget.vBox = QVBoxLayout()
        widget.vBox.addWidget(widget.splitter)

        widget.setLayout(widget.vBox)

    @staticmethod
    def _setup_new_parameter_layout(widget):

        # Layout for parameter TYPE, NAME, DESCRIPTION settings:

        widget.newP_title.setFont(QFont("Ubuntu Mono", 9, QFont.Black))

        widget.newP_typeCombo.setFixedWidth(100)
        widget.newP_nameLineEdit.setFixedWidth(170)
        widget.newP_descLineEdit.setFixedWidth(170)

        widget.newP_typeHBox = QHBoxLayout()
        widget.newP_typeHBox.addWidget(widget.newP_typeLabel)
        widget.newP_typeHBox.addWidget(widget.newP_typeCombo)

        widget.newP_nameHBox = QHBoxLayout()
        widget.newP_nameHBox.addWidget(widget.newP_nameLabel)
        widget.newP_nameHBox.addWidget(widget.newP_nameLineEdit)

        widget.newP_descHBox = QHBoxLayout()
        widget.newP_descHBox.addWidget(widget.newP_descLabel)
        widget.newP_descHBox.addWidget(widget.newP_descLineEdit)

        # Layout for parameter VALUE settings:

        widget.newP_minSpinbox.setFixedWidth(75)
        widget.newP_maxSpinbox.setFixedWidth(75)
        widget.newP_stepSpinbox.setFixedWidth(75)

        widget.newP_minVBox = QVBoxLayout()
        widget.newP_minVBox.addWidget(widget.newP_minLabel)
        widget.newP_minVBox.addWidget(widget.newP_minSpinbox)

        widget.newP_maxVBox = QVBoxLayout()
        widget.newP_maxVBox.addWidget(widget.newP_maxLabel)
        widget.newP_maxVBox.addWidget(widget.newP_maxSpinbox)

        widget.newP_stepVBox = QVBoxLayout()
        widget.newP_stepVBox.addWidget(widget.newP_stepLabel)
        widget.newP_stepVBox.addWidget(widget.newP_stepSpinbox)

        widget.newP_valuesHBox = QHBoxLayout()  # layout for the 3 spin-boxes
        widget.newP_valuesHBox.addLayout(widget.newP_minVBox)
        widget.newP_valuesHBox.addLayout(widget.newP_maxVBox)
        widget.newP_valuesHBox.addLayout(widget.newP_stepVBox)
        widget.newP_valuesHBox.setAlignment(widget.newP_minVBox, Qt.AlignLeft)
        widget.newP_valuesHBox.setAlignment(widget.newP_maxVBox, Qt.AlignCenter)
        widget.newP_valuesHBox.setAlignment(widget.newP_stepVBox, Qt.AlignRight)

        # Layout for ADD & CLEAR buttons:

        widget.newP_clearButton.setFixedWidth(125)
        widget.newP_addButton.setFixedWidth(125)

        widget.newP_buttonHBox = QHBoxLayout()
        widget.newP_buttonHBox.addWidget(widget.newP_clearButton)
        widget.newP_buttonHBox.addWidget(widget.newP_addButton)

        # Frame:

        widget.newP_frame = QFrame()
        widget.newP_frame.setFrameStyle(QFrame.StyledPanel)

        widget.newP_vBox = QVBoxLayout(widget.newP_frame)
        widget.newP_vBox.setAlignment(Qt.AlignTop)
        widget.newP_vBox.addWidget(widget.newP_title)
        widget.newP_vBox.addLayout(widget.newP_typeHBox)
        widget.newP_vBox.addLayout(widget.newP_nameHBox)
        widget.newP_vBox.addLayout(widget.newP_descHBox)
        widget.newP_vBox.addLayout(widget.newP_valuesHBox)
        widget.newP_vBox.addSpacing(15)
        widget.newP_vBox.addLayout(widget.newP_buttonHBox)

    @staticmethod
    def _setup_parameter_set_layout(widget):

        widget.pSet_title.setFont(QFont("Ubuntu Mono", 9, QFont.Black))

        widget.pSet_frame = QFrame()
        widget.pSet_frame.setFrameStyle(QFrame.StyledPanel)

        widget.pSet_vBox = QVBoxLayout(widget.pSet_frame)
        widget.pSet_vBox.setAlignment(Qt.AlignTop)
        widget.pSet_vBox.addWidget(widget.pSet_title)
        widget.pSet_vBox.addWidget(widget.pSet_listWidget)

    @staticmethod
    def _setup_custom_row_layout(widget):

        widget.customRow_title.setFont(QFont("Ubuntu Mono", 9, QFont.Black))

        widget.customRow_addButton.setFixedWidth(125)
        widget.customRow_editButton.setFixedWidth(125)

        widget.customRow_buttonHBox = QHBoxLayout()
        widget.customRow_buttonHBox.addWidget(widget.customRow_addButton)
        widget.customRow_buttonHBox.addWidget(widget.customRow_editButton)

        widget.customRow_frame = QFrame()
        widget.customRow_frame.setFrameStyle(QFrame.StyledPanel)

        widget.customRow_vBox = QVBoxLayout(widget.customRow_frame)
        widget.customRow_vBox.setAlignment(Qt.AlignTop)
        widget.customRow_vBox.addWidget(widget.customRow_title)
        widget.customRow_vBox.addSpacing(10)
        widget.customRow_vBox.addLayout(widget.customRow_buttonHBox)

    @staticmethod
    def _setup_excel_creator_layout(widget):

        widget.create_title.setFont(QFont("Ubuntu Mono", 9, QFont.Black))

        widget.create_runtimeHBox = QHBoxLayout()
        widget.create_runtimeHBox.addWidget(widget.create_runtimeLabel)
        widget.create_runtimeHBox.addWidget(widget.create_runtimeSpinbox)

        widget.create_excelCreatorButton.setFont(QFont("Ubuntu Mono", 7, QFont.Black))
        widget.create_excelCreatorButton.setFixedWidth(100)

        widget.create_buttonHBox = QHBoxLayout()
        widget.create_buttonHBox.addWidget(widget.create_orderEditorCheckBox)
        widget.create_buttonHBox.addWidget(widget.create_excelCreatorButton)

        widget.create_frame = QFrame()
        widget.create_frame.setFrameStyle(QFrame.StyledPanel)

        widget.create_vBox = QVBoxLayout(widget.create_frame)
        widget.create_vBox.setAlignment(Qt.AlignTop)
        widget.create_vBox.addWidget(widget.create_title)
        widget.create_vBox.addWidget(widget.create_rowNumberLabel)
        widget.create_vBox.addLayout(widget.create_runtimeHBox)
        widget.create_vBox.addWidget(widget.create_sumRuntimeLabel)
        widget.create_vBox.addLayout(widget.create_buttonHBox)


class FluxminatorLayout:
    """ UI class for setting up the Fluxminator View GUI """

    @staticmethod
    def setup_layout(flux_widget):      # FluxminatorView widget

        FluxminatorLayout._setup_settings_layout(flux_widget)
        FluxminatorLayout._setup_model_layout(flux_widget)
        FluxminatorLayout._setup_scenario_parameters_layout(flux_widget)
        FluxminatorLayout._setup_runner_layout(flux_widget)

        # LAYOUT - TOP:

        flux_widget.topSplitter = QSplitter(Qt.Horizontal)
        flux_widget.topSplitter.addWidget(flux_widget.settingsSplitter)
        flux_widget.topSplitter.addWidget(flux_widget.fluxModelSetupFrame)

        # LAYOUT - MIDDLE:

        flux_widget.splitter = QSplitter(Qt.Vertical)
        flux_widget.splitter.addWidget(flux_widget.topSplitter)
        flux_widget.splitter.addWidget(flux_widget.scenarioSetupFrame)
        flux_widget.splitter.addWidget(flux_widget.runnerFrame)

        # LAYOUT - WHOLE:

        flux_widget.VBox = QVBoxLayout()
        flux_widget.VBox.setAlignment(Qt.AlignLeft)
        flux_widget.VBox.addWidget(flux_widget.splitter)

        flux_widget.setLayout(flux_widget.VBox)

    @staticmethod
    def _setup_settings_layout(flux_widget):

        # Settings:

        flux_widget.settingsFrame = QFrame()
        flux_widget.settingsFrame.setFrameStyle(QFrame.StyledPanel)

        flux_widget.settingsVBox = QVBoxLayout(flux_widget.settingsFrame)
        flux_widget.settingsVBox.addWidget(flux_widget.newSessionButton)
        flux_widget.settingsVBox.addWidget(flux_widget.oldSessionButton)
        flux_widget.settingsVBox.addWidget(flux_widget.summarySessionButton)

        # Extra settings:

        flux_widget.settingsTitle.setFont(QFont("Ubuntu Mono", 9, QFont.Black))

        flux_widget.gammaNameLineEdit.setFixedWidth(75)
        flux_widget.gammaNameLineEdit.setAlignment(Qt.AlignRight)

        flux_widget.currentNameLineEdit.setFixedWidth(75)
        flux_widget.currentNameLineEdit.setAlignment(Qt.AlignRight)

        flux_widget.currentSourceNameLineEdit.setFixedWidth(75)
        flux_widget.currentSourceNameLineEdit.setAlignment(Qt.AlignRight)

        flux_widget.nameVBox = QVBoxLayout()
        flux_widget.nameVBox.addWidget(flux_widget.gammaNameLabel)
        flux_widget.nameVBox.addWidget(flux_widget.currentNameLabel)
        flux_widget.nameVBox.addWidget(flux_widget.currentSourceNameLabel)

        flux_widget.editorVBox = QVBoxLayout()
        flux_widget.editorVBox.setAlignment(Qt.AlignLeft)
        flux_widget.editorVBox.addWidget(flux_widget.gammaNameLineEdit)
        flux_widget.editorVBox.addWidget(flux_widget.currentNameLineEdit)
        flux_widget.editorVBox.addWidget(flux_widget.currentSourceNameLineEdit)

        flux_widget.nameEditorHBox = QHBoxLayout()
        flux_widget.nameEditorHBox.addLayout(flux_widget.nameVBox)
        flux_widget.nameEditorHBox.addLayout(flux_widget.editorVBox)

        flux_widget.extraSettingsFrame = QFrame()
        flux_widget.extraSettingsFrame.setFrameStyle(QFrame.StyledPanel)

        flux_widget.extraSettingsVBox = QVBoxLayout(flux_widget.extraSettingsFrame)
        flux_widget.extraSettingsVBox.setAlignment(Qt.AlignTop)
        flux_widget.extraSettingsVBox.addWidget(flux_widget.settingsTitle)
        flux_widget.extraSettingsVBox.addSpacing(20)
        flux_widget.extraSettingsVBox.addWidget(flux_widget.deleteCheckBox)
        flux_widget.extraSettingsVBox.addWidget(flux_widget.batchModeCheckBox)
        flux_widget.extraSettingsVBox.addWidget(flux_widget.priceCalcCheckBox)
        flux_widget.extraSettingsVBox.addSpacing(20)
        flux_widget.extraSettingsVBox.addLayout(flux_widget.nameEditorHBox)

        flux_widget.settingsSplitter = QSplitter(Qt.Vertical)
        flux_widget.settingsSplitter.addWidget(flux_widget.settingsFrame)
        flux_widget.settingsSplitter.addWidget(flux_widget.extraSettingsFrame)

    @staticmethod
    def _setup_model_layout(flux_widget):

        flux_widget.modelTitle.setFont(QFont("Ubuntu Mono", 9, QFont.Black))

        flux_widget.slotNumSpinBox.setFixedWidth(60)
        flux_widget.poleNumSpinBox.setFixedWidth(60)

        flux_widget.fluxModelButton.setFixedWidth(140)
        flux_widget.motorParamExcelButton.setFixedWidth(140)
        flux_widget.priceCalcButton.setFixedWidth(140)

        flux_widget.fluxModelLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        flux_widget.fluxModelLabel.setWordWrap(True)

        flux_widget.pixMap = flux_widget.pixMap.scaled(280, 280, Qt.KeepAspectRatio)

        # LAYOUT FOR MOTOR PARAMETERS:

        flux_widget.slotHBox = QHBoxLayout()
        flux_widget.slotHBox.addWidget(flux_widget.slotNumLabel)
        flux_widget.slotHBox.addWidget(flux_widget.slotNumSpinBox)

        flux_widget.poleHBox = QHBoxLayout()
        flux_widget.poleHBox.addWidget(flux_widget.poleNumLabel)
        flux_widget.poleHBox.addWidget(flux_widget.poleNumSpinBox)

        flux_widget.motorParametersVBox = QVBoxLayout()
        flux_widget.motorParametersVBox.setAlignment(Qt.AlignVCenter)
        flux_widget.motorParametersVBox.addLayout(flux_widget.slotHBox)
        flux_widget.motorParametersVBox.addLayout(flux_widget.poleHBox)
        flux_widget.motorParametersVBox.addSpacing(20)
        flux_widget.motorParametersVBox.addWidget(flux_widget.motorParamExcelButton)
        flux_widget.motorParametersVBox.addWidget(flux_widget.priceCalcButton)

        flux_widget.motorHBox = QHBoxLayout()
        flux_widget.motorHBox.addLayout(flux_widget.motorParametersVBox)
        flux_widget.motorHBox.addWidget(flux_widget.pixLabel)

        # LAYOUT FOR THE MODEL SETUP:

        flux_widget.fluxModelHBox = QHBoxLayout()
        flux_widget.fluxModelHBox.addWidget(flux_widget.fluxModelButton)
        flux_widget.fluxModelHBox.addWidget(flux_widget.fluxModelLabel)

        flux_widget.fluxModelSetupFrame = QFrame()
        flux_widget.fluxModelSetupFrame.setFrameStyle(QFrame.StyledPanel)

        flux_widget.fluxModelSetupVBox = QVBoxLayout(flux_widget.fluxModelSetupFrame)
        flux_widget.fluxModelSetupVBox.addWidget(flux_widget.modelTitle)
        flux_widget.fluxModelSetupVBox.addLayout(flux_widget.fluxModelHBox)
        flux_widget.fluxModelSetupVBox.addLayout(flux_widget.motorHBox)

    @staticmethod
    def _setup_scenario_parameters_layout(flux_widget):

        flux_widget.scenarioTitle.setFont(QFont("Ubuntu Mono", 9, QFont.Black))

        # Cogging, ripple, current, gamma values for the table:

        flux_widget.scenarioParameters = [[], [], [], []]
        flux_widget.scenarioParameters[0].extend([QLabel("Cogging:"), flux_widget.coggingMin, flux_widget.coggingMax,
                                                  flux_widget.coggingStep, QLabel("[mDeg]")])
        flux_widget.scenarioParameters[1].extend([QLabel("Ripple:"), flux_widget.rippleMin, flux_widget.rippleMax,
                                                  flux_widget.rippleStep, QLabel("[mDeg]")])
        flux_widget.scenarioParameters[2].extend([QLabel("Current:"), flux_widget.currentMin, flux_widget.currentMax,
                                                  flux_widget.currentStep, QLabel("[A]")])
        flux_widget.scenarioParameters[3].extend([QLabel("Gamma:"), flux_widget.gammaMin, flux_widget.gammaMax,
                                                  flux_widget.gammaStep, QLabel("[eDeg]")])

        for i, j in itertools.product(range(3), range(1, 4)):
            flux_widget.scenarioParameters[i][j].setDecimals(2)
            flux_widget.scenarioParameters[i][j].setSingleStep(0.01)
            flux_widget.scenarioParameters[i][j].setMaximum(1000)
            flux_widget.scenarioParameters[i][j].setFixedWidth(100)

        for i in range(1, 4):
            flux_widget.scenarioParameters[3][i].setDecimals(1)
            flux_widget.scenarioParameters[3][i].setSingleStep(0.1)
            flux_widget.scenarioParameters[3][i].setMaximum(1000)
            flux_widget.scenarioParameters[3][j].setFixedWidth(100)

        flux_widget.gammaMin.setMinimum(-1000)
        flux_widget.gammaMax.setMinimum(-1000)

        # CONTAINERS FOR THE LAYOUT:

        flux_widget.loadDepHBox = QHBoxLayout()
        flux_widget.loadDepHBox.addSpacing(23)
        flux_widget.loadDepHBox.addWidget(flux_widget.loadDepCheckBox)

        flux_widget.gammaDepHBox = QHBoxLayout()
        flux_widget.gammaDepHBox.addSpacing(23)
        flux_widget.gammaDepHBox.addWidget(flux_widget.gammaDepCheckBox)

        flux_widget.scenarioSetupVBox = QVBoxLayout()
        flux_widget.scenarioSetupVBox.addWidget(flux_widget.scenarioTitle)
        flux_widget.scenarioSetupVBox.addSpacing(10)
        flux_widget.scenarioSetupVBox.addWidget(flux_widget.coggingScenarioCheckBox)
        flux_widget.scenarioSetupVBox.addWidget(flux_widget.rippleScenarioCheckBox)
        flux_widget.scenarioSetupVBox.addLayout(flux_widget.loadDepHBox)
        flux_widget.scenarioSetupVBox.addLayout(flux_widget.gammaDepHBox)

        # GRID for Cogging, Ripple, Current, Gamma:

        flux_widget.scenarioSetupGrid = QGridLayout()
        flux_widget.scenarioSetupGrid.addWidget(QLabel("Minimum:"), 0, 1)
        flux_widget.scenarioSetupGrid.addWidget(QLabel("Maximum:"), 0, 2)
        flux_widget.scenarioSetupGrid.addWidget(QLabel("Step:"), 0, 3)

        for i, j in itertools.product(range(1, 5), range(0, 5)):
            flux_widget.scenarioSetupGrid.addWidget((flux_widget.scenarioParameters[i - 1][j]), i, j)

        # FRAME:

        flux_widget.scenarioSetupFrame = QFrame()
        flux_widget.scenarioSetupFrame.setFrameStyle(QFrame.StyledPanel)

        flux_widget.scenarioSetupHBox = QHBoxLayout(flux_widget.scenarioSetupFrame)
        flux_widget.scenarioSetupHBox.addLayout(flux_widget.scenarioSetupVBox)
        flux_widget.scenarioSetupHBox.addLayout(flux_widget.scenarioSetupGrid)

    @staticmethod
    def _setup_runner_layout(flux_widget):

        flux_widget.progressBar.setFixedHeight(15)
        flux_widget.progressBar.setFixedWidth(454)

        flux_widget.runButton.setFixedWidth(100)
        flux_widget.clearButton.setFixedWidth(100)

        flux_widget.runButton.setFont(QFont("Ubuntu Mono", 7, QFont.Black))
        flux_widget.clearButton.setFont(QFont("Ubuntu Mono", 7, QFont.Black))

        # LAYOUT:

        flux_widget.progressVBox = QVBoxLayout()
        flux_widget.progressVBox.addWidget(flux_widget.progressBar)
        flux_widget.progressVBox.addWidget(flux_widget.progressLabel)

        flux_widget.runnerFrame = QFrame()
        flux_widget.runnerFrame.setFrameStyle(QFrame.StyledPanel)

        flux_widget.runnerHBox = QHBoxLayout(flux_widget.runnerFrame)
        flux_widget.runnerHBox.addLayout(flux_widget.progressVBox)
        flux_widget.runnerHBox.addWidget(flux_widget.runButton)
        flux_widget.runnerHBox.addWidget(flux_widget.clearButton)
