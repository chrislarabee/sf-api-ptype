# Salesforce API Codex

Provides useful classes and methods for connecting to a Salesforce
instance via the API.

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

### Get Salesforce Security Token

To get your security token from Salesforce, login to Salesforce, go to
your account settings and go to the My Personal Information dropdown.
Select Reset My Security Token and Salesforce will send you your new token
in an email. This is the only way to get a security token, so if you lose
your token and generate a new one you'll need to update any application
that uses the API to access Salesforce with your token.

### Setup Config

Make a copy of `config.example.py` and name it `config.py`. Populate it
with your Salesforce username, password, and security token. Optionally,
you can supply a `tables` argument (as a tuple containing table api_names)
to specify which tables you want to pull from the Salesforce instance on 
instantiation. This improves performance if you know exactly what tables 
you want to explore/pull data from. If you don't supply a `tables` 
argument, Codex will just pull all the tables on instantiation.

## Using the Codex

This repository doesn't really contain a main function, it's very much
intended to be an exploratory tool and to be incorporated into another
application.

`service.codex` contains a Codex class, which acts as the conduit to the 
Salesforce instance that the `config.py` credentials allow access to. Codex 
objects have all the requested tables of the Salesforce instance as 
attributes (or all the tables if no tables were specified in the config).

During exploration, you can always add tables to an existing Codex with the
`get_table` method. This method adds the passed table api_name as an 
attribute on the Codex, ready for further exploration and querying. 

### Metadata

When exploring a Salesforce instance via the API, you can use the Codex to
assist you. Any table in the Salesforce instance can be an attribute on the
Codex, and can provide with its metadata with:
```
Codex().Account.fields
Codex().Account.schema
```
The fields attribute is a list of all the api_names for the fields on the
table (in this case the Account table). And the schema provides additional
information about each field, like its data type and in-system Label.

For example, the schema information for the Name field on Account can be
accessed with:
```
Codex().Account.schema['Name']
# Returns {'label': 'Account Name', 'type': 'string'}
```

### Querying

You can query any of the tables in the Codex by calling the  `select` 
method on the Table attribute. Note that the Codex does not store any
records contained in Salesforce tables, nor does its Table attributes, 
running queries goes through the API to get data, the Codex and Tables
just serve as intermediaries.

For example, you can query the Account table in a Salesforce instance by
connecting a Codex and then running:
```
Codex().Account.select()
```
To select every row and column in the Account table.

You could also just select Account names and ids with:
```
Codex().Account.select('Id', 'Name')
```

And you can limit the number of records retrieved with:
```
Codex().Account.select('Id', 'Name', limit=5)
```

Or specify a where clause with:
```
Codex().Account.select('Id', 'Name', where="Name like 'Great Falls%'")
```

You can also query the Bulk API rather than the REST API with:
```
Codex().Account.select(bulk=True)
```

And you can combine any of the above kwargs as desired.

#### Custom SOQL Statements

As an alternative to querying using the Tables on the Codex, you can 
directly query the connected Salesforce instance via the REST or Bulk
API using the query and queryb methods on the Codex object:
```
Codex().query(("SELECT Id, Name FROM Account "
               "WHERE Name like 'Great Falls%'"))
```

queryb also requires that you pass the api_name of the table you
want to query:
```
Codex().queryb(("SELECT Id, Name FROM Account "
                "WHERE Name like 'Great Falls%'"),
                'Account')
```
