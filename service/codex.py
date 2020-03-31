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
                self._tables[o['label']] = t
                setattr(self, o['name'], t)

    def query(self, *cols, table: str, **kwargs):
        if table not in self._tables.keys():
            raise ValueError(f'{table} is not a valid table name.')
        limit = self._gen_limit(kwargs.get('limit'))
        where = self._gen_where(kwargs.get('where'))
        q = self._gen_query(cols, table, where, limit)
        return self.client.query(q)

    @staticmethod
    def _gen_limit(limit=None):
        if limit:
            return ' LIMIT ' + str(limit)
        else:
            return ''

    @staticmethod
    def _gen_query(columns: list, table: str, where: str, limit: str):
        cols = ', '.join(columns)
        return 'SELECT ' + cols + ' FROM ' + table + where + limit

    @staticmethod
    def _gen_where(where=None):
        if where:
            if isinstance(where, list):
                w = ' AND '.join(where)
            else:
                w = where
            return ' WHERE ' + w
        else:
            return ''


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
