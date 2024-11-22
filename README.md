# Humidity Measurement

The app is a replica of an application written by Oleg Bolshakov (<a href='mailto:obolshakov@mail.ru'>obolshakov@mail.ru</a>) in 2010−2011.

The app is adapted to use modern drivers for the Advantech USB-4716 board.
The drivers are a part of the DAQNavi pack.
See www.advantech.com for the reference and the pack.

## Running the App

### Prerequisites

0. Install Python if you haven't. A good place to look for a release is www.python.org.
1. Install `QtPy` using a package manager to your taste. For example, run `pip install qtpy`.
2. Depending on your OS and favours, install one of the following sets:
    * `PySide6 >=6.1, !=6.8.0, !=6.8.0.1`,
    * `PyQt5 >=5.15` and `PyQtChart >=5.15`,
    * `PyQt6 >=6.1` and `PyQt6-Charts`.
3. If you like to see icons in the Preferences dialog, install `QtAwesome`.
4. Don't forget to install Advantech drivers from www.advantech.com.

### Running the App

Feed `main.py` to Python:
```commandline
python main.py
```

On Windows, you may use `pythonw.exe` instead of `python.exe` to hide the shell.
