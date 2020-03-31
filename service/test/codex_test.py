from service.codex import Table


class TestTable:
    def test_gen_limit(self):
        assert Table._gen_limit() == ''
        assert Table._gen_limit(10) == ' LIMIT 10'

    def test_gen_where(self):
        assert Table._gen_where() == ''
        assert Table._gen_where('Id = 1') == ' WHERE Id = 1'
        assert Table._gen_where(
            ['Id >= 1', 'Name = Test']
        ) == ' WHERE Id >= 1 AND Name = Test'
