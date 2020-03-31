from lib.util import Config


class TestConfig:
    def test_init(self):
        c = Config(test1=1, test2=2)

        assert c.__dict__ == {'test1': 1, 'test2': 2}
