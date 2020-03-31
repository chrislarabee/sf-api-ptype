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
                t = Table(getattr(self.client, o['name']))
                self._tables[o['name']] = t
                setattr(self, o['name'], t)


class Table:
    def __init__(self, sftype_obj: SFType):
        self._sftype_obj = sftype_obj
        self.cols, self.schema = self._gen_schema(sftype_obj)

    @staticmethod
    def _gen_schema(sftype_obj: SFType):
        cols = []
        schema = dict()
        for f in sftype_obj.describe()['fields']:
            label = f['label']
            name = f['name']
            type_ = f['type']
            schema[name] = dict(
                label=label,
                type=type_
            )
            cols.append(label)
        return cols, schema
