# global_protect_auto_login
Avoid copying and pasting multiple times while logging into global protect. Login with one click using this application.

# Instructions
* To install virtual environment use the following code: conda create --prefix ./env python=3.11
* Then activate the environment: conda activate ./env 
* Then install the requirements: pip install -r requirements.txt
* If your email is in microsoft.outlook you will need to register your application in azure to get
client_id and tenant_id. Put these information in a .env file.
* Once you register your application you need to add a Redirect URI (http://localhost) for Mobile and desktop applications.
