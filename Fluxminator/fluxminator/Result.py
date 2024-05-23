
import numpy as np
import xlrd

from fluxminator.Constants import *
import fluxminator.support_functions as sup_fun

# OBJECTS FOR PROCESSING THE RAW DATA FILES FROM FLUX:


class Cogging:

    def __init__(self, rot_pos, torque):

        self.rotorPosition = np.array(rot_pos)
        self.coggingValue = np.array(torque)

        self.peakToPeak = self.coggingValue.ptp() * 100     # [Ncm]

        # harmonics, amplitude, phase:
        self.fftValues = [[], [], []]
        self.fftValues[0], self.fftValues[1], self.fftValues[2] = sup_fun.fft_(rotor_position=self.rotorPosition,
                                                                               values=self.coggingValue)

    def get_p2p(self): return self.peakToPeak
    def get_fftValues(self): return self.fftValues


class Ripple:

    def __init__(self, gamma, i_max, rot_pos, torque, voltage, current):

        self.gamma = gamma
        self.iMax = i_max

        self.rotorPositions = np.array(rot_pos)
        self.rippleValues = np.array(torque)
        self.voltageValues = np.array(voltage)
        self.currentValues = np.array(current)

        self.peakToPeak = self.rippleValues.ptp() * 100      # [Ncm]

        self.torqueMean = self.rippleValues.mean()

        # harmonics, amplitude, phase:
        self.fftValues = [[], [], []]
        self.fftValues[0], self.fftValues[1], self.fftValues[2] = sup_fun.fft_(rotor_position=self.rotorPositions,
                                                                               values=self.rippleValues)

    def get_rotorPositions(self): return self.rotorPositions
    def get_rippleValues(self): return self.rippleValues
    def get_voltageValues(self): return self.voltageValues
    def get_currentValues(self): return self.currentValues

    def get_p2p(self): return self.peakToPeak
    def get_torqueMean(self): return self.torqueMean
    def get_fftValues(self): return self.fftValues


class BEMF:

    def __init__(self, rot_pos, voltage, pole_num):

        self.poleNumber = pole_num
        self.period = None
        self.valid = None

        self.rotorPosition = np.array(rot_pos)
        self.voltageValue = np.array(voltage)

        self.period = self._period()

        # harmonics, amplitude, phase:
        self.fftValues = [[], [], []]
        self.fftValues[0], self.fftValues[1], self.fftValues[2] = sup_fun.fft_(rotor_position=self.rotorPosition,
                                                                               values=self.voltageValue,
                                                                               period=self.period, multiplier=1)

        self.rmsValue = self._rms()

    def get_rmsValue(self): return self.rmsValue
    def get_fftValues(self): return self.fftValues

    def is_valid_BEMF(self): return self.valid

    def _period(self):

        period = 360 / (self.poleNumber / 2)

        rotor_pos_step = self.rotorPosition[1] - self.rotorPosition[0]
        rotor_pos_range = self.rotorPosition[-1] - (self.rotorPosition[0] - rotor_pos_step)

        if period == rotor_pos_range:
            self.valid = True
        else:
            self.valid = False

        return period

    def _rms(self):

        # effective value
        amplitudes = self.fftValues[1]
        return np.sqrt(np.sum(np.square(amplitudes)) / len(amplitudes))


