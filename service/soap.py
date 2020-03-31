from simple_salesforce import Salesforce

from config import SFCONFIG

client = Salesforce(
    username=SFCONFIG.username,
    password=SFCONFIG.password,
    security_token=SFCONFIG.security_token
)

accounts = client.bulk.Account.query('select Id, Name from Account limit 10')

if __name__ == '__main__':
    for a in accounts:
        print(a)
