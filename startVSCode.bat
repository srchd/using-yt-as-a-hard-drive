@echo off
call update_environment.bat
call conda activate ythd
call python startVSCode.py
@echo on