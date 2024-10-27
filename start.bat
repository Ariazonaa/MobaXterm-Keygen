@echo off
setlocal EnableExtensions
setlocal EnableDelayedExpansion
:: Batch script to run the Python keygen script as administrator with debug logging
set script_path=%~dp0MobaXterm-Keygen.py
set log_file=%~dp0debug_log.txt

:: Start debug logging
echo [%date% %time%] Starting script >> "%log_file%"
echo [%date% %time%] Current directory: %CD% >> "%log_file%"

:: Check if Python is installed
set python_path=""
for %%i in (python.exe) do set python_path=%%~$PATH:i
if "%python_path%"=="" (
    powershell -command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('Python is not installed or not in the system PATH. Please install Python or add it to the PATH to continue.', 'Error', [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error); exit"
    echo [%date% %time%] Python not found >> "%log_file%"
    exit /b
)

:: Log Python path
echo [%date% %time%] Python found at: %python_path% >> "%log_file%"

:: Check if script_path exists
echo [%date% %time%] Checking if script exists: %script_path% >> "%log_file%"
if not exist "%script_path%" (
    echo [%date% %time%] Script not found: %script_path% >> "%log_file%"
    if not exist "%temp%\WindowsForeground.wav" (
        powershell -command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://cdn.ariazonaa.net/sounds/WindowsForeground.wav' -OutFile '%temp%\WindowsForeground.wav'"
        echo [%date% %time%] Downloaded WindowsForeground.wav >> "%log_file%"
    )
    powershell -command "Add-Type -AssemblyName System.Windows.Forms; $player = New-Object System.Media.SoundPlayer '%temp%\WindowsForeground.wav'; $player.Play(); $form = New-Object System.Windows.Forms.Form; $form.Text = 'Error'; $form.Width = 400; $form.Height = 200; $form.BackColor = 'Red'; $form.TopMost = $true; $label = New-Object System.Windows.Forms.Label; $label.Text = 'The script MobaXterm-Keygen.py was not found in the current directory.'; $label.ForeColor = 'White'; $label.AutoSize = $true; $label.Top = 80; $label.Left = 50; $form.Controls.Add($label); $form.ShowDialog(); exit"
    exit /b
)

:: Request administrative privileges
echo [%date% %time%] Checking administrative privileges >> "%log_file%"
setlocal EnableDelayedExpansion
cd /d "%~dp0"

echo [%date% %time%] Current directory after privilege check: %CD% >> "%log_file%"

:checkAdminRights
net session >nul 2>&1
if %errorlevel% NEQ 0 (
    echo [%date% %time%] Administrative privileges not detected >> "%log_file%"
    if not exist "%temp%\WindowsForeground.wav" (
        powershell -command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://cdn.ariazonaa.net/sounds/WindowsForeground.wav' -OutFile '%temp%\WindowsForeground.wav'"
        echo [%date% %time%] Downloaded WindowsForeground.wav >> "%log_file%"
    )
    powershell -command "Add-Type -AssemblyName System.Windows.Forms; $player = New-Object System.Media.SoundPlayer '%temp%\WindowsForeground.wav'; $player.Play(); [System.Windows.Forms.MessageBox]::Show('This script must be run as administrator.', 'Error', [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error); exit"
    exit /b
)

pushd "%CD%"
CD /D "%~dp0"

echo [%date% %time%] Administrative privileges verified >> "%log_file%"
echo [%date% %time%] Current directory after pushd: %CD% >> "%log_file%"

:: Show progress bar during execution
echo [%date% %time%] Showing progress bar >> "%log_file%"
powershell -command "Add-Type -AssemblyName System.Windows.Forms; $form = New-Object System.Windows.Forms.Form; $form.Text = 'Progress'; $form.Width = 400; $form.Height = 100; $form.TopMost = $true; $progressBar = New-Object System.Windows.Forms.ProgressBar; $progressBar.Width = 350; $progressBar.Height = 30; $progressBar.Minimum = 0; $progressBar.Maximum = 100; $progressBar.Value = 0; $form.Controls.Add($progressBar); $form.Show(); for ($i = 0; $i -le 100; $i += 10) { Start-Sleep -Milliseconds 200; $progressBar.Value = $i } $form.Close(); Add-Type -AssemblyName System.Windows.Forms; Add-Type -AssemblyName System.Drawing; $form = New-Object System.Windows.Forms.Form; $form.Text = 'Success'; $form.Width = 400; $form.Height = 300; $form.StartPosition = 'CenterScreen'; $form.TopMost = $true; for ($i = 0; $i -le 360; $i += 5) { $form.Opacity = [Math]::Sin([Math]::PI * $i / 180); Start-Sleep -Milliseconds 20 } $form.Close(); [System.Windows.Forms.MessageBox]::Show('The script completed successfully!', 'Success', [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information)"

echo [%date% %time%] Progress bar completed >> "%log_file%"

:: Run the Python script
echo [%date% %time%] Running Python script: %script_path% >> "%log_file%"
if not exist "%temp%\WindowsNotifySystemGeneric.wav" (
    powershell -command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://cdn.ariazonaa.net/sounds/WindowsNotifySystemGeneric.wav' -OutFile '%temp%\WindowsNotifySystemGeneric.wav'"
    echo [%date% %time%] Downloaded WindowsNotifySystemGeneric.wav >> "%log_file%"
)
start "" cmd /c "python "%script_path%" & powershell -command "(New-Object System.Media.SoundPlayer '%temp%\WindowsNotifySystemGeneric.wav').PlaySync()""

echo [%date% %time%] Python script execution finished >> "%log_file%"

:: End of script
echo [%date% %time%] Script execution completed >> "%log_file%"
exit
