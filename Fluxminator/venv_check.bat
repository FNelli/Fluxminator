@ECHO off

SET "PY_MAJOR_VER=3"
SET "PY_MINOR_VER=9"
SET "PYTHON=C:\Python39\python.exe"

SET "VENV_DIR=fluxscript_venv"

IF NOT EXIST %VENV_DIR% (
    ECHO "> Virtual environment does not exist, trying to create into %VENV_DIR%... This can take a while..."
    :: check python version
    PYTHON -c "import sys; sys.exit(0 if sys.version_info.major==%PY_MAJOR_VER% and sys.version_info.minor>=%PY_MINOR_VER% else 1)"
    IF %ERRORLEVEL% == 1 (
        ECHO "Python version mismatch!"
        EXIT /b 1
    )
    :: create venv
    PYTHON -m venv %VENV_DIR% --system-site-packages
    :: activate venv
    CALL .\%VENV_DIR%\Scripts\activate.bat
    ECHO "> done."
    ECHO "> upgrading pip..."
    python -m pip install --upgrade pip
    ECHO "> done."
    ECHO "> Installing requirements..."
    :: now the virtualenv is activated, we can call python from there
    python -m pip install --ignore-installed -r .\requirements.txt
    ECHO "> done."
) ELSE (
    CALL .\%VENV_DIR%\Scripts\activate.bat
)