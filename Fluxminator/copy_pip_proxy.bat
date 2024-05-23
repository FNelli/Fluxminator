@ECHO off
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: copy_pip_proxy.bat
:: What does it do:
::    - checks whether pip.ini is in proper path to enable pip proxy
::    - if not then copies a proper pip.ini into the intended path
::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: CALLING pip.ini checker - checking whether pip proxy is allowed
IF EXIST "c:\users\%USERNAME%\AppData\Roaming\pip\pip.ini" (
    ECHO pip.ini is in proper root - no need to copy
) ELSE (
	xcopy "pip.ini" "c:\users\%USERNAME%\AppData\Roaming\pip" /i /e
	ECHO "> pip.ini copied to AppData\Roaming\pip\pip.ini"
)

