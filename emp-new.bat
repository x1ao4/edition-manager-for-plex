@echo off

set DIR=%~dp0

cd /d %DIR%

python3 edition-manager-for-plex.py --new

pause
