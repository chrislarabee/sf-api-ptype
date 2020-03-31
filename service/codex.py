from simple_salesforce import Salesforce, SFType

from service.util import Config


class Codex:
    def __init__(self, config: Config):
        self.client = Salesforce(
            username=config.username,
            password=config.password,
            security_token=config.security_token
        )
        self._tables = dict()
        for o in self.client.describe()['sobjects']:
            if o['createable']:
                self._tables[o['name']] = getattr(self.client, o['name'])

    def schema(self, tablename: str):
        return self._gen_schema(self._tables[tablename])

    @staticmethod
    def _gen_schema(sftype_obj: SFType):
        cols = []
        for f in sftype_obj.describe()['fields']:
            d = dict(
                label=f['label'],
                name=f['name'],
                type=f['type']
            )
            cols.append(d)
        return cols
