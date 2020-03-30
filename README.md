# Salesforce API Prototype

Some testing to connect to a Developer Salesforce Instance

## Setup

Create and activate a virtual environment.

For Linux:
```
python -m venv venv
source venv/bin/activate
```
Install requirements:
```
pip install -r requirements.txt
```

Make a copy of `config.example.py` and name it `config.py`. Populate it
with your Salesforce username, password, and security token. 

### Get Salesforce Security Token

To get your security token from Salesforce, login to Salesforce, go to
your account settings and go to the My Personal Information dropdown.
Select Reset My Security Token and Salesforce will send you your new token
in an email. This is the only way to get a security token, so if you lose
your token and generate a new one you'll need to update any application
that uses the API to access Salesforce with your token.
