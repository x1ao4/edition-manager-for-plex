@echo off

set DIR=%~dp0

cd /d %DIR%

python3 plex-edition-manager.py --new

pause
