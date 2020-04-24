from pyperclip import copy
from simple_salesforce import Salesforce, SFType

from config import SFCONFIG


class Codex:
    """
    Acts as a conduit to a Salesforce instance, as well as a central
    repository for metadata on the tables in the instance.
    """
    def __init__(self):
        self.client = Salesforce(
            username=SFCONFIG.username,
            password=SFCONFIG.password,
            security_token=SFCONFIG.security_token
        )
        self._tables = dict()
        for o in self.client.describe()['sobjects']:
            n = o['name']
            if o['createable'] and (n in SFCONFIG.tables or
                                    len(SFCONFIG.tables) == 0):
                self.get_table(n)

    def get_table(self, table_api_name: str):
        """
        Adds a table from the attached Salesforce instance as a new
        Table object attribute on the Codex.

        Args:
            table_api_name: A string, the API name of the table in the
                attached Salesforce instance.

        Returns: The generated Table object.

        """
        t = Table(getattr(self.client, table_api_name), self)
        self._tables[table_api_name] = t
        setattr(self, table_api_name, t)
        return t

    def query(self, q: str):
        """
        Queries the Salesforce REST API using the passed SOQL query
        string.

        Args:
            q: A valid SOQL query string.

        Returns: A list of OrderedDicts, the records resulting from
            the bulk query.

        """
        r = self.client.query(q)
        results = r['records']
        while not r['done']:
            r = self.client.query_more(r['nextRecordsUrl'], True)
            results += r['records']
        return results

    def queryb(self, q: str, table_api_name: str) -> list:
        """
        Queries the Salesforce Bulk API using the passed SOQL query
        string and table_api_name.

        Args:
            q: A valid SOQL query string.
            table_api_name: A table's api_name.

        Returns: A list of OrderedDicts, the records resulting from
            the bulk query.

        """
        return getattr(self.client.bulk, table_api_name).query(q)


class Table:
    """
    Acts as the repository for metadata on a specific table from a
    Salesforce instance and provides attributes and methods that make
    accessing said metadata as convenient as possible.
    """
    def __init__(self, sftype_obj: SFType, parent: Codex):
        """
        Tables should only be generated by a Codex object. Generally
        speaking, they should also only be interacted with through the
        Codex, as well.

        Args:
            sftype_obj: A simple_salesforce.SFType object from a
                Salesforce().describe() method.
            parent: A Codex object.
        """
        self.parent = parent
        self._sftype_obj = sftype_obj
        self.api_name = self._sftype_obj.name
        self.label = self._sftype_obj.describe()['label']
        (self.fields, self.schema,
         self.field_ct, self.cfield_ct) = self._gen_schema(sftype_obj)

    def select(self, *cols, **kwargs):
        """
        Generates a SOQL query string to select the passed columns
        from this Table.

        Args:
            *cols: A list of valid fields found on this Table. Skip
                this argument or pass '*' or None to select all the
                fields on this Table.
            **kwargs: Currently in use kwargs:
                bulk: A boolean, which toggles whether to use the
                    Salesforce bulk API (True) or the REST API
                    (False/None).
                limit: An integer, specifies the maximum number of
                    records to return from this select statement.
                where: A string or list/tuple of strings, which will
                    be added as a where clause on the select statement.
                    Each condition supplied in where must be true for
                    the record to be returned.

        Returns: The results of the select statement.

        """
        limit = self._gen_limit(kwargs.get('limit'))
        where = self._gen_where(kwargs.get('where'))
        field_str = self._field_str(cols)
        q = ('SELECT ' + field_str + ' FROM ' + self.api_name
             + where + limit)
        if kwargs.get('bulk'):
            return self.parent.queryb(q, self.api_name)
        else:
            return self.parent.query(q)

    def _field_str(self, fields: (list, tuple)):
        """
        Generates a string of field/column names for this Table, based
        on the passed argument. Passed field/column names are validated
        to ensure they are found in this Table.

        Args:
            fields: A list or tuple of field names. The first value can
                be None or '*", which will cause _field_str to generate
                a string containing the names of every field/column on
                this Table.

        Returns: A comma-separated string of field/column names.

        """
        valid_fields = []
        if len(fields) == 0 or fields[0] in (None, '*'):
            valid_fields = self.fields
        else:
            for f in fields:
                if f in self.fields:
                    valid_fields.append(f)
                else:
                    raise ValueError(f'{f} is not a valid field in '
                                     f'table {self.api_name}')
        return ', '.join(valid_fields)

    @staticmethod
    def _gen_limit(limit=None):
        """
        Generates a SOQL limit clause.

        Args:
            limit: An integer.

        Returns: A string, either '' or ' LIMIT limit'.

        """
        if limit:
            if isinstance(limit, int):
                return ' LIMIT ' + str(limit)
            else:
                raise ValueError(f'limit must be an integer: ({limit})')
        else:
            return ''

    @staticmethod
    def _gen_schema(sftype_obj: SFType):
        """
        Generates a list of field/column names on this Table, as well
        as a dictionary with field/column names as keys and data types
        and front-end labels for that field/column.

        Args:
            sftype_obj: A simple_salesforce.SFType object with
                a describe() method that contains 'fields' as a key.

        Returns: A list of field/column api_names and a dictionary
            containing information about said field/columns.

        """
        cols = []
        schema = dict()
        cust_field_ct = 0
        for f in sftype_obj.describe()['fields']:
            name = f['name']
            custom = f['custom']
            if custom:
                cust_field_ct += 1
            schema[name] = dict(
                label=f['label'],
                type=f['type'],
                custom=custom
            )
            cols.append(name)
        return Record(cols), Record(schema), len(cols), cust_field_ct

    @staticmethod
    def _gen_where(where=None):
        """
        Generates a SOQL where clause.

        Args:
            where: A string or list of strings.

        Returns: A string, either '' or ' WHERE where...'

        """
        if where:
            if isinstance(where, list) or isinstance(where, tuple):
                w = ' AND '.join(where)
            else:
                w = where
            return ' WHERE ' + w
        else:
            return ''


class Record:
    """
    A convenience object that wraps other python objects and provides
    methods like clip that make it easier to explore and move the data
    stored in said objects.
    """
    def __init__(self, r):
        """

        Args:
            r: Any object.
        """
        self._data = r

    def clip(self):
        """
        Uses pyperclip to copy the data held by the Record object to
        the clipboard. Removes python syntax around strings and such.

        Returns: None

        """
        if isinstance(self._data, list):
            d = ','.join(self._data)
        elif isinstance(self._data, dict):
            x = []
            for k, v in self._data.items():
                x.append(f'{k}:{v}')
            d = ','.join(x)
        else:
            d = str(self._data)
        copy(d)

    def __repr__(self):
        """
        Overrides __repr__ so that when the Record is called it spits
        out the data it contains rather than a representation of the
        Record object.

        Returns: A string representation of the data in self._data.

        """
        return str(self._data)
