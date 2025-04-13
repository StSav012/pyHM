# Humidity Measurement

The app is a replica of an application written by Oleg Bolshakov (<a href='mailto:obolshakov@mail.ru'>obolshakov@mail.ru</a>) in 2010−2011.

The app is adapted to use modern drivers for the Advantech USB-4716 board.
The drivers are a part of the DAQNavi pack.
See www.advantech.com for the reference and the pack.

## Installing the App

Install Python if you haven't.
A good place to look for a release is www.python.org.

**Python should be 3.12 or newer.**

### Install as a Package

Providing there is a Python package.
Let's keep the things short and assume the package is named just `pyHM`.
Install it via
```commandline
python -m pip install pyHM.whl
```
or
```commandline
python -m pip install pyHM.tar.gz
```
depending on the package type.

The package will install `QtPy` and its dependencies. They are required.

You may tell the installer to acquire a package for fancy icons and a Qt bindings to your taste.
For that, use extras:
 - `icons` for the `QtAwesome` package to get fancy icons in the app,
 - `pyside6` for PySide6 buindings, the `PySide6` package,
 - `pyqt6` for PyQt6 buindings, the `PyQt6` and `PyQt6-Charts` packages,
 - `pyqt5` for PyQt5 buindings, the `PyQt5` and `PyQtChart` packages.

To specify extras, place them in brackets after the package name, e.g.,
```commandline
python -m pip install "pyHM.whl[icons, pyside6]"
```
It's likely that the quotes will be required.

### Manually

#### Prerequisites

1. Install `QtPy` using a package manager to your taste. For example, run `pip install qtpy`.
2. Depending on your OS and favours, install one of the following sets:
    * `PySide6 >=6.1, !=6.8.0, !=6.8.0.1`,
    * `PyQt5 >=5.15` and `PyQtChart >=5.15`,
    * `PyQt6 >=6.1` and `PyQt6-Charts`.
3. If you like to see icons in the Preferences dialog, install `QtAwesome`.
4. Don't forget to install Advantech drivers from www.advantech.com.

#### Getting the Code

The code is available at https://github.com/StSav012/pyHM/archive/refs/heads/master.zip.

Download it, unpack and navigate into the directory.

## Running the App
There are several ways for it:
1. If you've installed the package, `pyHM` might become directly available:
   ```commandline
   pyHM
   ```
2. Run `pyHM` as a Python module:
   ```commandline
   python -m pyHM
   ```
3. Navigate to the directory where `main.py` resides (usually, into `pyHM`)
   and feed it to Python:
   ```commandline
   python main.py
   ```
They all lead to the same behavior.

On Windows, you may use `pythonw.exe` instead of `python.exe` to hide the shell.
