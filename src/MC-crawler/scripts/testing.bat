@echo off

cd /d %~dp0..
call env/scripts/activate

python -m pytest tests/ -v

pause