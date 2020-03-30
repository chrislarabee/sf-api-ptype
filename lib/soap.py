from simple_salesforce import Salesforce

from config import SFCONFIG

client = Salesforce(
    username=SFCONFIG.username,
    password=SFCONFIG.password,
    security_token=SFCONFIG.security_token
)
