
from openpyxl.styles import Color, PatternFill
from openpyxl.styles.borders import Border, Side, BORDER_THIN

# Altair Flux:

FLUX_PATH_INFO_FILE = "WorkingDirectory/flux_directory.txt"
FLUX_EXE_PATH = "\\flux\Flux\Bin\prg\win64\\flux.exe"
PYFLUX_SCRIPT_NAME = "Script_3_0.py"

RAW_COGGING_FILE_START_INDEX = 17
RAW_RIPPLE_FILE_START_INDEX = 18

# Execution result options:

EXECUTION_DONE = "Execution is complete!"
EXECUTION_STOP = "Execution is halted!"
EXECUTION_ERROR = "Unknown error occurred during execution!"

RAW_COGGING_FILE_ERROR = "Something went wrong during the processing of the raw cogging file!"
RAW_RIPPLE_FILE_ERROR = "Something went wrong during the processing of the raw ripple file!"

MISSING_RAW_FILES = "No raw result files were found for the summary creator session!"
RESULT_FILE_IO_ERROR = "Something went wrong during the updating and saving of the result files!"

# Excel file styling:

THYSSEN_BLUE = Color(rgb='00B0F0')
THYSSEN_FILL = PatternFill(patternType='solid', fgColor=THYSSEN_BLUE)

DEFAULT_BORDER = Border(
    left=Side(border_style=BORDER_THIN, color='00000000'),
    right=Side(border_style=BORDER_THIN, color='00000000'),
    top=Side(border_style=BORDER_THIN, color='00000000'),
    bottom=Side(border_style=BORDER_THIN, color='00000000'))

VERTICAL_BORDER = Border(
    left=Side(border_style=BORDER_THIN, color='00000000'),
    right=Side(border_style=BORDER_THIN, color='00000000'),)

BOTTOM_BORDER = Border(
    left=Side(border_style=BORDER_THIN, color='00000000'),
    right=Side(border_style=BORDER_THIN, color='00000000'),
    bottom=Side(border_style=BORDER_THIN, color='00000000'))
