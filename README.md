# Micro Web Server

An implementation of the Python Web Server

This is an implementation of a Micro Web Server, based on a sample found in [https://docs.python.org/3/library/http.server.html](https://docs.python.org/3/library/http.server.html).

This is not intended to be a substitute for more serious web server packages such as XAMPP or MAMP. However, it is useful if all you want to do is to develop

See [https://internotes.net/simple-web-server](https://internotes.net/simple-web-server) for a discussion on why this is useful.

There are two versions of the server, both for MacOS and Windows.

## GUI Usage

The GUI version of the server looks like this:

- MacOS

	<img src="misc/gui-mac.png" width="50%" alt="GUI MacOS">

- Windows

	<img src="misc/gui-windows.png" width="50%" alt="GUI Windows">

1. Enter the __Path__ of the directory you wish to be served. You can use the __Select …__ button to select the directory.
2. The __Host__ defaults to `localhost`. Enter an alternative name or IP address if you have one.
3. The __Port__ defaults to `8000`. Choose another if you wish. You probably can’t select a number below `1024` without privileges.

When you start, the __Start__ button will turn into __Stop__.

When ever you change any of the fields, they will be saved for next time. This uses a JSON file in `~/micro-web-server/prefs.json`.

You will also see a link to launch the site in your default browser.

##	CLI Usage

If you prefer to use the command line version, its usage is below:

- __MacOS__: `PythonWebServer --directory="…" --host=… --port=…` --go
- __Windows__: `PythonWebServer.exe --directory="…" --host=… --port=…` --go

The `--directory`, `--host`, `--port`, and `--go` parameters are all optional. Here are the options and their defaults:

| Short | Full         | Meaning             | Original Default    |
|-------|--------------|---------------------|---------------------|
| -h    | --help=      | Show Help           |                     |
| -d    | --directory= | Directory to Serve  | (current directory) |
|       | --host=      | Host URL            | localhost           |
| -p    | --port=      | Port Number         | 8000                |
| -g    | --go         | Open in Web Browser |                     |

Although not always required, its generally better to put the directory inside "quotes", to avoid problems with spaces.

Once you have launched __MicroWebServer__, the directory, host, and port settings are saved, and they will be the defaults next time.

If you include the __go__ option (`-g` or `--go`), your site will open up in your default web browser, after a delay of a few seconds.

## TODO

1. Save named project settings:

	- CLI: --use "named project"
	- GUI: Combo Box

2. Tabbed Interface with About etc


## E&OE

This application is still in an early stage. It does what it does and doesn’t do what it doesn’t do.
