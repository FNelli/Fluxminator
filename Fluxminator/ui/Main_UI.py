import sys
import os

from PyQt5 import QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QMenu, QFileDialog, \
    QAction, QApplication, QMessageBox, QShortcut, QLabel, QStackedWidget


class Main_UI:
    """ UI class for setting up the main window GUI """

    def setup_main_UI(self, main_window):

        # Fluxminator:
        main_window.fluxAct = QAction('Flux automation')
        main_window.fluxAct.setCheckable(True)
        main_window.fluxAct.setToolTip("Set up simulations for Flux")

        main_window.fluxPathAct = QAction('Change Flux Application path')
        main_window.fluxPathAct.setToolTip("Example:\nC:/Program Files/Altair/2019/")

        # 2D map:       TODO FUTURE DEVELOPMENT
        main_window.mapAct = QAction('2D map')
        main_window.mapAct.setCheckable(True)
        main_window.mapAct.setToolTip("FUTURE DEVELOPMENT")

        # FFT window:   TODO FUTURE DEVELOPMENT
        main_window.fftAct = QAction('FFT')
        main_window.fftAct.setCheckable(True)
        main_window.fftAct.setToolTip("FUTURE DEVELOPMENT")

        # EXIT:
        main_window.exitAct = QAction('Exit')

        # USER GUIDE:
        main_window.userGuideAct = QAction('User Guide')

        # MENU:
        main_window.menuBar = main_window.menuBar()
        main_window.fileMenu = main_window.menuBar.addMenu('File')
        main_window.helpMenu = main_window.menuBar.addMenu('Help')

        main_window.fluxMenu = QMenu('Flux')
        main_window.fluxMenu.setToolTipsVisible(True)
        main_window.fluxMenu.addAction(main_window.fluxAct)
        main_window.fluxMenu.addAction(main_window.fluxPathAct)

        main_window.fileMenu.addMenu(main_window.fluxMenu)
        main_window.fileMenu.addAction(main_window.mapAct)
        main_window.fileMenu.addAction(main_window.fftAct)
        main_window.fileMenu.addAction(main_window.exitAct)

        main_window.helpMenu.addAction(main_window.userGuideAct)

        # TOOLBAR:

        main_window.toolBar = main_window.addToolBar('')
        main_window.toolBar.setFixedHeight(40)
        main_window.toolBar.setFont(QFont("Ubuntu Mono", 9))

        main_window.toolBar.addAction(main_window.fluxAct)
        main_window.toolBar.addAction(main_window.mapAct)
        main_window.toolBar.addAction(main_window.fftAct)

        # GUI:

        main_window.setWindowTitle("Fluxminator")
        main_window.setWindowIcon(QtGui.QIcon("icon.ico"))

        main_window.centralWidget = QStackedWidget()
        main_window.setCentralWidget(main_window.centralWidget)

        main_window.centralWidget.addWidget(main_window.fluxminatorView)
        main_window.centralWidget.addWidget(main_window.mapWindow)
        main_window.centralWidget.addWidget(main_window.fftWindow)

        main_window.centralWidget.setCurrentWidget(main_window.fluxminatorView)



