from scipy.fftpack import fft
from cmath import phase

from PyQt5.QtWidgets import QMessageBox


def popup_message(view, message, title="Error"):
    """ Pop up a message box, usually for displaying error messages """

    mB = QMessageBox(view)

    if title == "Error":
        mB.setIcon(QMessageBox.Critical)
    else:
        mB.setIcon(QMessageBox.Information)

    mB.setText(message)
    mB.setWindowTitle(title)
    mB.setStandardButtons(QMessageBox.Ok)

    mB.show()
        
        
def fft_(rotor_position, values, period=360, multiplier=100):
    """ FFT function, used by Cogging, Ripple & BEMF objects """

    rotor_pos_step = rotor_position[1] - rotor_position[0]
    rotor_pos_range = rotor_position[-1] - (rotor_position[0] - rotor_pos_step)

    data_fft = fft(values) / len(values) * 2

    data_fft_harmonics = [0]
    data_fft_abs = []
    data_fft_phase = []

    for current_data in data_fft:
        data_fft_abs.append(abs(current_data) * multiplier)        # [Ncm] for Cogging, Ripple & [V] for BEMF
        data_fft_phase.append(phase(current_data))

    data_fft_abs[0] = data_fft_abs[0] / 2

    first_harmonic = period / rotor_pos_range
    act_harmonic = first_harmonic

    for i in range(1, len(data_fft_abs)):
        data_fft_harmonics.append(act_harmonic)
        act_harmonic += first_harmonic

    return data_fft_harmonics, data_fft_abs, data_fft_phase
