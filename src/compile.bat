@echo off
echo	Compile Python Web Server
if "%1" == "cli" (
	echo	CLI Version

	pyinstaller --distpath=../bin --specpath ../pyinstaller --workpath=../pyinstaller --name="MicroWebServerCLI.exe" --clean --onefile server-cli.py
rem	pyinstaller --distpath=../bin --workpath=../pyinstaller --clean MicroWebServerCLI.exe.spec
) else if "%1" == "gui" (
	echo	GUI Version

	pyinstaller --distpath=../bin --specpath ../pyinstaller --workpath=../pyinstaller --name="MicroWebServerGUI.exe" --windowed --clean --onefile --version-file ../src/server-gui-version-info.txt server-gui.py
rem	pyinstaller --distpath=../bin --workpath=../pyinstaller --clean MicroWebServerGUI.exe.spec
) else (
	echo Usage: compile.bat [type]
)