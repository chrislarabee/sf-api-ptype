from service.codex import Codex


class TestCodex:
    def test_gen_limit(self):
        assert Codex._gen_limit() == ''
        assert Codex._gen_limit(10) == ' LIMIT 10'

    def test_gen_query(self):
        assert Codex._gen_query(
            ['Id', 'Name'], 'Account', '', '') == (
            'SELECT Id, Name FROM Account')

    def test_gen_where(self):
        assert Codex._gen_where() == ''
        assert Codex._gen_where('Id = 1') == ' WHERE Id = 1'
        assert Codex._gen_where(
            ['Id >= 1', 'Name = Test']
        ) == ' WHERE Id >= 1 AND Name = Test'
