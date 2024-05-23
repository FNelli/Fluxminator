import sys
import unittest

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from PyQt5.QtTest import QTest

from fluxminator.View import FluxminatorView
from fluxminator.Model import Model
from fluxminator.Presenter import Presenter


app = QApplication(sys.argv)


class FluxminatorTest(unittest.TestCase):

    def setUp(self):
        """ Create the GUI """
        self.model = Model()
        self.view = FluxminatorView()
        self.presenter = Presenter(model=self.model, view=self.view)

    def test_defaults(self):
        """ Test the GUI in its default state """
        self.assertEqual(self.view.coggingScenarioCheckBox.isChecked(), True)
        self.assertEqual(self.view.rippleScenarioCheckBox.isChecked(), True)

    def test_cogging_parameters(self):
        """ Set an invalid value for the minimum Cogging position """
        self.view.coggingMin.setValue(-1)
        self.assertEqual(self.view.coggingMin.value(), 0)

    def test_flux_starting(self):
        """ Start execution before proper setup """
        QTest.mouseClick(self.view.runButton, Qt.LeftButton)
        self.assertEqual(self.model.get_executionInProgress(), False)


if __name__ == "__main__":
    unittest.main()
