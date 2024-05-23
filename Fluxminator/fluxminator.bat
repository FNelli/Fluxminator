@ECHO off
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: 
:: It checks, if the required python virtual environment exists,
:: and if not, tries to create it.
:: After that or otherwise, it calls the main fluxminator.py.
::
:: What does it do:
::    - checks whether pip.ini is in proper path and copies it to
::      proper path if not exist
::    - creates a virtual environment from the specified python
::      version if not exists.
::    - installs packages defined in the requirements.txt
::    - activates the virtual environment
::    - calls Fluxminator/main.py
::
:: Usage:
::    - call it:
::      > fluxminator.bat --help
::      > fluxminator --help
::
:: Note:
::    After calling this, the virtual environment stays activated!
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: CALLING common virtualenv checker
cmd /c "copy_pip_proxy.bat"
cmd /c "venv_check.bat"

SET "VENV_DIR=fluxscript_venv"
ECHO "> Activating virtual environment from %VENV_DIR%..."
CALL .\%VENV_DIR%\Scripts\activate.bat

echo "> Calling main.py..."

python -m main %*
