import sys
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut
from PyQt5 import QtGui
from fluxminator.View import FluxminatorView
from fluxminator.Model import Model
from fluxminator.Presenter import Presenter
from fluxminator.Constants import FLUX_PATH_INFO_FILE

from ui.Main_UI import Main_UI
from fft.FFTWidget import FFTWidget
from map.MapWidget import MapWidget


class MainWindow(QMainWindow, Main_UI):
    """ Main Window class definition for the application """

    def __init__(self):

        super().__init__()

        self.exitShortcut = QShortcut(QtGui.QKeySequence("Ctrl+Q"), self)
        self.exitShortcut.activated.connect(self.close)

        # Fluxminator (MVP):
        self.fluxminatorModel = Model()
        self.fluxminatorView = FluxminatorView()

        # 2D map & FFT Window: TODO FUTURE DEVELOPMENT
        self.mapWindow = MapWidget()
        self.fftWindow = FFTWidget()
        self.fluxminatorPresenter = Presenter(model=self.fluxminatorModel, view=self.fluxminatorView)

        # Set up the layout for the main window (Main_UI):
        self.setup_main_UI(self)

        # Set up the main window related bindings:
        self.set_main_bindings()

    def set_main_bindings(self):
        """ Functions for switching the widget in the main window """

        self.fluxAct.triggered.connect(self.select_flux_window)
        self.fluxAct.triggered.connect(lambda: self.fftAct.setChecked(False))
        self.fluxAct.triggered.connect(lambda: self.mapAct.setChecked(False))

        self.mapAct.triggered.connect(self.select_map_window)
        self.mapAct.triggered.connect(lambda: self.fftAct.setChecked(False))
        self.mapAct.triggered.connect(lambda: self.fluxAct.setChecked(False))

        self.fftAct.triggered.connect(self.select_fft_window)
        self.fftAct.triggered.connect(lambda: self.fluxAct.setChecked(False))
        self.fftAct.triggered.connect(lambda: self.mapAct.setChecked(False))

        self.fluxPathAct.triggered.connect(self.fluxminatorPresenter.change_flux_directory)  # TODO

        self.userGuideAct.triggered.connect(self.help)  # TODO

        self.exitAct.triggered.connect(self.close)

    def set_toolbar_font(self, flux=False, map_=False, fft=False):
        """ Configure bold or normal font type for the menu items """
        font = self.fluxAct.font()

        font.setBold(flux)
        self.fluxAct.setFont(font)

        font.setBold(map_)
        self.mapAct.setFont(font)

        font.setBold(fft)
        self.fftAct.setFont(font)

    def select_flux_window(self):
        """ Display the Fluxminator widget on the main window"""
        self.set_toolbar_font(flux=True)
        self.centralWidget.setCurrentWidget(self.fluxminatorView)
        self.show()

    def select_map_window(self):
        """ Display the 2D map widget on the main window """
        self.set_toolbar_font(map_=True)
        self.centralWidget.setCurrentWidget(self.mapWindow)

    def select_fft_window(self):
        """ Display the FFT widget on the main window """
        self.set_toolbar_font(fft=True)
        self.centralWidget.setCurrentWidget(self.fftWindow)

    def help(self):    # TODO
        """ Display the user guide """
        print("USER GUIDE - coming soon")

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        """ Also close the Fluxminator subwidgets """
        if self.fluxminatorView.specialParameterSetCreatorWidget is not None:
            self.fluxminatorView.specialParameterSetCreatorWidget.close()
        self.fluxminatorView.parameterSetCreatorWidget.close()


def set_flux_path_info_file():
    """ Create the WorkingDirectory folder and generate a text file for the path information for the Flux app """

    current_directory = os.getcwd()

    working_directory = os.path.join(current_directory, r'WorkingDirectory')
    if not os.path.exists(working_directory):
        os.makedirs(working_directory)

    if not os.path.exists(FLUX_PATH_INFO_FILE):
        flux_directory_file = open(FLUX_PATH_INFO_FILE, "w")
        flux_directory_file.close()


def main():

    set_flux_path_info_file()

    # Create the application instance
    app = QApplication(sys.argv)

    # Initialize the main window
    main_window = MainWindow()

    # Display the main view
    main_window.show()

    # Start the application's event loop
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()





