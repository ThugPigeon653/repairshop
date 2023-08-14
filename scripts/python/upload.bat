@echo off
setlocal

set S3_BUCKET=repair-lneil

for %%i in (*.py) do (
    aws s3 cp "%%i" "s3://%S3_BUCKET%/"
)

echo All Python files uploaded to S3 bucket: %S3_BUCKET%