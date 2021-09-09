echo	Compile Python Web Server
echo	CLI Version
	rem	pyinstaller --distpath=../bin --specpath ../pyinstaller --workpath=../pyinstaller --name="MicroWebServerCLI.exe" --clean --onefile server-cli.py
	pyinstaller --distpath=../bin --workpath=../pyinstaller --clean MicroWebServerCLI.exe.spec
echo	GUI Version
	rem	pyinstaller --distpath=../bin --specpath ../pyinstaller --workpath=../pyinstaller --name="MicroWebServerGUI.exe" --windowed --clean --onefile --version-file ../src/server-gui-version-info.txt server-gui.py
	pyinstaller --distpath=../bin --workpath=../pyinstaller --clean MicroWebServerGUI.exe.spec
	rem	pyi-set_version server-gui-version-info.txt ..\bin\MicroWebServerGUI.exe
