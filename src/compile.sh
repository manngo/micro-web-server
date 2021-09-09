#!/bin/bash
echo	Compile Python Web Server
echo	CLI Version
	#	pyinstaller --distpath=../bin --specpath ../pyinstaller --workpath=../pyinstaller --name="MicroWebServerCLI" --clean --onefile server-cli.py
	pyinstaller --distpath=../bin --workpath=../pyinstaller --clean MicroWebServerCLI.spec
echo	GUI Version
	#	pyinstaller --distpath=../bin --specpath ../pyinstaller --workpath=../pyinstaller --name="MicroWebServerGUI" --windowed --clean --onefile server-gui.py
	#	pyi-makespec --name="MicroWebServerGUI" --windowed --onefile server-gui.py
	pyinstaller --distpath=../bin --workpath=../pyinstaller --clean MicroWebServerGUI.spec
	cd ../bin
	rm -f MicroWebServerGUI.zip
	zip -r MicroWebServerGUI.zip MicroWebServerGUI.app
	cd ../src
