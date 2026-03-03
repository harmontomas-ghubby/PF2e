@echo off
setlocal
set "APP_PATH=%~dp0app\index.html"
if not exist "%APP_PATH%" (
  echo Could not find app\index.html
  pause
  exit /b 1
)
start "" "%APP_PATH%"