class Result:

    def __init__(self):

        self.cogging1Stack = None
        self.cogging2Stack = None
        self.cogging3Stack = None

        self.BEMF1Stack = None
        self.BEMF2Stack = None
        self.BEMF3Stack = None

        self.rippleModels = {}
        self.ripple1Stack = {}
        self.ripple2Stack = {}
        self.ripple3Stack = {}

    def get_cogging1Stack(self): return self.cogging1Stack
    def get_cogging2Stack(self): return self.cogging2Stack
    def get_cogging3Stack(self): return self.cogging3Stack

    def get_BEMF1Stack(self): return self.BEMF1Stack
    def get_BEMF2Stack(self): return self.BEMF2Stack
    def get_BEMF3Stack(self): return self.BEMF3Stack

    def get_rippleModels(self): return self.rippleModels
    def get_ripple1Stack(self): return self.ripple1Stack
    def get_ripple2Stack(self): return self.ripple2Stack
    def get_ripple3Stack(self): return self.ripple3Stack

    def setup_Cogging_BEMF(self, file, flux_model, scenario_id):
        """ Set up Cogging and BEMF objects based on the raw results files from Flux """

        step_number = flux_model.positionCogging.get_numberOfSteps() - 1        # first step is not in the result file

        try:
            rotor_position, magnetic_torque, voltage, _ = Result._read_raw_data_files("Cogging", file, step_number)
        except IOError:
            return False

        pole_num = flux_model.motor.get_numberPole()
        gammas_for2stack = flux_model.get_gammasFor2Stack()
        gammas_for3stack = flux_model.get_gammasFor3Stack()

        if flux_model.rangeGamma.is_value_in_range(0):
            self.cogging1Stack = Cogging(rot_pos=rotor_position, torque=magnetic_torque)
            self.BEMF1Stack = BEMF(rot_pos=rotor_position, voltage=voltage, pole_num=pole_num)

        if gammas_for2stack is not None:

            if (flux_model.rangeGamma.is_value_in_range(gammas_for2stack[0])
                    and flux_model.rangeGamma.is_value_in_range(gammas_for2stack[1])) or scenario_id == 1:

                torques = [None, None]
                voltages = [None, None]

                for i in range(2):
                    rotation = int(round(
                        (gammas_for2stack[i] / (pole_num / 2)) / flux_model.positionCogging.get_step(), 0))

                    torques[i] = self._rotate(magnetic_torque, rotation)
                    voltages[i] = self._rotate(voltage, rotation)

                new_torque = (np.array(torques[0]) + np.array(torques[1])) / 2
                new_voltage = (np.array(voltages[0]) + np.array(voltages[1])) / 2

                self.cogging2Stack = Cogging(rotor_position, new_torque)
                self.BEMF2Stack = BEMF(rotor_position, new_voltage, pole_num)

        if gammas_for3stack is not None:

            if (flux_model.rangeGamma.is_value_in_range(gammas_for3stack[0])
                    and flux_model.rangeGamma.is_value_in_range(gammas_for3stack[1])
                    and flux_model.rangeGamma.is_value_in_range(gammas_for3stack[2])) or scenario_id == 1:

                torques = [None, None, None]
                voltages = [None, None, None]

                for i in range(3):
                    rotation = int(round(
                        (gammas_for3stack[i] / (pole_num / 2)) / flux_model.positionCogging.get_step(), 0))

                    torques[i] = self._rotate(magnetic_torque, rotation)
                    voltages[i] = self._rotate(voltage, rotation)

                new_torque = (np.array(torques[0]) + np.array(torques[1]) + np.array(torques[2])) / 3
                new_voltage = (np.array(voltages[0]) + np.array(voltages[1]) + np.array(voltages[2])) / 3

                self.cogging3Stack = Cogging(rotor_position, new_torque)
                self.BEMF3Stack = BEMF(rotor_position, new_voltage, pole_num)

        return True

    def setup_Ripple(self, file, flux_model):
        """ Set up Ripple objects based on the raw results files from Flux """

        step_number = flux_model.positionRipple.get_numberOfSteps() - 1         # first step is not in the result file

        current_values = flux_model.rangeCurrent.get_all_values()
        gamma_values = flux_model.rangeGamma.get_all_values()

        pole_num = flux_model.motor.get_numberPole()
        gammas_for2stack = flux_model.get_gammasFor2Stack()
        gammas_for3stack = flux_model.get_gammasFor3Stack()

        for current_index, current_value in enumerate(current_values):

            self.rippleModels[current_value] = []

            ripples_for_2stack = []  # ripples for 2/3 Stack motor (before rotate)
            ripples_for_3stack = []

            for gamma_index, gamma_value in enumerate(gamma_values):

                try:
                    rotor_position, magnetic_torque, voltage, current = \
                        Result._read_raw_data_files("Ripple", file.format(current_index+1, gamma_index+1), step_number)
                except IOError:
                    return False

                ripple = Ripple(gamma_value, current_value, rotor_position, magnetic_torque, voltage, current)

                self.rippleModels[current_value].append(ripple)

                if gamma_value == 0:
                    self.ripple1Stack[current_value] = ripple
                if gamma_value in gammas_for2stack:
                    ripples_for_2stack.append(ripple)
                if gamma_value in gammas_for3stack:
                    ripples_for_3stack.append(ripple)

            if len(ripples_for_2stack) == 2:
                self.ripple2Stack[current_value] = Result._create_skewed_ripple(flux_model, 2, ripples_for_2stack,
                                                                                gammas_for2stack, pole_num, current_value)
            if len(ripples_for_3stack) == 3:
                self.ripple3Stack[current_value] = Result._create_skewed_ripple(flux_model, 3, ripples_for_3stack,
                                                                                gammas_for3stack, pole_num, current_value)
        return True

    @staticmethod
    def _read_raw_data_files(type_, file, step_number):
        """ Read the raw data files provided by the Flux software after each simulation """

        rotor_position = []
        magnetic_torque = []
        voltage = []
        current = []

        if type_ == "Cogging":
            start_index = RAW_COGGING_FILE_START_INDEX
        else:       # Ripple
            start_index = RAW_RIPPLE_FILE_START_INDEX

        wb = xlrd.open_workbook(file)
        ws = wb.sheet_by_index(0)

        for i in range(start_index, start_index + step_number):
            values = ws.row_values(rowx=i, start_colx=1, end_colx=5)

            rotor_position.append(values[0])
            magnetic_torque.append(values[1])
            voltage.append(values[2])
            current.append(values[3])

        wb.release_resources()

        return rotor_position, magnetic_torque, voltage, current

    @staticmethod
    def _create_skewed_ripple(flux_model, stack_number, ripples_for_skewing, gammas_for_skewing, pole_num, current_value):
        """ Create a skewed ripple object for the motor with 2 or 3 stacks """

        if stack_number == 2:
            torque = [None, None]
            voltage = [None, None]
            current = [None, None]
        else:
            torque = [None, None, None]
            voltage = [None, None, None]
            current = [None, None, None]

        rotor_positions = ripples_for_skewing[0].get_rotorPositions()

        for i in range(stack_number):
            rotation = int(round(
                (gammas_for_skewing[i] / (pole_num / 2)) / flux_model.positionRipple.get_step(), 0))

            torque[i] = Result._rotate(ripples_for_skewing[i].get_rippleValues(), rotation)
            voltage[i] = Result._rotate(ripples_for_skewing[i].get_voltageValues(), rotation)
            current[i] = Result._rotate(ripples_for_skewing[i].get_currentValues(), rotation)

        if stack_number == 2:
            new_torque = (np.array(torque[0]) + np.array(torque[1])) / 2
            new_voltage = (np.array(voltage[0]) + np.array(voltage[1])) / 2
            new_current = (np.array(current[0]) + np.array(current[1])) / 2
        else:
            new_torque = (np.array(torque[0]) + np.array(torque[1]) + np.array(torque[2])) / 3
            new_voltage = (np.array(voltage[0]) + np.array(voltage[1]) + np.array(voltage[2])) / 3
            new_current = (np.array(current[0]) + np.array(current[1]) + np.array(current[2])) / 3

        return Ripple(0, current_value, rotor_positions, new_torque, new_voltage, new_current)

    @staticmethod
    def _rotate(data, rotation):
        """ Shift the values in the list """
        return np.concatenate((data[-rotation:], data[:-rotation]), axis=None)
