# HandyTray
Tray Application to add software for quick access.

This is a tray application that let's you add various software to for quick launch. Under one tray icon you can have a list of
various applications for easy access. Comments for each application can also be added.

Screenshot:

![alt text](https://raw.githubusercontent.com/activatedtmx/HandyTray/master/sample_screenshot.png)

Compile:
pyinstaller main.py -F -i tray.ico -n 'Handy Tray' --hidden-import pkg_resources --hidden-import infi.systray --hidden-import Pillow --uac-admin --noconsole
