@echo off
setlocal enabledelayedexpansion
set ENV=""
set NEEDED_ENV=ythd

for /f %%e in ('conda info --envs') do (
	if %%e==%NEEDED_ENV% (
		set ENV=%%e
	)
)

if !ENV!=="" (
	echo Env not found! Creating it from envs/Windows.yml
	call conda env create -f envs/Windows.yml
)
@echo on
