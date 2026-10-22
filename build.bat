@echo off
setlocal
cd /d "%~dp0"
python -m pip install -r requirements-build.txt
python -m PyInstaller --noconfirm --clean --onefile --windowed --icon "app.ico" --add-data "app.ico;." --name "EVE-Escalation-Watcher" eve_escalation_watcher.py
endlocal
