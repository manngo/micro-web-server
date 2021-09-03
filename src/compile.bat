echo	Compile Python Web Server
echo	CLI Version
	pyinstaller --distpath=../bin --specpath ../pyinstaller --workpath=../pyinstaller --name="MicroWebServerCLI.exe" --clean --onefile server-cli.py
echo	GUI Version
	pyinstaller --distpath=../bin --specpath ../pyinstaller --workpath=../pyinstaller --name="MicroWebServerGUI.exe" --windowed --clean --onefile server-gui.py
	cd ../bin
	zip -r MicroWebServerGUI.zip MicroWebServerGUI.app
	cd ../src
