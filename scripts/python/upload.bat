@echo off

setlocal enabledelayedexpansion

for %%F in (*.py) do (
    set filename=%%~nF
    aws s3 cp "%%F" "s3://repair-lneil/!filename!.py"
)

echo All .py files uploaded to repair-lneil S3 bucket.
pause