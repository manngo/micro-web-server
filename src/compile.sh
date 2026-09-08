#!/bin/bash
echo	Compile Python Web Server
if [ "$1" == "cli" ]; then
	echo	CLI Version

#	pyinstaller --distpath=../bin --workpath=../pyinstaller --name="MicroWebServerCLI" --onefile --clean server-cli.py
	pyinstaller --distpath=../bin --workpath=../pyinstaller MicroWebServerCLI.spec

	if [ -n "$2" ]; then
		echo signing with $2 …
		codesign --remove-signature ../bin/MicroWebServerCLI
		codesign --verbose --options runtime --timestamp --sign "$2" ../bin/MicroWebServerCLI
		codesign -dv ../bin/MicroWebServerCLI
	fi

elif [ "$1" == "gui" ]; then
	echo	GUI Version

#	pyinstaller --distpath=../bin --workpath=../pyinstaller --name="MicroWebServerGUI" --windowed --clean server-gui.py
	pyinstaller --distpath=../bin --workpath=../pyinstaller MicroWebServerGUI.spec

	if [ -n "$2" ]; then
		echo signing application with $2 …
		codesign --remove-signature ../bin/MicroWebServerGUI.app
		codesign --verbose --options runtime --timestamp --sign "$2" ../bin/MicroWebServerGUI.app
		codesign -dv ../bin/MicroWebServerGUI.app
	fi

	cd ../bin
		rm -f MicroWebServerGUI.zip
		zip -r MicroWebServerGUI.zip MicroWebServerGUI.app
	cd ../src
else
	echo Usage: compile.sh [type] [codesign]
fi