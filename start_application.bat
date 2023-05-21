@echo off
call update_environment.bat
call conda activate ythd
call python .\src\main.py
@echo on