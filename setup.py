from setuptools import setup

APP = ["src/main.py"]
DATA_FILES = [
    "src/clipboard_Reader.py", 
    "src/paste_utils.py", 
    "src/word_menuitem.py",
    "src/assets"]

OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'app_icon/clipboard.png',
    'plist': {
        'CFBundleShortVersionString': '0.2.0',
        'LSUIElement': True,
    },
    'packages': [
        'rumps',
        'pyperclip']
}

setup(
    app=APP,
    name="ClipboardHistory",
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'], 
    install_requires=['rumps', 'pyperclip']
)