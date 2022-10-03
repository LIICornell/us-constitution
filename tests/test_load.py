from load_data import load_from_json


class TestLoad:
    def test_load(self):
        model = load_from_json(prefix="/constitution-conan")
        paths = list(model.paths())
        assert paths[0] == "/constitution-conan"
        assert paths[1] == "/constitution-conan/preamble"
        assert paths[-1] == "/constitution-conan/amendment-27/clause-1"
