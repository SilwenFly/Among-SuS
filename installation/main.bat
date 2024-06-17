@echo off
pip install -r requirements.txt
where /q sqlite3
if errorlevel 1 (
    tar -xf sqlite-tools-win32-x86-3350400.zip -C C:\sqlite
    setx path "%path%;C:\sqlite"
)