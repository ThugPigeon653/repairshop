#!/bin/bash

# Set your S3 bucket name
bucket_name="repair-lneil"

# List all .py files in the S3 bucket
py_files=$(aws s3 ls "s3://$bucket_name/" | awk '{print $4}' | grep '\.py$')

# Iterate through each .py file and create a zip file
for py_file in $py_files; do
    file_name=$(basename "$py_file" .py)
    zip_file="$file_name.zip"
    
    # Download the .py file
    aws s3 cp "s3://$bucket_name/$py_file" "$py_file"
    
    # Zip the .py file
    zip "$zip_file" "$py_file"
    
    # Upload the zip file back to S3
    aws s3 cp "$zip_file" "s3://$bucket_name/$zip_file"
    
    # Clean up local files
    rm "$py_file" "$zip_file"
done

rm -r ./*

echo "All .py files zipped and uploaded to S3."
