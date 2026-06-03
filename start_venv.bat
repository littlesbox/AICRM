@echo off

REM === 获取脚本所在目录 ===
set SCRIPT_DIR=%~dp0

REM === 切换到脚本所在目录（确保在项目根） ===
cd /d "%SCRIPT_DIR%"

REM === 激活虚拟环境 ===
call .venv\Scripts\activate.bat

echo.
echo Virtual environment activated.
echo Current directory:
cd
