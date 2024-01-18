This application focuses on cms and invoicing needs of a repair shop. For a better
understanding of the function of this application, see scripts/ddl.sql, and scripts/
cloudformation/template.json

IMPORTANT: This web application has been created for my own eduction, and should 
not be considered production-ready. 
The application is mostly complete, but is still currently under active development.
Some important things to keep in mind are:
    - Built for lowest cost: multi-az, high-performance instances, etc. have not 
    been applied. This is to reduce cost during development phase.
    - The cloudforamtion currently contains some variables which will become 
    sensitive, if this is deployed as-is. Be sure you understand who might be able
    to gain access to these values, and what that means for you. 
    - There is a major vulnerability at the moment, regarding one of the API 
    gateway methods currently NOT configured to require auth. This has been done
    for testing purposes, and is not suitable for production.
    - The frontend is partially complete. Extensive testing will be required once
    this is done
    - No CICD pipeline has been added yet for the lambda functions. This is a critical
    step if you wish to has a managable, upgradable application

---------------------------------------------------------------------------------------

DEPLOYMENT: The final deployment process should be far more streamlined, however
the currrent deployment process is as follows:

    1. Setup s3 bucket
     - Create a bucket s3, called 'repair-lneil'. This naming does need to be 
     globally unique - if you need to change the name, you will also need to ammend
     the cloudformation template, as well as the .sh and .bat files in scripts/.
     - Windows users can run 'upload.bat', which will automatically upload all 
     scripts to the previously mentioned s3 location. If you cannot run .bat, a
     manual upload to s3 will be required. This can easily be done with s3 cli, or
     by using the s3 console directly. If this is the case, only add the full contents
     of the scripts/ directory.
     - Next, you will need to run 'zip-python.sh' on a linux machine, with s3 
     access. The easiest way to do this is by using cloudshell. The bash script
     has been written to cleanup after itself automatically, so no files will be 
     inadvertently left on the machine. 
     - Note: both of the provided helper scripts are dynamic, so you do not need to 
     change them if more backed scripts are added to this folder - they  will 
     indiscriminantly upload and zip all scripts/*.py files to s3.

    2. Cloudformation deployment
     - Deploy 'template.json', using Cloudformation. This will automatically create
     all the aws infrastructure require. 

    3. Frontend
     - The frontend is in the midst of development, and is only partially functional.
     - To connect to the api gateway, you will need to update the url found in 
     "src/custom-exports.js", and the value of 'proxy' in package.json. 
     - The frontend can be run anywhere at the moment. 
     - The frontend should work after cors has been corrected, and auth has been fully
     implemented (i.e. Amplify Authenticator frontend component)

---------------------------------------------------------------------------------------

DEVELOPER INFO:
Lachlan Neilsen
lnelisen1996@outlook.com
